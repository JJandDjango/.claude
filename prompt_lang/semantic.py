"""Semantic validation for prompt files.

Performs LLM-assisted and pattern-based validation:
- Ambiguous language detection in <instructions>
- Pattern matching for known hedging phrases
- Optional LLM fallback for edge cases
"""

import re
from dataclasses import dataclass

from .config import Config, load_config
from .errors import ValidationResult
from .parser import ParsedPrompt, Tag


@dataclass
class AmbiguousMatch:
    """A detected ambiguous language pattern."""

    pattern: str
    line: int
    context: str  # The line containing the match


def check_ambiguous_language(
    parsed: ParsedPrompt,
    result: ValidationResult,
    config: Config | None = None,
) -> list[AmbiguousMatch]:
    """Check for ambiguous language in <instructions> tag.

    Args:
        parsed: Parsed prompt object.
        result: ValidationResult to populate with errors.
        config: Optional config object.

    Returns:
        List of AmbiguousMatch objects found.
    """
    if config is None:
        config = load_config()

    matches: list[AmbiguousMatch] = []

    # Get instructions tag
    instructions = parsed.get_tag("instructions")
    if instructions is None:
        return matches

    # Check for ambiguous patterns
    patterns = config.validation.ambiguous_patterns
    matches = _find_ambiguous_patterns(instructions, patterns)

    # Add errors for each match
    for match in matches:
        result.add_error(
            match.line, f'Ambiguous language in <instructions>: "{match.pattern}"'
        )

    return matches


def _find_ambiguous_patterns(tag: Tag, patterns: list[str]) -> list[AmbiguousMatch]:
    """Find ambiguous patterns in a tag's content.

    Args:
        tag: The tag to search.
        patterns: List of ambiguous patterns to match.

    Returns:
        List of AmbiguousMatch objects.
    """
    matches: list[AmbiguousMatch] = []
    lines = tag.content.split("\n")

    for i, line in enumerate(lines):
        line_number = tag.start_line + i
        line_lower = line.lower()

        for pattern in patterns:
            # Use word boundary matching to avoid false positives
            # e.g., "delivery" shouldn't match "maybe"
            regex = _pattern_to_regex(pattern)
            if regex.search(line_lower):
                matches.append(
                    AmbiguousMatch(
                        pattern=pattern,
                        line=line_number,
                        context=line.strip(),
                    )
                )

    return matches


def _pattern_to_regex(pattern: str) -> re.Pattern:
    """Convert an ambiguous pattern to a word-boundary regex.

    Args:
        pattern: The pattern string (e.g., "maybe", "try to").

    Returns:
        Compiled regex pattern.
    """
    # Escape special regex characters
    escaped = re.escape(pattern)
    # Add word boundaries
    return re.compile(rf"\b{escaped}\b", re.IGNORECASE)


def validate_semantic(
    parsed: ParsedPrompt,
    result: ValidationResult,
    config: Config | None = None,
    use_llm: bool = False,
) -> ValidationResult:
    """Run all semantic validation checks.

    Args:
        parsed: Parsed prompt object.
        result: ValidationResult to populate.
        config: Optional config object.
        use_llm: Whether to use LLM for additional checks (not implemented).

    Returns:
        Updated ValidationResult.
    """
    if config is None:
        config = load_config()

    # Skip semantic checks if disabled
    if not config.validation.semantic_check:
        return result

    # Check for ambiguous language
    check_ambiguous_language(parsed, result, config)

    # LLM fallback (placeholder for future implementation)
    if use_llm:
        _llm_semantic_check(parsed, result, config)

    return result


def _llm_semantic_check(
    parsed: ParsedPrompt,
    result: ValidationResult,
    config: Config,
) -> None:
    """Perform LLM-based semantic validation.

    This is a placeholder for future implementation.
    The LLM would check for:
    - Subtle ambiguity not caught by patterns
    - Logical inconsistencies
    - Unclear instructions

    Args:
        parsed: Parsed prompt object.
        result: ValidationResult to populate.
        config: Configuration object.
    """
    # TODO: Implement LLM-based semantic checking
    # This would use the anthropic client to analyze the prompt
    # for semantic issues not caught by pattern matching.
    #
    # Example implementation:
    # 1. Extract <instructions> content
    # 2. Send to Claude with a prompt asking to identify ambiguity
    # 3. Parse response and add warnings/errors
    #
    # For now, this is a no-op placeholder.
    pass
