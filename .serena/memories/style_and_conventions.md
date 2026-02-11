# Style and conventions
- Formatting: Black + Ruff with line length 100.
- Ruff lint rules include E, F, I, B, UP.
- Type hints are used throughout; strict mypy is not fully enforced (`disallow_untyped_defs=false`).
- Tests use pytest; naming convention `test_*.py` and `test_*` functions.
- Config is centralized in `adapter/settings.py` via `pydantic-settings` with `ADAPTER_` env prefix.