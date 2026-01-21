"""Tests for the structural parser."""

from pathlib import Path

import pytest
from prompt_lang.config import Config, load_config
from prompt_lang.errors import ValidationResult
from prompt_lang.parser import ParsedPrompt, parse_content, parse_file

# Test fixtures directory
FIXTURES_DIR = Path(__file__).parent / "fixtures"
VALID_DIR = FIXTURES_DIR / "valid"
INVALID_DIR = FIXTURES_DIR / "invalid"


class TestValidPrompts:
    """Tests for valid prompt files."""

    def test_minimal_prompt_passes(self):
        """Minimal prompt with only required elements should pass."""
        parsed, result = parse_file(VALID_DIR / "minimal.md")

        assert result.passed, f"Expected pass but got errors: {result}"
        assert parsed.frontmatter is not None
        assert parsed.frontmatter["name"] == "minimal-skill"
        assert parsed.has_tag("purpose")
        assert parsed.has_tag("instructions")

    def test_full_prompt_passes(self):
        """Full prompt with all tags should pass."""
        parsed, result = parse_file(VALID_DIR / "full.md")

        assert result.passed, f"Expected pass but got errors: {result}"
        assert parsed.frontmatter["name"] == "full-skill"
        assert parsed.frontmatter["model"] == "sonnet"

        # Check all tags present
        expected_tags = [
            "purpose",
            "variables",
            "context",
            "instructions",
            "workflow",
            "constraints",
            "examples",
            "output",
            "criteria",
        ]
        for tag_name in expected_tags:
            assert parsed.has_tag(tag_name), f"Missing tag: {tag_name}"

    def test_deploy_service_passes(self):
        """Deploy service example from spec should pass."""
        parsed, result = parse_file(VALID_DIR / "deploy-service.md")

        assert result.passed, f"Expected pass but got errors: {result}"
        assert parsed.frontmatter["name"] == "deploy-service"

        # Check instructions contain code blocks
        instructions = parsed.get_tag("instructions")
        assert instructions is not None
        assert "```bash" in instructions.content


class TestMissingFrontmatter:
    """Tests for frontmatter validation."""

    def test_missing_frontmatter_fails(self):
        """File without frontmatter should fail."""
        parsed, result = parse_file(INVALID_DIR / "missing-frontmatter.md")

        assert not result.passed
        assert any("frontmatter" in e.message.lower() for e in result.errors)

    def test_missing_name_field_fails(self):
        """Frontmatter without 'name' field should fail."""
        content = """---
description: Missing name field
---

# Test

<purpose>
Test purpose.
</purpose>

<instructions>
1. Do something
</instructions>
"""
        result = ValidationResult(file_path="test.md")
        config = load_config()
        parsed, result = parse_content(content, result, config)

        assert not result.passed
        assert any("name" in e.message for e in result.errors)

    def test_missing_description_field_fails(self):
        """Frontmatter without 'description' field should fail."""
        content = """---
name: test-skill
---

# Test

<purpose>
Test purpose.
</purpose>

<instructions>
1. Do something
</instructions>
"""
        result = ValidationResult(file_path="test.md")
        config = load_config()
        parsed, result = parse_content(content, result, config)

        assert not result.passed
        assert any("description" in e.message for e in result.errors)


class TestMissingTags:
    """Tests for required tag validation."""

    def test_missing_purpose_fails(self):
        """File without <purpose> tag should fail."""
        parsed, result = parse_file(INVALID_DIR / "missing-purpose.md")

        assert not result.passed
        assert any("<purpose>" in e.message for e in result.errors)

    def test_missing_instructions_fails(self):
        """File without <instructions> tag should fail."""
        parsed, result = parse_file(INVALID_DIR / "missing-instructions.md")

        assert not result.passed
        assert any("<instructions>" in e.message for e in result.errors)


class TestTagValidation:
    """Tests for tag structure validation."""

    def test_nested_tags_fails(self):
        """Nested tags should fail."""
        parsed, result = parse_file(INVALID_DIR / "nested-tags.md")

        assert not result.passed
        assert any("nested" in e.message.lower() for e in result.errors)

    def test_unclosed_tag_fails(self):
        """Unclosed tag should fail."""
        parsed, result = parse_file(INVALID_DIR / "unclosed-tag.md")

        assert not result.passed
        assert any("unclosed" in e.message.lower() for e in result.errors)

    def test_mismatched_tag_fails(self):
        """Mismatched opening/closing tags should fail."""
        parsed, result = parse_file(INVALID_DIR / "mismatched-tag.md")

        assert not result.passed
        # Should have either mismatched or unclosed error
        has_mismatch_error = any(
            "mismatched" in e.message.lower() or "unclosed" in e.message.lower()
            for e in result.errors
        )
        assert has_mismatch_error

    def test_unrecognized_tag_fails(self):
        """Unrecognized tag should fail."""
        parsed, result = parse_file(INVALID_DIR / "unrecognized-tag.md")

        assert not result.passed
        assert any("unrecognized" in e.message.lower() for e in result.errors)
        assert any("<unknown>" in e.message for e in result.errors)


