from domain.dependencyLibraries.Globalmports import *
from domain.dependencyLibraries.SQLAlchemy import *

class RecipeImage(Base):
    __tablename__ = "recipe_image"

    image_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipe.recipe_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    image_url: Mapped[str] = mapped_column(Text, nullable=False)

    # N:1 -> many images belong to one recipe.
    recipe: Mapped["Recipe"] = relationship(back_populates="images")