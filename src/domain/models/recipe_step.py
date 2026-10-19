from domain.dependencyLibraries.Globalmports import *
from domain.dependencyLibraries.SQLAlchemy import *

class RecipeStep(Base):
    __tablename__ = "recipe_step"
    __table_args__ = (UniqueConstraint("recipe_id", "step_number", name="recipe_step_recipe_id_step_number_key"),)

    step_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipe.recipe_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    step_number: Mapped[int] = mapped_column(Integer, nullable=False)
    instruction: Mapped[str] = mapped_column(Text, nullable=False)
    image_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # N:1 -> many steps belong to one recipe.
    recipe: Mapped["Recipe"] = relationship(back_populates="steps")