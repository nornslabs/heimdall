import json
from collections.abc import Iterator

import pytest
import structlog

from heimdall.shared.context import PrRef, TenantCtx
from heimdall.shared.ids import InstallationId, RepoId
from heimdall.shared.logging import REDACTED, bind_tenant, configure_logging, get_logger


@pytest.fixture(autouse=True)
def _clean_context() -> Iterator[None]:
    structlog.contextvars.clear_contextvars()
    yield
    structlog.contextvars.clear_contextvars()


def _last_json_line(capsys: pytest.CaptureFixture[str]) -> dict[str, object]:
    lines = capsys.readouterr().out.strip().splitlines()
    return json.loads(lines[-1])


def test_log_line_is_json_with_bound_installation_id(capsys: pytest.CaptureFixture[str]) -> None:
    configure_logging("INFO")
    ctx = TenantCtx(installation_id=InstallationId(11), request_id="req-9")
    bind_tenant(ctx, PrRef(repo_id=RepoId(5), number=77))

    get_logger("test").info("intake_started")

    line = _last_json_line(capsys)
    assert line["event"] == "intake_started"
    assert line["installation_id"] == 11
    assert line["request_id"] == "req-9"
    assert line["pr_number"] == 77
    assert line["level"] == "info"


def test_redacts_token_and_diff_fields(capsys: pytest.CaptureFixture[str]) -> None:
    configure_logging("INFO")

    get_logger("test").info("call", access_token="ghs_abc", diff="+evil", pr_id=3)

    line = _last_json_line(capsys)
    assert line["access_token"] == REDACTED
    assert line["diff"] == REDACTED
    assert line["pr_id"] == 3


def test_respects_log_level(capsys: pytest.CaptureFixture[str]) -> None:
    configure_logging("WARNING")

    get_logger("test").info("quiet")

    assert capsys.readouterr().out == ""
