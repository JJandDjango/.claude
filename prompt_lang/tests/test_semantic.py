"""Tests for semantic validation."""

from pathlib import Path

import pytest

from prompt_lang.config import Config, load_config
from prompt_lang.errors import ValidationResult
from prompt_lang.parser import parse_content, parse_file
from prompt_lang.semantic import (
    _find_ambiguous_patterns,
    _pattern_to_regex,
    check_ambiguous_language,
    validate_semantic,
)

# Test fixtures directory
FIXTURES_DIR = Path(__file__).parent / "fixtures"
VALID_DIR = FIXTURES_DIR / "valid"
INVALID_DIR = FIXTURES_DIR / "invalid"


class TestAmbiguousLanguageDetection:
    """Tests for ambiguous language detection."""

    def test_ambiguous_language_detected(self):
        """Ambiguous language in instructions should be detected."""
        parsed, result = parse_file(INVALID_DIR / "ambiguous-language.md")
        config = load_config()

        # Run semantic check
        matches = check_ambiguous_language(parsed, result, config)

        assert len(matches) > 0
        assert not result.passed

        # Check specific patterns were found
        patterns_found = [m.pattern for m in matches]
        assert "maybe" in patterns_found
        assert "you could" in patterns_found
        assert "consider" in patterns_found

    def test_valid_prompt_no_ambiguity(self):
        """Valid prompts should have no ambiguous language."""
        parsed, result = parse_file(VALID_DIR / "minimal.md")
        config = load_config()

        matches = check_ambiguous_language(parsed, result, config)

        assert len(matches) == 0

    def test_full_prompt_no_ambiguity(self):
        """Full valid prompt should have no ambiguous language."""
        parsed, result = parse_file(VALID_DIR / "full.md")
        config = load_config()

        matches = check_ambiguous_language(parsed, result, config)

        assert len(matches) == 0

    def test_all_default_patterns_detected(self):
        """All default ambiguous patterns should be detected."""
        content = """---
name: test
description: Test all patterns
---

# Test

<purpose>
Test ambiguous pattern detection.
</purpose>

<instructions>
1. Maybe do this
2. You might want to check
3. Consider the options
4. Optionally run tests
5. Try to complete the task
6. Possibly update the file
7. It would be good to verify
8. You could deploy now
9. Perhaps check the logs
</instructions>
"""
        result = ValidationResult(file_path="test.md")
        config = load_config()
        parsed, result = parse_content(content, result, config)

        matches = check_ambiguous_language(parsed, result, config)

        # All 9 patterns should be found
        patterns_found = [m.pattern for m in matches]
        expected_patterns = [
            "maybe",
            "might",
            "consider",
            "optionally",
            "try to",
            "possibly",
            "it would be good to",
            "you could",
            "perhaps",
        ]
        for pattern in expected_patterns:
            assert pattern in patterns_found, f"Pattern '{pattern}' not found"


class TestPatternMatching:
    """Tests for pattern matching utilities."""

    def test_word_boundary_matching(self):
        """Patterns should match at word boundaries only."""
        regex = _pattern_to_regex("maybe")

        # Should match
        assert regex.search("maybe do this")
        assert regex.search("Maybe do this")
        assert regex.search("do this maybe")
        assert regex.search("do maybe this")

        # Should NOT match (part of another word)
        assert not regex.search("mayberry")
        assert not regex.search("somemaybe")

    def test_case_insensitive_matching(self):
        """Pattern matching should be case-insensitive."""
        regex = _pattern_to_regex("consider")

        assert regex.search("consider this")
        assert regex.search("Consider this")
        assert regex.search("CONSIDER this")
        assert regex.search("CoNsIdEr this")

    def test_multi_word_pattern(self):
        """Multi-word patterns should match correctly."""
        regex = _pattern_to_regex("try to")

        assert regex.search("try to do this")
        assert regex.search("please try to complete")

        # Should not match with extra words in between
        assert not regex.search("try hard to")

    def test_phrase_pattern(self):
        """Phrase patterns should match correctly."""
        regex = _pattern_to_regex("it would be good to")

        assert regex.search("it would be good to check")
        assert regex.search("It would be good to verify")


