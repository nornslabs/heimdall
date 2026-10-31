import pytest

pytestmark = pytest.mark.e2e


@pytest.mark.skip(reason="E2E replay lands in HEI-73")
def test_seeded_prs_replay() -> None: ...
