from enum import Enum


class RecipeStatus(Enum):
    TO_WRITE = "to_write"
    TO_TRY = "to_try"
    MADE_BEFORE = "made_before"
