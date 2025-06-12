from app.models import RecipeStatus

def _load_pipeline(task: str, model_name: str):
    try:
        from transformers import pipeline
    except ImportError:
        return None

    try:
        return pipeline(task, model=model_name)
    except Exception:
        return None


def predict_cuisine(ingredients: str) -> str:
    """Return a predicted cuisine label, or 'Unknown' if unavailable."""
    cls = _load_pipeline("text-classification", "distilbert-base-uncased-finetuned-cuisine")
    if not cls:
        return "Unknown"
    result = cls(ingredients, truncation=True)[0]
    return result.get("label", "Unknown")


def suggest_status(ingredients: str) -> RecipeStatus:
    """Return a suggested RecipeStatus (defaults to TO_WRITE on any failure)."""
    cls = _load_pipeline("text-classification", "distilbert-base-uncased-finetuned-recipe-status")
    if not cls:
        return RecipeStatus.TO_WRITE

    result = cls(ingredients, truncation=True)[0]
    label = result.get("label", "").upper()
    return RecipeStatus[label] if label in RecipeStatus.__members__ else RecipeStatus.TO_WRITE
