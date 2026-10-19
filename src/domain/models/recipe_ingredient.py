from domain.dependencyLibraries.Globalmports import *
from domain.dependencyLibraries.SQLAlchemy import *


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredient"

    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipe.recipe_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey("ingredient.ingredient_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    quantity: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True)
    unit: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # N:1 -> many association rows can reference one recipe.
    recipe: Mapped["Recipe"] = relationship(back_populates="recipe_ingredients")
    # N:1 -> many association rows can reference one ingredient.
    ingredient: Mapped["Ingredient"] = relationship(back_populates="recipe_ingredients")

