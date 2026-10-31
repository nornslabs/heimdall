"""Structured JSON logging with tenant ids bound and secrets redacted."""

import logging
import sys
from collections.abc import MutableMapping

import structlog

from heimdall.shared.context import PrRef, TenantCtx
from heimdall.shared.settings import LogLevel

REDACTED = "[redacted]"
SENSITIVE_KEY_PARTS = ("token", "secret", "private_key", "password", "diff", "authorization")


def _redact_sensitive(
    _logger: object, _method: str, event_dict: MutableMapping[str, object]
) -> MutableMapping[str, object]:
    """Replace values whose key looks sensitive, so tokens and diffs never reach logs."""
    return {
        key: REDACTED if any(part in key.lower() for part in SENSITIVE_KEY_PARTS) else value
        for key, value in event_dict.items()
    }


def configure_logging(level: LogLevel) -> None:
    """Set up structlog to write one JSON object per line to stdout.

    Call once at process start, from ``apps/*/main.py``.

    Args:
        level: Minimum level name to log, for example ``"INFO"``.
    """
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            _redact_sensitive,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.getLevelNamesMapping()[level]),
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        cache_logger_on_first_use=False,
    )


def bind_tenant(ctx: TenantCtx, pr: PrRef | None = None) -> None:
    """Attach tenant ids to every log line written in the current task.

    Args:
        ctx: Supplies installation_id and request_id.
        pr: The PR being worked on, if any; adds repo_id and pr_number.
    """
    structlog.contextvars.bind_contextvars(
        installation_id=ctx.installation_id, request_id=ctx.request_id
    )
    if pr is not None:
        structlog.contextvars.bind_contextvars(repo_id=pr.repo_id, pr_number=pr.number)


def get_logger(name: str) -> structlog.typing.FilteringBoundLogger:
    """Get a logger tagged with the calling module's name.

    Args:
        name: Usually ``__name__``.

    Returns:
        A structlog bound logger.
    """
    return structlog.get_logger(logger_name=name)
