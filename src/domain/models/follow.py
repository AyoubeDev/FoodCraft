from domain.dependencyLibraries.Globalmports import *
from domain.dependencyLibraries.SQLAlchemy import *

class Follow(Base):
    __tablename__ = "follow"

    follower_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    followed_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )

    # N:1 -> many follow rows can reference one user as follower.
    follower: Mapped["User"] = relationship( # type: ignore
        foreign_keys=[follower_id],
        back_populates="following",
    )
    # N:1 -> many follow rows can reference one user as followed.
    followed: Mapped["User"] = relationship(
        foreign_keys=[followed_id],
        back_populates="followers",
    )