from __future__ import annotations

from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session as SQLAlchemySession

from .models import Category, Ingredient, Rating, Recipe, User

K = TypeVar("K")
V = TypeVar("V")


class Repository(Generic[K, V]):
    model_class: type[V]

    def __init__(self, session: SQLAlchemySession):
        self.session = session

    def save(self, entity: V) -> V:
        self._validate(entity)
        self.session.add(entity)
        return entity

    def update(self, entity: V) -> V:
        self._validate(entity)
        merged_entity = self.session.merge(entity)
        self.session.commit()
        return merged_entity

    def get(self, entity_id: K) -> V | None:
        return self.session.get(self.model_class, entity_id)

    def get_all(self) -> list[V]:
        statement = select(self.model_class)
        return list(self.session.scalars(statement).all())

    def delete(self, entity_id: K) -> None:
        entity = self.get(entity_id)
        if entity is None:
            raise ValueError(f"{self.model_class.__name__} with id {entity_id} was not found")
        self.session.delete(entity)

    def _validate(self, entity: V) -> None:
        return None


class UserRepository(Repository[int, User]):
    model_class = User

    def _validate(self, entity: User) -> None:
        if not entity.username:
            raise ValueError("username is mandatory")
        if not entity.email:
            raise ValueError("email is mandatory")
        if not entity.password_hash:
            raise ValueError("password_hash is mandatory")
        
    def get_by_email(self, email:str):
        stmt = select(User).where(User.email == email)
        return self.session.scalar(stmt)

    def get_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        return self.session.scalar(stmt)

    def exists_by_email(self, email: str) -> bool:
        return self.get_by_email(email) is not None
    
    


class CategoryRepository(Repository[int, Category]):
    model_class = Category

    def _validate(self, entity: Category) -> None:
        if not entity.name:
            raise ValueError("name is mandatory")

    def get_by_name(self, name: str) -> Category | None:
        stmt = select(Category).where(Category.name == name)
        return self.session.scalar(stmt)


class IngredientRepository(Repository[int, Ingredient]):
    model_class = Ingredient

    def _validate(self, entity: Ingredient) -> None:
        if not entity.name:
            raise ValueError("name is mandatory")

    def get_by_name(self, name: str) -> Ingredient | None:
        stmt = select(Ingredient).where(Ingredient.name == name)
        return self.session.scalar(stmt)


class RecipeRepository(Repository[int, Recipe]):
    model_class = Recipe

    def _validate(self, entity: Recipe) -> None:
        if entity.author is None:
            raise ValueError("author is mandatory")
        if not entity.title:
            raise ValueError("title is mandatory")

    def get_by_author(self, user_id: int) -> list[Recipe]:
        stmt = select(Recipe).where(Recipe.author.has(User.user_id == user_id))
        return list(self.session.scalars(stmt).all())

    def search_by_title(self, title: str) -> list[Recipe]:
        stmt = select(Recipe).where(Recipe.title.ilike(f"%{title}%"))
        return list(self.session.scalars(stmt).all())


class RatingRepository(Repository[int, Rating]):
    model_class = Rating

    def _validate(self, entity: Rating) -> None:
        if entity.user_id is None:
            raise ValueError("user_id is mandatory")
        if entity.recipe_id is None:
            raise ValueError("recipe_id is mandatory")
        if entity.stars is None:
            raise ValueError("stars is mandatory")
        if not 1 <= entity.stars <= 5:
            raise ValueError("stars must be between 1 and 5")

    def get_by_user_and_recipe(self, user_id: int, recipe_id: int) -> Rating | None:
        stmt = select(Rating).where(
            Rating.user_id == user_id,
            Rating.recipe_id == recipe_id,
        )
        return self.session.scalar(stmt)

    def get_by_recipe(self, recipe_id: int) -> list[Rating]:
        stmt = select(Rating).where(Rating.recipe_id == recipe_id)
        return list(self.session.scalars(stmt).all())