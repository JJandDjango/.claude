"""Configuration loader for prompt validation."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class TokenConfig:
    """Token limit configuration."""

    warn_at: int = 2000
    fail_at: int = 4000


@dataclass
class FrontmatterConfig:
    """Frontmatter field requirements."""

    required: list[str] = field(default_factory=lambda: ["name", "description"])
    optional: list[str] = field(
        default_factory=lambda: ["model", "argument-hint", "tools"]
    )


@dataclass
class DirectiveConfig:
    """Directive syntax configuration for routing rules."""

    keywords: list[str] = field(
        default_factory=lambda: ["DELEGATE", "DEFAULT", "CHAIN", "REQUIRE"]
    )
    patterns: dict[str, str] = field(
        default_factory=lambda: {
            "DELEGATE": r"^DELEGATE @[\w-]+ WHEN [\w, -]+$",
            "DEFAULT": r"^DEFAULT @[\w-]+$",
            "CHAIN": r"^CHAIN [\w-]+: @[\w-]+( → @[\w-]+)+$",
            "REQUIRE": r"^REQUIRE \S+ ON \w+$",
        }
    )


@dataclass
class InstructionConfig:
    """Instruction action keyword enforcement configuration."""

    enforce_actions: bool = True
    action_keywords: list[str] = field(
        default_factory=lambda: [
            "ROUTE",
            "LOAD",
            "DELEGATE",
            "VERIFY",
            "EXECUTE",
            "SYNTHESIZE",
            "REPORT",
            "PARSE",
            "CHECK",
        ]
    )


@dataclass
class FileRule:
    """File-specific tag requirements based on path patterns."""

    pattern: str
    required_tags: list[str] = field(default_factory=list)
    forbidden_tags: list[str] = field(default_factory=list)
    skip_frontmatter: bool = False
    skip_required_tags: bool = False


@dataclass
class ValidationConfig:
    """Complete validation configuration."""

    tokens: TokenConfig = field(default_factory=TokenConfig)
    semantic_check: bool = True
    required_tags: list[str] = field(
        default_factory=lambda: ["purpose", "instructions"]
    )
    optional_tags: list[str] = field(
        default_factory=lambda: [
            "variables",
            "context",
            "constraints",
            "examples",
            "output",
            "criteria",
            "routing",
            "directives",
        ]
    )
    ambiguous_patterns: list[str] = field(
        default_factory=lambda: [
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
    )
    frontmatter: FrontmatterConfig = field(default_factory=FrontmatterConfig)
    enforce_tag_order: bool = False
    tag_order: list[str] = field(default_factory=list)
    directives: DirectiveConfig = field(default_factory=DirectiveConfig)
    instructions: InstructionConfig = field(default_factory=InstructionConfig)

    @property
    def all_tags(self) -> list[str]:
        """Return all recognized tags (required + optional)."""
        return self.required_tags + self.optional_tags


@dataclass
class Config:
    """Root configuration object."""

    validation: ValidationConfig = field(default_factory=ValidationConfig)
    file_rules: list[FileRule] = field(default_factory=list)


def load_config(config_path: Path | str | None = None) -> Config:
    """Load configuration from YAML file.

    Args:
        config_path: Path to config file. If None, looks for
            'prompt-lang.config.yaml' in the prompt_lang package directory.

    Returns:
        Config object with loaded or default values.
    """
    if config_path is None:
        config_path = Path(__file__).parent / "prompt-lang.config.yaml"
    else:
        config_path = Path(config_path)

    if not config_path.exists():
        return Config()

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except (yaml.YAMLError, OSError):
        return Config()

    if not data:
        return Config()

    return _parse_config(data)


def _parse_config(data: dict[str, Any]) -> Config:
    """Parse raw YAML data into Config object."""
    v = data.get("validation", {})

    # Parse tokens
    tokens_data = v.get("tokens", {})
    tokens = TokenConfig(
        warn_at=tokens_data.get("warn_at", 2000),
        fail_at=tokens_data.get("fail_at", 4000),
    )

    # Parse frontmatter
    fm_data = v.get("frontmatter", {})
    frontmatter = FrontmatterConfig(
        required=fm_data.get("required", ["name", "description"]),
        optional=fm_data.get("optional", ["model", "argument-hint", "tools"]),
    )

    # Parse directives from top-level (not nested under validation)
    dir_data = data.get("directives", {})
    directives = DirectiveConfig(
        keywords=dir_data.get("keywords", ["DELEGATE", "DEFAULT", "CHAIN", "REQUIRE"]),
        patterns=dir_data.get(
            "patterns",
            {
                "DELEGATE": r"^DELEGATE @[\w-]+ WHEN [\w, -]+$",
                "DEFAULT": r"^DEFAULT @[\w-]+$",
                "CHAIN": r"^CHAIN [\w-]+: @[\w-]+( → @[\w-]+)+$",
                "REQUIRE": r"^REQUIRE \S+ ON \w+$",
            },
        ),
    )

    # Parse instructions from top-level (not nested under validation)
    inst_data = data.get("instructions", {})
    instructions = InstructionConfig(
        enforce_actions=inst_data.get("enforce_actions", True),
        action_keywords=inst_data.get(
            "action_keywords",
            [
                "ROUTE",
                "LOAD",
                "DELEGATE",
                "VERIFY",
                "EXECUTE",
                "SYNTHESIZE",
                "REPORT",
                "PARSE",
                "CHECK",
            ],
        ),
    )

    # Parse validation config
    validation = ValidationConfig(
        tokens=tokens,
        semantic_check=v.get("semantic_check", True),
        required_tags=v.get("required_tags", ["purpose", "instructions"]),
        optional_tags=v.get(
            "optional_tags",
            [
                "variables",
                "context",
                "constraints",
                "examples",
                "output",
                "criteria",
                "routing",
                "directives",
            ],
        ),
        ambiguous_patterns=v.get(
            "ambiguous_patterns",
            [
                "maybe",
                "might",
                "consider",
                "optionally",
                "try to",
                "possibly",
                "it would be good to",
                "you could",
                "perhaps",
            ],
        ),
        frontmatter=frontmatter,
        enforce_tag_order=v.get("enforce_tag_order", False),
        tag_order=v.get("tag_order", []),
        directives=directives,
        instructions=instructions,
    )

    # Parse file rules from top-level
    file_rules_data = data.get("file_rules", [])
    file_rules = [
        FileRule(
            pattern=rule.get("pattern", ""),
            required_tags=rule.get("required_tags", []),
            forbidden_tags=rule.get("forbidden_tags", []),
        )
        for rule in file_rules_data
    ]

    return Config(validation=validation, file_rules=file_rules)
