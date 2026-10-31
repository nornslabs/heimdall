import pytest
from pydantic import ValidationError

from heimdall.shared.settings import Settings

REQUIRED_ENV = {
    "HEIMDALL_DATABASE_URL": "postgresql://heimdall:heimdall@localhost:5432/heimdall",
    "HEIMDALL_GITHUB_APP_ID": "12345",
    "HEIMDALL_GITHUB_PRIVATE_KEY_PATH": "/run/secrets/app.pem",
    "HEIMDALL_GITHUB_WEBHOOK_SECRET": "webhook-secret-value",
}


@pytest.fixture
def required_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for name, value in REQUIRED_ENV.items():
        monkeypatch.setenv(name, value)


@pytest.mark.usefixtures("required_env")
def test_settings_reads_prefixed_env_and_hides_secrets() -> None:
    settings = Settings(_env_file=None)  # pyright: ignore[reportCallIssue]

    assert settings.github_app_id == 12345
    assert settings.github_webhook_secret.get_secret_value() == "webhook-secret-value"
    assert "webhook-secret-value" not in repr(settings)
    assert settings.log_level == "INFO"


def test_settings_fail_fast_when_required_value_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in REQUIRED_ENV:
        monkeypatch.delenv(name, raising=False)

    with pytest.raises(ValidationError):
        Settings(_env_file=None)  # pyright: ignore[reportCallIssue]


@pytest.mark.usefixtures("required_env")
def test_settings_rejects_unknown_log_level(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("HEIMDALL_LOG_LEVEL", "LOUD")

    with pytest.raises(ValidationError):
        Settings(_env_file=None)  # pyright: ignore[reportCallIssue]