class TestValidateSemantic:
    """Tests for the main validate_semantic function."""

    def test_validate_semantic_adds_errors(self):
        """validate_semantic should add errors for ambiguous language."""
        parsed, result = parse_file(INVALID_DIR / "ambiguous-language.md")
        config = load_config()

        validate_semantic(parsed, result, config)

        assert not result.passed
        assert len(result.errors) > 0
        assert any("ambiguous" in e.message.lower() for e in result.errors)

    def test_validate_semantic_respects_config_disable(self):
        """validate_semantic should skip checks when disabled in config."""
        parsed, result = parse_file(INVALID_DIR / "ambiguous-language.md")
        config = load_config()
        config.validation.semantic_check = False

        # Clear any structural errors first
        result.errors = []

        validate_semantic(parsed, result, config)

        # No semantic errors should be added
        assert len(result.errors) == 0

    def test_validate_semantic_passes_valid_prompt(self):
        """validate_semantic should pass for valid prompts."""
        parsed, result = parse_file(VALID_DIR / "deploy-service.md")
        config = load_config()

        validate_semantic(parsed, result, config)

        # Should still pass (no ambiguous language)
        assert result.passed


class TestEdgeCases:
    """Tests for edge cases in semantic validation."""

    def test_no_instructions_tag(self):
        """Missing instructions tag should not cause error in semantic check."""
        content = """---
name: test
description: Test without instructions
---

# Test

<purpose>
Test purpose.
</purpose>
"""
        result = ValidationResult(file_path="test.md")
        config = load_config()
        parsed, result = parse_content(content, result, config)

        # Clear structural errors about missing instructions
        structural_errors = result.errors.copy()
        result.errors = []

        matches = check_ambiguous_language(parsed, result, config)

        # Should return empty list, not error
        assert len(matches) == 0
        assert len(result.errors) == 0

    def test_empty_instructions(self):
        """Empty instructions tag should not cause error."""
        content = """---
name: test
description: Test with empty instructions
---

# Test

<purpose>
Test purpose.
</purpose>

<instructions>
</instructions>
"""
        result = ValidationResult(file_path="test.md")
        config = load_config()
        parsed, result = parse_content(content, result, config)

        matches = check_ambiguous_language(parsed, result, config)

        assert len(matches) == 0

    def test_ambiguous_in_context_allowed(self):
        """Ambiguous language in <context> should be allowed."""
        content = """---
name: test
description: Test ambiguous in context
---

# Test

<purpose>
Test purpose.
</purpose>

<context>
You might want to know that this is background info.
Maybe this is useful context.
Consider this as reference material.
</context>

<instructions>
1. Do the thing
2. Complete the task
</instructions>
"""
        result = ValidationResult(file_path="test.md")
        config = load_config()
        parsed, result = parse_content(content, result, config)

        matches = check_ambiguous_language(parsed, result, config)

        # Ambiguous language in <context> should NOT be flagged
        assert len(matches) == 0
        assert result.passed

    def test_ambiguous_in_examples_allowed(self):
        """Ambiguous language in <examples> should be allowed."""
        content = """---
name: test
description: Test ambiguous in examples
---

# Test

<purpose>
Test purpose.
</purpose>

<instructions>
1. Do the thing
</instructions>

<examples>
**Input:** User says "maybe do this"
**Output:** Agent does this definitively
</examples>
"""
        result = ValidationResult(file_path="test.md")
        config = load_config()
        parsed, result = parse_content(content, result, config)

        matches = check_ambiguous_language(parsed, result, config)

        # Ambiguous language in <examples> should NOT be flagged
        assert len(matches) == 0
        assert result.passed

    def test_line_numbers_correct(self):
        """Line numbers in error messages should be accurate."""
        content = """---
name: test
description: Test line numbers
---

# Test

<purpose>
Test purpose.
</purpose>

<instructions>
1. Do the first thing
2. Do the second thing
3. Maybe do the third thing
4. Do the fourth thing
</instructions>
"""
        result = ValidationResult(file_path="test.md")
        config = load_config()
        parsed, result = parse_content(content, result, config)

        matches = check_ambiguous_language(parsed, result, config)

        assert len(matches) == 1
        # The "maybe" should be on line 15 (after frontmatter and other content)
        assert matches[0].pattern == "maybe"
        # Line number should point to the actual line with "maybe"
        assert matches[0].line > 10  # Should be somewhere after the header

    def test_custom_patterns(self):
        """Custom ambiguous patterns from config should be detected."""
        content = """---
name: test
description: Test custom patterns
---

# Test

<purpose>
Test purpose.
</purpose>

<instructions>
1. Kinda do this
2. Sorta complete the task
</instructions>
"""
        result = ValidationResult(file_path="test.md")
        config = load_config()
        # Add custom patterns
        config.validation.ambiguous_patterns.extend(["kinda", "sorta"])

        parsed, result = parse_content(content, result, config)
        matches = check_ambiguous_language(parsed, result, config)

        patterns_found = [m.pattern for m in matches]
        assert "kinda" in patterns_found
        assert "sorta" in patterns_found
