import pytest

from heimdall.shared import errors

RETRYABLE: list[type[errors.HeimdallError]] = [errors.GitHubUnavailable, errors.SwitchUnavailable]
PERMANENT: list[type[errors.HeimdallError]] = [
    errors.NotAMaintainer,
    errors.DraftChanged,
    errors.ConfigInvalid,
    errors.RepoLimitReached,
    errors.StaleHeadSha,
    errors.ToolNotAllowed,
]


@pytest.mark.parametrize("error_type", [*RETRYABLE, *PERMANENT])
def test_all_errors_subclass_heimdall_error(error_type: type[errors.HeimdallError]) -> None:
    assert issubclass(error_type, errors.HeimdallError)


@pytest.mark.parametrize("error_type", RETRYABLE)
def test_outage_errors_are_retryable(error_type: type[errors.HeimdallError]) -> None:
    assert error_type("down").retryable is True


@pytest.mark.parametrize("error_type", PERMANENT)
def test_rule_errors_are_not_retryable(error_type: type[errors.HeimdallError]) -> None:
    assert error_type("no").retryable is False


def test_error_keeps_its_message() -> None:
    assert str(errors.DraftChanged("hash mismatch")) == "hash mismatch"
