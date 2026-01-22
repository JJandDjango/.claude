"""Error and result classes for prompt validation."""

from dataclasses import dataclass, field
from typing import Literal


@dataclass
class ValidationError:
    """A single validation error or warning."""

    line: int
    message: str
    severity: Literal["error", "warning"]

    def __str__(self) -> str:
        prefix = "ERROR" if self.severity == "error" else "WARNING"
        return f"  Line {self.line}: {self.message}"


@dataclass
class ValidationResult:
    """Result of validating a prompt file."""

    file_path: str
    errors: list[ValidationError] = field(default_factory=list)
    warnings: list[ValidationError] = field(default_factory=list)
    token_count: int = 0

    @property
    def passed(self) -> bool:
        """Returns True if no errors were found."""
        return len(self.errors) == 0

    def add_error(self, line: int, message: str) -> None:
        """Add an error to the result."""
        self.errors.append(ValidationError(line, message, "error"))

    def add_warning(self, line: int, message: str) -> None:
        """Add a warning to the result."""
        self.warnings.append(ValidationError(line, message, "warning"))

    def __str__(self) -> str:
        lines = [f"Validating: {self.file_path}", ""]

        if self.errors:
            lines.append("ERRORS:")
            for err in self.errors:
                lines.append(str(err))
            lines.append("")

        if self.warnings:
            lines.append("WARNINGS:")
            for warn in self.warnings:
                lines.append(str(warn))
            lines.append("")

        status = "PASS" if self.passed else "FAIL"
        lines.append(
            f"Result: {status} ({len(self.errors)} errors, {len(self.warnings)} warnings)"
        )

        return "\n".join(lines)
