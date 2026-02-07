from __future__ import annotations

from adapter.utils.errors import openai_http_exception


def validate_text_limits(
    items: list[str], max_batch_size: int, max_chars_per_item: int, max_total_chars: int
) -> None:
    if len(items) == 0:
        raise openai_http_exception(400, "input list cannot be empty", "input")
    if len(items) > max_batch_size:
        raise openai_http_exception(400, "too many input items", "input")

    total = 0
    for idx, item in enumerate(items):
        chars = len(item)
        if chars > max_chars_per_item:
            raise openai_http_exception(400, f"input item {idx} exceeds max chars", "input")
        total += chars

    if total > max_total_chars:
        raise openai_http_exception(400, "total input chars exceeded", "input")
