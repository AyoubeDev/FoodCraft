from domain.dependencyLibraries.Globalmports import *
from domain.dependencyLibraries.SQLAlchemy import *



class Category(Base):
    __tablename__ = "category"

    category_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    # 1:N (association rows) -> one category can be linked to many recipes.
    recipe_categories: Mapped[list["RecipeCategory"]] = relationship( # type: ignore
        back_populates="category",
        cascade="all, delete-orphan",
    )