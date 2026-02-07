import torch

from adapter.embedding_engine import enforce_dimensions
from adapter.hints_cpm import CpmHints


def test_enforce_dimensions_from_body() -> None:
    vectors = torch.ones(2, 8)
    out = enforce_dimensions(vectors, model_dim=8, body_dimensions=4, hints=CpmHints())
    assert out.shape[1] == 4


def test_enforce_dimensions_from_header() -> None:
    vectors = torch.ones(2, 8)
    out = enforce_dimensions(vectors, model_dim=8, body_dimensions=None, hints=CpmHints(embedding_dim=6))
    assert out.shape[1] == 6
