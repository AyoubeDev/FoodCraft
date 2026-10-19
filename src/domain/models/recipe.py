from domain.dependencyLibraries.Globalmports import *
from domain.dependencyLibraries.SQLAlchemy import *




class Recipe(Base):
    __tablename__ = "recipe"

    recipe_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    prep_time: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    cook_time: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    servings: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        server_default=func.now(),
    )

    # N:1 -> many recipes belong to one user (author).
    author: Mapped["User"] = relationship(back_populates="recipes") # type: ignore
    # 1:N -> one recipe can have many ratings.
    ratings: Mapped[list["Rating"]] = relationship(
        back_populates="recipe",
        cascade="all, delete-orphan",
    )
    # 1:N -> one recipe can have many images.
    images: Mapped[list["RecipeImage"]] = relationship(
        back_populates="recipe",
        cascade="all, delete-orphan",
    )
    # 1:N -> one recipe can have many ordered steps.
    steps: Mapped[list["RecipeStep"]] = relationship(
        back_populates="recipe",
        cascade="all, delete-orphan",
        order_by="RecipeStep.step_number",
    )
    # 1:N (association rows) -> one recipe can be linked to many categories.
    recipe_categories: Mapped[list["RecipeCategory"]] = relationship(
        back_populates="recipe",
        cascade="all, delete-orphan",
    )
    # 1:N (association rows) -> one recipe can be linked to many ingredients.
    recipe_ingredients: Mapped[list["RecipeIngredient"]] = relationship(
        back_populates="recipe",
        cascade="all, delete-orphan",
    )
    # 1:N (association rows) -> one recipe can be favorited by many users.
    favorited_by: Mapped[list["Favorite"]] = relationship(
        back_populates="recipe",
        cascade="all, delete-orphan",
    )
