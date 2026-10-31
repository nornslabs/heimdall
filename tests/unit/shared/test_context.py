import dataclasses

import pytest

from heimdall.shared.context import PrRef, TenantCtx, new_request_id
from heimdall.shared.ids import InstallationId, RepoId


def test_tenant_ctx_is_immutable() -> None:
    ctx = TenantCtx(installation_id=InstallationId(7), request_id="req-1")

    with pytest.raises(dataclasses.FrozenInstanceError):
        ctx.installation_id = InstallationId(8)  # pyright: ignore[reportAttributeAccessIssue]


def test_pr_ref_equality() -> None:
    assert PrRef(repo_id=RepoId(1), number=42) == PrRef(repo_id=RepoId(1), number=42)
    assert PrRef(repo_id=RepoId(1), number=42) != PrRef(repo_id=RepoId(2), number=42)


def test_pr_ref_rejects_non_positive_number() -> None:
    with pytest.raises(ValueError):
        PrRef(repo_id=RepoId(1), number=0)


def test_new_request_id_is_unique() -> None:
    assert new_request_id() != new_request_id()
