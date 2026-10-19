from domain.dependencyLibraries.Globalmports import *
from domain.dependencyLibraries.SQLAlchemy import *


class Rating(Base):
    __tablename__ = "rating"
    __table_args__ = (UniqueConstraint("user_id", "recipe_id", name="rating_user_id_recipe_id_key"),)

    rating_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipe.recipe_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    stars: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        server_default=func.now(),
    )

    # N:1 -> many ratings belong to one user.
    user: Mapped["User"] = relationship(back_populates="ratings")
    # N:1 -> many ratings belong to one recipe.
    recipe: Mapped["Recipe"] = relationship(back_populates="ratings")
