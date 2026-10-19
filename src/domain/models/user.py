from domain.dependencyLibraries.Globalmports import *
from domain.dependencyLibraries.SQLAlchemy import *


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        server_default=func.now(),
    )

    # 1:N -> one user can author many recipes.
    recipes: Mapped[list["Recipe"]] = relationship( # type: ignore
        back_populates="author",
        cascade="all, delete-orphan",
    )
    # 1:N -> one user can create many ratings.
    ratings: Mapped[list["Rating"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    # 1:N (association rows) -> one user can have many favorites.
    favorites: Mapped[list["Favorite"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # N:M self relationship via Follow (rows where this user is follower).
    following: Mapped[list["Follow"]] = relationship(
        foreign_keys="Follow.follower_id",
        back_populates="follower",
        cascade="all, delete-orphan",
    )
    # N:M self relationship via Follow (rows where this user is followed).
    followers: Mapped[list["Follow"]] = relationship(
        foreign_keys="Follow.followed_id",
        back_populates="followed",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"User(user_id={self.user_id}, username='{self.username}', email='{self.email}')"
