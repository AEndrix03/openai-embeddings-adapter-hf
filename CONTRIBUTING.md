# Contributing

## Workflow

- Use SerenaMCP for repository operations where available.
- Work task-by-task with one commit per task.
- Commit message must follow one prefix: `feat:`, `fix:`, `chore:`, `test:`, `docs:`.

## Quality gates

Before opening a PR:

```bash
ruff check .
black --check .
mypy src
pytest
```

## Branching

- Keep commits focused and atomic.
- Update docs when behavior or configuration changes.
