"""Tests for directive parsing and validation."""

import pytest

from prompt_lang.config import DirectiveConfig, InstructionConfig
from prompt_lang.directives import (
    Directive,
    extract_instruction_steps,
    parse_directives,
    validate_directive,
    validate_instruction_step,
)


class TestParseDirectives:
    """Tests for parse_directives function."""

    def test_parse_delegate_directive(self):
        content = "DELEGATE @developer WHEN fix, code, implement"
        directives = parse_directives(content)
        assert len(directives) == 1
        assert directives[0].type == "DELEGATE"
        assert directives[0].content == "DELEGATE @developer WHEN fix, code, implement"

    def test_parse_default_directive(self):
        content = "DEFAULT @orchestrator"
        directives = parse_directives(content)
        assert len(directives) == 1
        assert directives[0].type == "DEFAULT"

    def test_parse_chain_directive(self):
        content = "CHAIN implementation: @doc-explorer → @developer → @verifier"
        directives = parse_directives(content)
        assert len(directives) == 1
        assert directives[0].type == "CHAIN"

    def test_parse_require_directive(self):
        content = "REQUIRE agents/orchestrator.md ON session_start"
        directives = parse_directives(content)
        assert len(directives) == 1
        assert directives[0].type == "REQUIRE"

    def test_parse_multiple_directives(self):
        content = """DELEGATE @developer WHEN fix, code
DEFAULT @orchestrator
CHAIN impl: @a → @b → @c
REQUIRE file.md ON session_start"""
        directives = parse_directives(content)
        assert len(directives) == 4
        assert directives[0].type == "DELEGATE"
        assert directives[1].type == "DEFAULT"
        assert directives[2].type == "CHAIN"
        assert directives[3].type == "REQUIRE"

    def test_skip_comments(self):
        content = """# This is a comment
DELEGATE @developer WHEN fix
# Another comment"""
        directives = parse_directives(content)
        assert len(directives) == 1

    def test_skip_empty_lines(self):
        content = """
DELEGATE @developer WHEN fix

DEFAULT @orchestrator
"""
        directives = parse_directives(content)
        assert len(directives) == 2


class TestValidateDirective:
    """Tests for validate_directive function."""

    @pytest.fixture
    def config(self):
        return DirectiveConfig()

    def test_valid_delegate(self, config):
        is_valid, error = validate_directive(
            "DELEGATE @developer WHEN fix, code", config
        )
        assert is_valid is True
        assert error == ""

    def test_valid_default(self, config):
        is_valid, error = validate_directive("DEFAULT @orchestrator", config)
        assert is_valid is True
        assert error == ""

    def test_valid_chain(self, config):
        is_valid, error = validate_directive("CHAIN impl: @a → @b → @c", config)
        assert is_valid is True
        assert error == ""

    def test_valid_require(self, config):
        is_valid, error = validate_directive("REQUIRE file.md ON session_start", config)
        assert is_valid is True
        assert error == ""

    def test_invalid_lowercase_delegate(self, config):
        is_valid, error = validate_directive("delegate @developer WHEN fix", config)
        assert is_valid is False
        assert "Unknown directive keyword" in error

    def test_invalid_delegate_missing_when(self, config):
        is_valid, error = validate_directive("DELEGATE @developer fix, code", config)
        assert is_valid is False
        assert "Invalid DELEGATE syntax" in error

    def test_invalid_default_missing_agent(self, config):
        is_valid, error = validate_directive("DEFAULT", config)
        assert is_valid is False
        assert "Invalid DEFAULT syntax" in error

    def test_invalid_chain_missing_arrow(self, config):
        is_valid, error = validate_directive("CHAIN impl: @a @b @c", config)
        assert is_valid is False
        assert "Invalid CHAIN syntax" in error

    def test_unknown_directive(self, config):
        is_valid, error = validate_directive("UNKNOWN @something", config)
        assert is_valid is False
        assert "Unknown directive keyword" in error


class TestValidateInstructionStep:
    """Tests for validate_instruction_step function."""

    @pytest.fixture
    def config(self):
        return InstructionConfig()

    def test_valid_route_step(self, config):
        is_valid, error = validate_instruction_step("1. ROUTE request to agent", config)
        assert is_valid is True
        assert error == ""

    def test_valid_delegate_step(self, config):
        is_valid, error = validate_instruction_step(
            "2. DELEGATE task to specialist", config
        )
        assert is_valid is True
        assert error == ""

    def test_valid_verify_step(self, config):
        is_valid, error = validate_instruction_step("3. VERIFY code changes", config)
        assert is_valid is True
        assert error == ""

    def test_invalid_step_lowercase_keyword(self, config):
        is_valid, error = validate_instruction_step("1. route request to agent", config)
        assert is_valid is False
        assert "Instruction step must start with an action keyword" in error

    def test_invalid_step_unknown_keyword(self, config):
        is_valid, error = validate_instruction_step("1. Do something", config)
        assert is_valid is False
        assert "Instruction step must start with an action keyword" in error

    def test_invalid_step_keyword_not_first(self, config):
        is_valid, error = validate_instruction_step("1. Then ROUTE request", config)
        assert is_valid is False
        assert "Instruction step must start with an action keyword" in error

    def test_non_numbered_line_skipped(self, config):
        is_valid, error = validate_instruction_step("Some text without number", config)
        assert is_valid is True
        assert error == ""

    def test_enforce_actions_disabled(self):
        config = InstructionConfig(enforce_actions=False)
        is_valid, error = validate_instruction_step("1. do something invalid", config)
        assert is_valid is True


class TestExtractInstructionSteps:
    """Tests for extract_instruction_steps function."""

    def test_extract_numbered_steps(self):
        content = """1. ROUTE request
2. DELEGATE task
3. VERIFY result"""
        steps = extract_instruction_steps(content)
        assert len(steps) == 3
        assert steps[0][0] == "1. ROUTE request"
        assert steps[1][0] == "2. DELEGATE task"
        assert steps[2][0] == "3. VERIFY result"

    def test_extract_with_non_numbered_lines(self):
        content = """Introduction text
1. ROUTE request
Some description
2. DELEGATE task"""
        steps = extract_instruction_steps(content)
        assert len(steps) == 2

    def test_line_numbers(self):
        content = """1. ROUTE request
2. DELEGATE task"""
        steps = extract_instruction_steps(content)
        assert steps[0][1] == 1  # line 1
        assert steps[1][1] == 2  # line 2

    def test_empty_content(self):
        steps = extract_instruction_steps("")
        assert len(steps) == 0
