"""Typed ids so an installation id can't be passed where a repo id is expected."""

from typing import NewType

InstallationId = NewType("InstallationId", int)
"""GitHub App installation id; the tenant key on every table."""

RepoId = NewType("RepoId", int)
"""GitHub repository id."""

DraftId = NewType("DraftId", int)
"""A draft comment awaiting maintainer approval."""

ReproId = NewType("ReproId", int)
"""One reproduction run on GitHub Actions."""

FindingId = NewType("FindingId", int)
"""One review finding from Loki."""
