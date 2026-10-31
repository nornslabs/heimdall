# Contributing to Heimdall

Read [AGENTS.md](AGENTS.md) first. It defines module borders, private `_` files, readability limits, docstring style and security rules.

## Setup

```bash
uv sync
uv run ruff check . && uv run ruff format --check . && uv run pyright && uv run pytest
```

## Branches

One branch per Linear issue, using the branch name Linear generates: `<user>/hei-<n>-<slug>`, for example `contactsagarbera/hei-29-create-folder-structure-and-module-stubs`.

## Commits

`<module>: <change>`, in the imperative and lower case, for example:

- `triage: add next_state transition table`
- `adapters/github: verify webhook signatures`
- `repo: init uv project` (for repo-wide tooling)

## Module borders

- A module imports another module only through its `api.py`.
- Names starting with `_` never cross a module border.
- `tests/unit/test_module_borders.py` enforces both, and CI runs it.

## Pull request checklist

- [ ] Linked to its Linear issue (`HEI-<n>` in the title or branch)
- [ ] `uv run ruff check .` and `uv run ruff format --check .` pass
- [ ] `uv run pyright` passes (strict on `src/`)
- [ ] Tests added or updated; `uv run pytest` passes
- [ ] Public functions have Google-style docstrings
- [ ] No secrets, tokens or `.env` files committed
- [ ] Module README updated if the module's public API changed
