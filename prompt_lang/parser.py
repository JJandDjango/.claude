"""Structural parser for prompt files.

Performs deterministic validation of:
- YAML frontmatter presence and required fields
- XML tag extraction and validation
- Nesting detection
- Token counting
"""

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

try:
    import tiktoken

    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False

from .config import Config, load_config
from .errors import ValidationResult

# Regex patterns
FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
OPEN_TAG_PATTERN = re.compile(r"<([a-z][a-z0-9-]*)>", re.IGNORECASE)
CLOSE_TAG_PATTERN = re.compile(r"</([a-z][a-z0-9-]*)>", re.IGNORECASE)
TAG_PAIR_PATTERN = re.compile(
    r"<([a-z][a-z0-9-]*)>(.*?)</\1>", re.DOTALL | re.IGNORECASE
)


@dataclass
class Tag:
    """Represents a parsed XML tag."""

    name: str
    content: str
    start_line: int
    end_line: int


@dataclass
class ParsedPrompt:
    """Result of parsing a prompt file."""

    frontmatter: dict | None = None
    frontmatter_end_line: int = 0
    tags: list[Tag] = field(default_factory=list)
    raw_content: str = ""

    def get_tag(self, name: str) -> Tag | None:
        """Get a tag by name."""
        for tag in self.tags:
            if tag.name.lower() == name.lower():
                return tag
        return None

    def has_tag(self, name: str) -> bool:
        """Check if a tag exists."""
        return self.get_tag(name) is not None


def parse_file(
    file_path: Path | str, config: Config | None = None
) -> tuple[ParsedPrompt, ValidationResult]:
    """Parse a prompt file and validate its structure.

    Args:
        file_path: Path to the prompt file.
        config: Optional config object. If None, loads from default location.

    Returns:
        Tuple of (ParsedPrompt, ValidationResult).
    """
    file_path = Path(file_path)
    result = ValidationResult(file_path=str(file_path))

    if config is None:
        config = load_config()

    # Read file content
    try:
        content = file_path.read_text(encoding="utf-8")
    except OSError as e:
        result.add_error(0, f"Failed to read file: {e}")
        return ParsedPrompt(), result

    return parse_content(content, result, config)


def parse_content(
    content: str, result: ValidationResult, config: Config
) -> tuple[ParsedPrompt, ValidationResult]:
    """Parse prompt content and validate structure.

    Args:
        content: Raw file content.
        result: ValidationResult to populate.
        config: Configuration object.

    Returns:
        Tuple of (ParsedPrompt, ValidationResult).
    """
    parsed = ParsedPrompt(raw_content=content)
    lines = content.split("\n")

    # Step 1: Parse and validate frontmatter
    parsed.frontmatter, parsed.frontmatter_end_line = _parse_frontmatter(
        content, lines, result, config
    )

    # Step 2: Check for reference flag - skip further validation if set
    if parsed.frontmatter and parsed.frontmatter.get("reference") is True:
        result.token_count = _count_tokens(content)
        return parsed, result

    # Step 3: Extract and validate tags
    body_start = parsed.frontmatter_end_line
    body_content = "\n".join(lines[body_start:])
    parsed.tags = _extract_tags(body_content, body_start, lines, result, config)

    # Step 4: Check for nesting violations
    _check_nesting(body_content, body_start, lines, result, config)

    # Step 5: Check required tags
    _check_required_tags(parsed, result, config)

    # Step 6: Check tag order
    _check_tag_order(parsed, result, config)

    # Step 7: Count tokens
    parsed_token_count = _count_tokens(content)
    result.token_count = parsed_token_count
    _check_token_limits(parsed_token_count, result, config)

    return parsed, result


