from domain.dependencyLibraries.Globalmports import *
from domain.dependencyLibraries.SQLAlchemy import *



class Ingredient(Base):
    __tablename__ = "ingredient"

    ingredient_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)

    # 1:N (association rows) -> one ingredient can be used in many recipes.
    recipe_ingredients: Mapped[list["RecipeIngredient"]] = relationship(
        back_populates="ingredient",
        cascade="all, delete-orphan",
    )