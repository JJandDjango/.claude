"""Directive parsing and validation for routing rules."""

import re
from dataclasses import dataclass
from typing import Tuple

from .config import DirectiveConfig, InstructionConfig


@dataclass
class Directive:
    """Parsed directive from a directives block."""

    type: str  # DELEGATE, DEFAULT, CHAIN, REQUIRE
    content: str  # Full line content
    line_number: int


def parse_directives(content: str) -> list[Directive]:
    """Extract directive lines from content.

    Args:
        content: Content of a <directives> block.

    Returns:
        List of Directive objects.
    """
    directives = []
    lines = content.strip().split("\n")

    for i, line in enumerate(lines, start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Check if line starts with a known directive keyword
        for keyword in ["DELEGATE", "DEFAULT", "CHAIN", "REQUIRE"]:
            if line.startswith(keyword):
                directives.append(Directive(type=keyword, content=line, line_number=i))
                break

    return directives


def validate_directive(line: str, config: DirectiveConfig) -> Tuple[bool, str]:
    """Validate a directive line against patterns.

    Args:
        line: The directive line to validate.
        config: Directive configuration with patterns.

    Returns:
        Tuple of (is_valid, error_message). error_message is empty string if valid.
    """
    line = line.strip()

    # Find which directive type this is
    directive_type = None
    for keyword in config.keywords:
        if line.startswith(keyword):
            directive_type = keyword
            break

    if not directive_type:
        return (
            False,
            f"Unknown directive keyword. Expected one of: {', '.join(config.keywords)}",
        )

    # Get pattern for this directive type
    pattern = config.patterns.get(directive_type)
    if not pattern:
        return (
            False,
            f"No validation pattern found for directive type: {directive_type}",
        )

    # Validate against pattern
    if not re.match(pattern, line):
        return False, f"Invalid {directive_type} syntax. Expected pattern: {pattern}"

    return True, ""


def validate_instruction_step(line: str, config: InstructionConfig) -> Tuple[bool, str]:
    """Validate that an instruction step starts with an action keyword.

    Args:
        line: The instruction line to validate (e.g., "1. ROUTE to agent").
        config: Instruction configuration with action keywords.

    Returns:
        Tuple of (is_valid, error_message). error_message is empty string if valid.
    """
    if not config.enforce_actions:
        return True, ""

    line = line.strip()

    # Check if this is a numbered step
    step_match = re.match(r"^\d+\.\s+(.+)$", line)
    if not step_match:
        # Not a numbered step, skip validation
        return True, ""

    # Extract the content after the number
    content = step_match.group(1).strip()

    # Check if first word is an action keyword
    first_word = content.split()[0] if content.split() else ""

    if first_word not in config.action_keywords:
        return (
            False,
            f"Instruction step must start with an action keyword. "
            f"Found: '{first_word}', expected one of: {', '.join(config.action_keywords)}",
        )

    return True, ""


def extract_instruction_steps(content: str) -> list[Tuple[str, int]]:
    """Extract numbered instruction steps from content.

    Args:
        content: Content of an <instructions> block.

    Returns:
        List of tuples (line_content, line_number).
    """
    steps = []
    lines = content.strip().split("\n")

    for i, line in enumerate(lines, start=1):
        line = line.strip()
        if re.match(r"^\d+\.", line):
            steps.append((line, i))

    return steps
