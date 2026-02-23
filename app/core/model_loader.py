"""
TalentIQ — Singleton Model Loader
Loads SentenceTransformer ONCE at startup and reuses across all engines.
Uses lazy-loading to avoid re-downloading on every uvicorn reload.
"""

import logging
from sentence_transformers import SentenceTransformer
from app.config import settings

logger = logging.getLogger(__name__)

_model: SentenceTransformer | None = None


def get_model() -> SentenceTransformer:
    """Return the cached model, loading it on first call."""
    global _model
    if _model is None:
        logger.info("Loading SentenceTransformer model '%s' …", settings.EMBEDDING_MODEL)
        _model = SentenceTransformer(settings.EMBEDDING_MODEL)
        logger.info("Model loaded successfully.")
    return _model


class _LazyModel:
    """Proxy that delays model loading until first attribute access."""
    def __getattr__(self, name):
        return getattr(get_model(), name)
    def __call__(self, *args, **kwargs):
        return get_model()(*args, **kwargs)


# Backward-compatible: `from app.core.model_loader import model` still works
model = _LazyModel()
