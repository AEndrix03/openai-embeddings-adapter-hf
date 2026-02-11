# Suggested commands (Windows/Powershell)
- Create venv: `python -m venv .venv`
- Activate venv: `.\.venv\Scripts\Activate.ps1`
- Install dev deps: `pip install -e .[dev]`
- Run app locally: `uvicorn adapter.main:app --reload`
- Run tests: `python -m pytest -q`
- Run docker CPU profile: `docker compose --profile cpu up --build`
- Run docker GPU profile: `docker compose --profile gpu up --build`
- Useful search: `rg -n "pattern"`