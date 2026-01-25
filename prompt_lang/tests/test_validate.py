"""Tests for the CLI validation tool."""

import sys
from io import StringIO
from pathlib import Path

import pytest

from prompt_lang.config import load_config
from prompt_lang.validate import (
    EXIT_CONFIG_ERROR,
    EXIT_FILE_NOT_FOUND,
    EXIT_SUCCESS,
    EXIT_VALIDATION_ERROR,
    main,
    parse_args,
    print_results,
    validate_directory,
    validate_file,
)

# Test fixtures directory
FIXTURES_DIR = Path(__file__).parent / "fixtures"
VALID_DIR = FIXTURES_DIR / "valid"
INVALID_DIR = FIXTURES_DIR / "invalid"


class TestParseArgs:
    """Tests for argument parsing."""

    def test_parse_single_file(self):
        """Parse single file argument."""
        args = parse_args(["path/to/file.md"])
        assert args.path == "path/to/file.md"
        assert args.config is None
        assert args.no_semantic is False
        assert args.verbose is False

    def test_parse_with_config(self):
        """Parse with custom config."""
        args = parse_args(["file.md", "--config", "custom.yaml"])
        assert args.config == "custom.yaml"

    def test_parse_short_config(self):
        """Parse with short config flag."""
        args = parse_args(["file.md", "-c", "custom.yaml"])
        assert args.config == "custom.yaml"

    def test_parse_no_semantic(self):
        """Parse with --no-semantic flag."""
        args = parse_args(["file.md", "--no-semantic"])
        assert args.no_semantic is True

    def test_parse_verbose(self):
        """Parse with verbose flag."""
        args = parse_args(["file.md", "-v"])
        assert args.verbose is True

    def test_parse_all_options(self):
        """Parse with all options."""
        args = parse_args(
            ["path/to/dir/", "--config", "my-config.yaml", "--no-semantic", "-v"]
        )
        assert args.path == "path/to/dir/"
        assert args.config == "my-config.yaml"
        assert args.no_semantic is True
        assert args.verbose is True


class TestValidateFile:
    """Tests for single file validation."""

    def test_validate_valid_file(self):
        """Valid file should pass."""
        config = load_config()
        result = validate_file(VALID_DIR / "minimal.md", config)

        assert result.passed
        assert len(result.errors) == 0

    def test_validate_invalid_file(self):
        """Invalid file should fail."""
        config = load_config()
        result = validate_file(INVALID_DIR / "missing-purpose.md", config)

        assert not result.passed
        assert len(result.errors) > 0

    def test_validate_with_semantic_errors(self):
        """File with ambiguous language should fail."""
        config = load_config()
        result = validate_file(INVALID_DIR / "ambiguous-language.md", config)

        assert not result.passed
        assert any("ambiguous" in e.message.lower() for e in result.errors)

    def test_validate_skip_semantic(self):
        """Skipping semantic check should not report ambiguous language."""
        config = load_config()
        config.validation.semantic_check = False
        result = validate_file(INVALID_DIR / "ambiguous-language.md", config)

        # Should still pass structural checks
        # (ambiguous-language.md has valid structure)
        assert result.passed


class TestValidateDirectory:
    """Tests for directory validation."""

    def test_validate_valid_directory(self):
        """All files in valid directory should pass."""
        config = load_config()
        results = validate_directory(VALID_DIR, config)

        assert len(results) == 3  # minimal.md, full.md, deploy-service.md
        assert all(r.passed for r in results)

    def test_validate_invalid_directory(self):
        """All files in invalid directory should fail."""
        config = load_config()
        results = validate_directory(INVALID_DIR, config)

        assert len(results) == 8  # 8 invalid fixtures
        assert all(not r.passed for r in results)

    def test_validate_mixed_directory(self):
        """Validate entire fixtures directory."""
        config = load_config()
        results = validate_directory(FIXTURES_DIR, config)

        passed = [r for r in results if r.passed]
        failed = [r for r in results if not r.passed]

        assert len(passed) == 3  # 3 valid
        assert len(failed) == 8  # 8 invalid