def _parse_frontmatter(
    content: str,
    lines: list[str],
    result: ValidationResult,
    config: Config,
) -> tuple[dict | None, int]:
    """Parse YAML frontmatter from content.

    Returns:
        Tuple of (frontmatter dict or None, line number where body starts).
    """
    # Check if file starts with frontmatter delimiter
    if not content.startswith("---"):
        result.add_error(1, "Missing YAML frontmatter (file must start with '---')")
        return None, 0

    # Find frontmatter boundaries
    match = FRONTMATTER_PATTERN.match(content)
    if not match:
        result.add_error(1, "Malformed YAML frontmatter (missing closing '---')")
        return None, 0

    yaml_content = match.group(1)

    # Calculate end line of frontmatter
    frontmatter_text = match.group(0)
    end_line = frontmatter_text.count("\n")

    # Parse YAML
    try:
        frontmatter = yaml.safe_load(yaml_content)
    except yaml.YAMLError as e:
        result.add_error(1, f"Invalid YAML in frontmatter: {e}")
        return None, end_line

    if not isinstance(frontmatter, dict):
        result.add_error(1, "Frontmatter must be a YAML mapping")
        return None, end_line

    # Validate required fields
    for field_name in config.validation.frontmatter.required:
        if field_name not in frontmatter:
            result.add_error(1, f"Missing required frontmatter field: '{field_name}'")

    return frontmatter, end_line


def _extract_tags(
    body: str,
    body_start_line: int,
    all_lines: list[str],
    result: ValidationResult,
    config: Config,
) -> list[Tag]:
    """Extract XML tags from body content.

    Returns:
        List of Tag objects.
    """
    tags: list[Tag] = []
    recognized_tags = config.validation.all_tags

    # Find all opening tags
    open_tags: dict[str, list[int]] = {}  # tag_name -> [line_numbers]
    for i, line in enumerate(all_lines[body_start_line:], start=body_start_line + 1):
        for match in OPEN_TAG_PATTERN.finditer(line):
            tag_name = match.group(1).lower()
            if tag_name not in open_tags:
                open_tags[tag_name] = []
            open_tags[tag_name].append(i)

    # Find all closing tags
    close_tags: dict[str, list[int]] = {}  # tag_name -> [line_numbers]
    for i, line in enumerate(all_lines[body_start_line:], start=body_start_line + 1):
        for match in CLOSE_TAG_PATTERN.finditer(line):
            tag_name = match.group(1).lower()
            if tag_name not in close_tags:
                close_tags[tag_name] = []
            close_tags[tag_name].append(i)

    # Check for unrecognized tags
    all_found_tags = set(open_tags.keys()) | set(close_tags.keys())
    for tag_name in all_found_tags:
        if tag_name not in recognized_tags:
            line_num = (open_tags.get(tag_name, [0]) + close_tags.get(tag_name, [0]))[0]
            result.add_error(line_num, f"Unrecognized tag: <{tag_name}>")

    # Check for unclosed tags
    for tag_name, open_lines in open_tags.items():
        close_lines = close_tags.get(tag_name, [])
        if len(open_lines) > len(close_lines):
            for line_num in open_lines[len(close_lines) :]:
                result.add_error(line_num, f"Unclosed tag: <{tag_name}>")

    # Check for extra closing tags
    for tag_name, close_lines in close_tags.items():
        open_lines = open_tags.get(tag_name, [])
        if len(close_lines) > len(open_lines):
            for line_num in close_lines[len(open_lines) :]:
                result.add_error(line_num, f"Extra closing tag: </{tag_name}>")

    # Extract matched tag pairs with content
    for match in TAG_PAIR_PATTERN.finditer(body):
        tag_name = match.group(1).lower()
        tag_content = match.group(2)

        # Calculate line numbers
        start_pos = match.start()
        end_pos = match.end()
        start_line = body[:start_pos].count("\n") + body_start_line + 1
        end_line = body[:end_pos].count("\n") + body_start_line + 1

        tags.append(
            Tag(
                name=tag_name,
                content=tag_content.strip(),
                start_line=start_line,
                end_line=end_line,
            )
        )

    return tags


