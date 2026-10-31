"""Request and PR context values passed into every service function."""

import uuid
from dataclasses import dataclass

from heimdall.shared.ids import InstallationId, RepoId


@dataclass(frozen=True)
class TenantCtx:
    """Tenant and request context; every service call carries one.

    Attributes:
        installation_id: The GitHub App installation this request belongs to.
        request_id: Correlation id that ties log lines for one request together.
    """

    installation_id: InstallationId
    request_id: str


@dataclass(frozen=True)
class PrRef:
    """Points at one pull request inside a repository.

    Attributes:
        repo_id: GitHub repository id.
        number: Pull request number within that repository.

    Raises:
        ValueError: number is zero or negative.
    """

    repo_id: RepoId
    number: int

    def __post_init__(self) -> None:
        """Reject PR numbers GitHub would never issue."""
        if self.number < 1:
            raise ValueError(f"PR number must be positive, got {self.number}")


def new_request_id() -> str:
    """Make a fresh correlation id for a request or job.

    Returns:
        A random hex string, unique per call.
    """
    return uuid.uuid4().hex