class TestMainCLI:
    """Tests for main CLI entry point."""

    def test_main_valid_file_returns_success(self):
        """Valid file should return EXIT_SUCCESS."""
        exit_code = main([str(VALID_DIR / "minimal.md")])
        assert exit_code == EXIT_SUCCESS

    def test_main_invalid_file_returns_error(self):
        """Invalid file should return EXIT_VALIDATION_ERROR."""
        exit_code = main([str(INVALID_DIR / "missing-purpose.md")])
        assert exit_code == EXIT_VALIDATION_ERROR

    def test_main_nonexistent_file_returns_not_found(self):
        """Nonexistent file should return EXIT_FILE_NOT_FOUND."""
        exit_code = main(["nonexistent/path/file.md"])
        assert exit_code == EXIT_FILE_NOT_FOUND

    def test_main_valid_directory_returns_success(self):
        """Valid directory should return EXIT_SUCCESS."""
        exit_code = main([str(VALID_DIR)])
        assert exit_code == EXIT_SUCCESS

    def test_main_invalid_directory_returns_error(self):
        """Invalid directory should return EXIT_VALIDATION_ERROR."""
        exit_code = main([str(INVALID_DIR)])
        assert exit_code == EXIT_VALIDATION_ERROR

    def test_main_with_no_semantic(self):
        """--no-semantic should skip semantic checks."""
        # ambiguous-language.md has valid structure but fails semantic
        exit_code = main([str(INVALID_DIR / "ambiguous-language.md"), "--no-semantic"])
        assert exit_code == EXIT_SUCCESS

    def test_main_with_verbose(self, capsys):
        """Verbose mode should show passing files."""
        exit_code = main([str(VALID_DIR / "minimal.md"), "-v"])

        captured = capsys.readouterr()
        assert "PASS:" in captured.out
        assert exit_code == EXIT_SUCCESS


class TestPrintResults:
    """Tests for result printing."""

    def test_print_all_passed(self, capsys):
        """Print summary when all pass."""
        config = load_config()
        results = validate_directory(VALID_DIR, config)

        all_passed = print_results(results, verbose=False)

        assert all_passed
        captured = capsys.readouterr()
        assert "All 3 file(s) passed" in captured.out

    def test_print_with_failures(self, capsys):
        """Print failures."""
        config = load_config()
        results = validate_directory(INVALID_DIR, config)

        all_passed = print_results(results, verbose=False)

        assert not all_passed
        captured = capsys.readouterr()
        assert "FAIL:" in captured.out
        assert "ERRORS:" in captured.out

    def test_print_verbose_shows_passing(self, capsys):
        """Verbose mode shows passing files."""
        config = load_config()
        results = validate_directory(VALID_DIR, config)

        print_results(results, verbose=True)

        captured = capsys.readouterr()
        assert "PASS:" in captured.out


class TestExitCodes:
    """Tests for exit codes."""

    def test_exit_codes_defined(self):
        """Exit codes should be defined correctly."""
        assert EXIT_SUCCESS == 0
        assert EXIT_VALIDATION_ERROR == 1
        assert EXIT_CONFIG_ERROR == 2
        assert EXIT_FILE_NOT_FOUND == 3


class TestEdgeCases:
    """Tests for edge cases."""

    def test_empty_directory(self, tmp_path):
        """Empty directory should pass (no files to validate)."""
        config = load_config()
        results = validate_directory(tmp_path, config)

        assert len(results) == 0

    def test_directory_with_non_md_files(self, tmp_path):
        """Non-.md files should be ignored."""
        # Create some non-md files
        (tmp_path / "readme.txt").write_text("Hello")
        (tmp_path / "script.py").write_text("print('hello')")

        config = load_config()
        results = validate_directory(tmp_path, config)

        assert len(results) == 0

    def test_nested_directory_structure(self, tmp_path):
        """Validate files in nested directories."""
        # Create nested structure
        subdir = tmp_path / "subdir"
        subdir.mkdir()

        # Create valid file in root
        (tmp_path / "root.md").write_text("""---
name: root
description: Root file
---

# Root

<purpose>Test</purpose>
<instructions>1. EXECUTE the task</instructions>
""")

        # Create valid file in subdir
        (subdir / "nested.md").write_text("""---
name: nested
description: Nested file
---

# Nested

<purpose>Test</purpose>
<instructions>1. EXECUTE the task</instructions>
""")

        config = load_config()
        results = validate_directory(tmp_path, config)

        assert len(results) == 2
        assert all(r.passed for r in results)
