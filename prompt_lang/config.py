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
            "workflow",
            "constraints",
            "examples",
            "output",
            "criteria",
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

    @property
    def all_tags(self) -> list[str]:
        """Return all recognized tags (required + optional)."""
        return self.required_tags + self.optional_tags


@dataclass
class Config:
    """Root configuration object."""

    validation: ValidationConfig = field(default_factory=ValidationConfig)


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

    if not data or "validation" not in data:
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
                "workflow",
                "constraints",
                "examples",
                "output",
                "criteria",
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
    )

    return Config(validation=validation)
