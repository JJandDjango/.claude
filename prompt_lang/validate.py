"""CLI for prompt file validation.

Usage:
    python -m prompt_lang.validate path/to/file.md
    python -m prompt_lang.validate path/to/directory/
    python -m prompt_lang.validate path/to/file.md --config custom.yaml
    python -m prompt_lang.validate path/to/file.md --no-semantic
    python -m prompt_lang.validate path/to/file.md -v
"""

import argparse
import sys
from pathlib import Path

from .config import Config, load_config
from .errors import ValidationResult
from .parser import parse_content, parse_file
from .semantic import validate_semantic

# Exit codes
EXIT_SUCCESS = 0
EXIT_VALIDATION_ERROR = 1
EXIT_CONFIG_ERROR = 2
EXIT_FILE_NOT_FOUND = 3


def main(argv: list[str] | None = None) -> int:
    """Main entry point for CLI.

    Args:
        argv: Command line arguments. If None, uses sys.argv.

    Returns:
        Exit code (0 for success, non-zero for errors).
    """
    args = parse_args(argv)

    # Load configuration
    try:
        config = load_config(args.config)
    except Exception as e:
        print(f"Error loading config: {e}", file=sys.stderr)
        return EXIT_CONFIG_ERROR

    # Override semantic check if --no-semantic
    if args.no_semantic:
        config.validation.semantic_check = False

    # Resolve path
    path = Path(args.path)
    if not path.exists():
        print(f"Error: Path not found: {path}", file=sys.stderr)
        return EXIT_FILE_NOT_FOUND

    # Validate file(s)
    if path.is_file():
        results = [validate_file(path, config)]
    else:
        results = validate_directory(path, config)

    # Print results
    all_passed = print_results(results, verbose=args.verbose)

    return EXIT_SUCCESS if all_passed else EXIT_VALIDATION_ERROR


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command line arguments.

    Args:
        argv: Command line arguments.

    Returns:
        Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        prog="prompt_lang.validate",
        description="Validate prompt files against the Prompt Programming Language specification.",
        epilog="Exit codes: 0=success, 1=validation errors, 2=config error, 3=file not found",
    )

    parser.add_argument(
        "path",
        type=str,
        help="Path to a prompt file (.md) or directory to validate",
    )

    parser.add_argument(
        "--config",
        "-c",
        type=str,
        default=None,
        help="Path to config file (default: prompt-lang.config.yaml)",
    )

    parser.add_argument(
        "--no-semantic",
        action="store_true",
        help="Skip semantic validation (ambiguous language detection)",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Verbose output (show passing files)",
    )

    return parser.parse_args(argv)


def validate_file(file_path: Path, config: Config) -> ValidationResult:
    """Validate a single prompt file.

    Args:
        file_path: Path to the prompt file.
        config: Configuration object.

    Returns:
        ValidationResult for the file.
    """
    # Parse and validate structure
    parsed, result = parse_file(file_path, config)

    # Run semantic validation
    validate_semantic(parsed, result, config)

    return result


def validate_directory(dir_path: Path, config: Config) -> list[ValidationResult]:
    """Validate all prompt files in a directory.

    Args:
        dir_path: Path to the directory.
        config: Configuration object.

    Returns:
        List of ValidationResult objects.
    """
    results: list[ValidationResult] = []

    # Find all .md files recursively
    for file_path in sorted(dir_path.rglob("*.md")):
        results.append(validate_file(file_path, config))

    return results


def print_results(results: list[ValidationResult], verbose: bool = False) -> bool:
    """Print validation results.

    Args:
        results: List of validation results.
        verbose: Whether to show passing files.

    Returns:
        True if all files passed, False otherwise.
    """
    passed_count = 0
    failed_count = 0

    for result in results:
        if result.passed:
            passed_count += 1
            if verbose:
                print(f"PASS: {result.file_path}")
        else:
            failed_count += 1
            print_failure(result)

    # Print summary
    print()
    print("=" * 60)
    total = passed_count + failed_count
    if failed_count == 0:
        print(f"All {total} file(s) passed validation.")
    else:
        print(f"Validation complete: {passed_count} passed, {failed_count} failed")

    return failed_count == 0


def print_failure(result: ValidationResult) -> None:
    """Print a failed validation result.

    Args:
        result: The failed validation result.
    """
    print()
    print(f"FAIL: {result.file_path}")
    print("-" * 60)

    if result.errors:
        print("ERRORS:")
        for error in result.errors:
            print(f"  Line {error.line}: {error.message}")

    if result.warnings:
        print("WARNINGS:")
        for warning in result.warnings:
            print(f"  Line {warning.line}: {warning.message}")

    print()
    print(f"Token count: {result.token_count}")
    print(
        f"Result: FAIL ({len(result.errors)} errors, {len(result.warnings)} warnings)"
    )


if __name__ == "__main__":
    sys.exit(main())
