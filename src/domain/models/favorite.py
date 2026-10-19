from domain.dependencyLibraries.Globalmports import *
from domain.dependencyLibraries.SQLAlchemy import *

class Favorite(Base):
    __tablename__ = "favorite"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipe.recipe_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )

    # N:1 -> many favorite rows can reference one user.
    user: Mapped["User"] = relationship(back_populates="favorites") # type: ignore #
    # N:1 -> many favorite rows can reference one recipe.
    recipe: Mapped["Recipe"] = relationship(back_populates="favorited_by") # type: ignore #