class TestTokenCounting:
    """Tests for token counting."""

    def test_token_count_calculated(self):
        """Token count should be calculated."""
        parsed, result = parse_file(VALID_DIR / "minimal.md")

        assert result.token_count > 0

    def test_token_warning_threshold(self):
        """Token count exceeding warn threshold should warn."""
        # Create a large content that exceeds warn threshold
        large_content = (
            """---
name: large-prompt
description: A very large prompt
---

# Large Prompt

<purpose>
Test token counting.
</purpose>

<instructions>
"""
            + ("1. Do something with a lot of text. " * 500)
            + """
</instructions>
"""
        )
        result = ValidationResult(file_path="test.md")
        config = load_config()
        # Set low threshold for testing
        config.validation.tokens.warn_at = 100
        config.validation.tokens.fail_at = 10000

        parsed, result = parse_content(large_content, result, config)

        assert len(result.warnings) > 0
        assert any("token" in w.message.lower() for w in result.warnings)

    def test_token_fail_threshold(self):
        """Token count exceeding fail threshold should error."""
        large_content = (
            """---
name: huge-prompt
description: An extremely large prompt
---

# Huge Prompt

<purpose>
Test token counting.
</purpose>

<instructions>
"""
            + ("1. Do something with a lot of text. " * 500)
            + """
</instructions>
"""
        )
        result = ValidationResult(file_path="test.md")
        config = load_config()
        # Set low threshold for testing
        config.validation.tokens.fail_at = 100

        parsed, result = parse_content(large_content, result, config)

        assert not result.passed
        assert any("token" in e.message.lower() for e in result.errors)


class TestParsedPrompt:
    """Tests for ParsedPrompt helper methods."""

    def test_get_tag_returns_tag(self):
        """get_tag should return the tag if it exists."""
        parsed, result = parse_file(VALID_DIR / "minimal.md")

        purpose = parsed.get_tag("purpose")
        assert purpose is not None
        assert purpose.name == "purpose"
        assert len(purpose.content) > 0

    def test_get_tag_returns_none_for_missing(self):
        """get_tag should return None for missing tags."""
        parsed, result = parse_file(VALID_DIR / "minimal.md")

        workflow = parsed.get_tag("workflow")
        assert workflow is None

    def test_has_tag_returns_true_for_existing(self):
        """has_tag should return True for existing tags."""
        parsed, result = parse_file(VALID_DIR / "minimal.md")

        assert parsed.has_tag("purpose")
        assert parsed.has_tag("instructions")

    def test_has_tag_returns_false_for_missing(self):
        """has_tag should return False for missing tags."""
        parsed, result = parse_file(VALID_DIR / "minimal.md")

        assert not parsed.has_tag("workflow")
        assert not parsed.has_tag("nonexistent")


class TestEdgeCases:
    """Tests for edge cases and special scenarios."""

    def test_empty_file_fails(self):
        """Empty file should fail."""
        content = ""
        result = ValidationResult(file_path="test.md")
        config = load_config()

        parsed, result = parse_content(content, result, config)

        assert not result.passed

    def test_frontmatter_only_fails(self):
        """File with only frontmatter should fail (missing tags)."""
        content = """---
name: test
description: Test
---
"""
        result = ValidationResult(file_path="test.md")
        config = load_config()

        parsed, result = parse_content(content, result, config)

        assert not result.passed
        assert any("<purpose>" in e.message for e in result.errors)
        assert any("<instructions>" in e.message for e in result.errors)

    def test_malformed_yaml_fails(self):
        """Malformed YAML in frontmatter should fail."""
        content = """---
name: test
description: [unclosed bracket
---

# Test

<purpose>Test</purpose>
<instructions>1. Test</instructions>
"""
        result = ValidationResult(file_path="test.md")
        config = load_config()

        parsed, result = parse_content(content, result, config)

        assert not result.passed
        assert any("yaml" in e.message.lower() for e in result.errors)

    def test_case_insensitive_tags(self):
        """Tags should be case-insensitive."""
        content = """---
name: test
description: Test case insensitivity
---

# Test

<PURPOSE>
This is the purpose.
</PURPOSE>

<Instructions>
1. Do something
</Instructions>
"""
        result = ValidationResult(file_path="test.md")
        config = load_config()

        parsed, result = parse_content(content, result, config)

        assert result.passed, f"Expected pass but got: {result}"
        assert parsed.has_tag("purpose")
        assert parsed.has_tag("instructions")
