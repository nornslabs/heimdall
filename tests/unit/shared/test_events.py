from datetime import UTC

import pytest
from pydantic import ValidationError

from heimdall.shared.events import DomainEvent
from heimdall.shared.ids import InstallationId


class PrOpened(DomainEvent):
    number: int


def test_domain_event_is_frozen_and_timestamped_in_utc() -> None:
    event = PrOpened(installation_id=InstallationId(3), number=9)

    assert event.name == "PrOpened"
    assert event.occurred_at.tzinfo == UTC
    with pytest.raises(ValidationError):
        event.number = 10
