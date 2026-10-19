from domain.dependencyLibraries.Globalmports import *
from domain.dependencyLibraries.SQLAlchemy import *

class RecipeCategory(Base):
    __tablename__ = "recipe_category"

    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipe.recipe_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("category.category_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )

    # N:1 -> many association rows can reference one recipe.
    recipe: Mapped["Recipe"] = relationship(back_populates="recipe_categories")
    # N:1 -> many association rows can reference one category.
    category: Mapped["Category"] = relationship(back_populates="recipe_categories")
