"""Base type for domain events that modules publish to each other."""

from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field, computed_field

from heimdall.shared.ids import InstallationId


def _utc_now() -> datetime:
    return datetime.now(UTC)


class DomainEvent(BaseModel):
    """Something that happened in one tenant; subclass it per event.

    Attributes:
        installation_id: The tenant the event belongs to.
        occurred_at: When the event happened, in UTC.
    """

    model_config = ConfigDict(frozen=True)

    installation_id: InstallationId
    occurred_at: datetime = Field(default_factory=_utc_now)

    @computed_field
    @property
    def name(self) -> str:
        """The event's type name, for example ``PrOpened``."""
        return type(self).__name__