def _check_nesting(
    body: str,
    body_start_line: int,
    all_lines: list[str],
    result: ValidationResult,
    config: Config,
) -> None:
    """Check for illegally nested tags."""
    recognized_tags = config.validation.all_tags

    # Track open tags as we scan
    open_stack: list[tuple[str, int]] = []  # (tag_name, line_number)

    for i, line in enumerate(all_lines[body_start_line:], start=body_start_line + 1):
        # Process in order of appearance
        events: list[tuple[int, str, str]] = []  # (position, type, tag_name)

        for match in OPEN_TAG_PATTERN.finditer(line):
            tag_name = match.group(1).lower()
            if tag_name in recognized_tags:
                events.append((match.start(), "open", tag_name))

        for match in CLOSE_TAG_PATTERN.finditer(line):
            tag_name = match.group(1).lower()
            if tag_name in recognized_tags:
                events.append((match.start(), "close", tag_name))

        # Sort by position in line
        events.sort(key=lambda x: x[0])

        for _, event_type, tag_name in events:
            if event_type == "open":
                if open_stack:
                    parent_tag, parent_line = open_stack[-1]
                    result.add_error(
                        i,
                        f"Nested tag detected: <{tag_name}> inside <{parent_tag}> (opened at line {parent_line})",
                    )
                open_stack.append((tag_name, i))
            else:  # close
                if open_stack and open_stack[-1][0] == tag_name:
                    open_stack.pop()
                elif open_stack:
                    # Mismatched close tag
                    expected_tag, _ = open_stack[-1]
                    result.add_error(
                        i,
                        f"Mismatched closing tag: expected </{expected_tag}>, found </{tag_name}>",
                    )


def _check_required_tags(
    parsed: ParsedPrompt, result: ValidationResult, config: Config
) -> None:
    """Check that all required tags are present."""
    for tag_name in config.validation.required_tags:
        if not parsed.has_tag(tag_name):
            result.add_error(0, f"Missing required tag: <{tag_name}>")


def _check_tag_order(
    parsed: ParsedPrompt, result: ValidationResult, config: Config
) -> None:
    """Check that tags appear in the configured order.

    Only checks tags that are present in the document. Tags not in tag_order
    are ignored.
    """
    if not config.validation.enforce_tag_order:
        return

    tag_order = config.validation.tag_order
    if not tag_order:
        return

    # Get actual tag names in document order
    actual_tags = [tag.name.lower() for tag in parsed.tags]

    # Filter to only tags that are in the configured order
    actual_ordered = [t for t in actual_tags if t in tag_order]

    # Get expected order for tags that are present
    expected_ordered = [t for t in tag_order if t in actual_tags]

    # Compare
    if actual_ordered != expected_ordered:
        # Find the first out-of-order tag
        for i, actual_tag in enumerate(actual_ordered):
            if i >= len(expected_ordered) or actual_tag != expected_ordered[i]:
                # Find the tag object to get line number
                tag_obj = parsed.get_tag(actual_tag)
                line_num = tag_obj.start_line if tag_obj else 0

                # Determine what was expected
                if i < len(expected_ordered):
                    expected_tag = expected_ordered[i]
                    result.add_error(
                        line_num,
                        f"Tag <{actual_tag}> is out of order: expected <{expected_tag}> at this position",
                    )
                else:
                    result.add_error(
                        line_num,
                        f"Tag <{actual_tag}> is out of order",
                    )
                break


def _count_tokens(content: str) -> int:
    """Count tokens in content using tiktoken."""
    if not TIKTOKEN_AVAILABLE:
        # Fallback: rough estimate (1 token ≈ 4 chars)
        return len(content) // 4

    try:
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(content))
    except Exception:
        return len(content) // 4


def _check_token_limits(
    token_count: int, result: ValidationResult, config: Config
) -> None:
    """Check token count against configured limits."""
    tokens_config = config.validation.tokens

    if token_count >= tokens_config.fail_at:
        result.add_error(
            0,
            f"Token count ({token_count}) exceeds fail threshold ({tokens_config.fail_at})",
        )
    elif token_count >= tokens_config.warn_at:
        result.add_warning(
            0,
            f"Token count ({token_count}) exceeds warn threshold ({tokens_config.warn_at})",
        )
