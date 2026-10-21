from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import FlushError

from backend.responses import ResponseBuilder
from domain import (
    CategoryRepository,
    IngredientRepository,
    RatingRepository,
    RecipeRepository,
    Session,
    UserRepository,
)
from domain.models import (
    Category,
    Favorite,
    Follow,
    Ingredient,
    Rating,
    Recipe,
    RecipeCategory,
    RecipeImage,
    RecipeIngredient,
    RecipeStep,
    User,
)

# Tablas principales (tienen repositorio): nombre -> (modelo, repositorio)
MAIN_TABLES = {
    "user": (User, UserRepository),
    "recipe": (Recipe, RecipeRepository),
    "category": (Category, CategoryRepository),
    "ingredient": (Ingredient, IngredientRepository),
    "rating": (Rating, RatingRepository),
}

# Tablas hijas: nombre -> (modelo, columna que apunta al padre (el {id} de la URL),
#                          columna que identifica la fila dentro del padre)
CHILD_TABLES = {
    "favorite": (Favorite, "user_id", "recipe_id"),
    "follow": (Follow, "follower_id", "followed_id"),
    "recipe_category": (RecipeCategory, "recipe_id", "category_id"),
    "recipe_ingredient": (RecipeIngredient, "recipe_id", "ingredient_id"),
    "recipe_image": (RecipeImage, "recipe_id", "image_id"),
    "recipe_step": (RecipeStep, "recipe_id", "step_id"),
}


def dispatch(order):
    """Recibe una orden de la API y ejecuta la accion. Devuelve una Response.

    order = {"name": "user.add", "params": {"id": "7"}, "query": {}, "body": {...}}
    """
    table, action = order["name"].split(".")

    try:
        params = {key: int(value) for key, value in order["params"].items()}  # ids de la URL
        data = order["body"]

        with Session() as session:
            if table in MAIN_TABLES:
                return main_actions(session, table, action, params, data, order["query"])
            return child_actions(session, table, action, params, data)

    except ValueError as error:  # id no numerico o validacion del repositorio
        return ResponseBuilder.bad_request(str(error))
    except (IntegrityError, FlushError):  # duplicado, o falta/no existe un dato relacionado
        return ResponseBuilder.bad_request("Invalid data: duplicated or missing related data")


def main_actions(session, table, action, params, data, query):
    model, repository = MAIN_TABLES[table]
    repo = repository(session)

    if action == "get_all":
        if table == "recipe" and "title" in query:  # GET /recipes?title=pasta
            return ResponseBuilder.ok_list(table, repo.search_by_title(query["title"]))
        return ResponseBuilder.ok_list(table, repo.get_all())

    if action == "get_by_author":  # GET /users/{id}/recipes
        return ResponseBuilder.ok_list(table, repo.get_by_author(params["id"]))

    if action == "get_by_recipe":  # GET /recipes/{id}/ratings
        return ResponseBuilder.ok_list(table, repo.get_by_recipe(params["id"]))

    if action == "add":
        entity = model(**data)
        if table == "recipe":  # el repositorio exige el autor, no solo el user_id
            entity.author = session.get(User, data["user_id"]) if "user_id" in data else None
        repo.save(entity)
        session.commit()
        return ResponseBuilder.created(table, entity)

    # Las acciones que quedan trabajan sobre una fila concreta: /tabla/{id}
    entity = repo.get(params["id"])
    if entity is None:
        return ResponseBuilder.not_found(f"{table} not found")

    if action == "get":
        return ResponseBuilder.ok(table, entity)

    if action == "update":
        for key, value in data.items():
            setattr(entity, key, value)
        session.commit()
        return ResponseBuilder.ok(table, entity)

    if action == "delete":
        session.delete(entity)
        session.commit()
        return ResponseBuilder.no_content()

    return ResponseBuilder.not_found("Not implemented")


def child_actions(session, table, action, params, data):
    model, parent_column, key_column = CHILD_TABLES[table]

    if action in ("get_all", "get_following", "get_followers"):
        column = "followed_id" if action == "get_followers" else parent_column
        rows = session.scalars(select(model).filter_by(**{column: params["id"]})).all()
        return ResponseBuilder.ok_list(table, rows)

    if action == "add":
        entity = model(**{**data, parent_column: params["id"]})  # el id de la URL manda
        session.add(entity)
        session.commit()
        return ResponseBuilder.created(table, entity)

    # update y delete: /padre/{id}/hijos/{key_column}
    filters = {parent_column: params["id"], key_column: params[key_column]}
    entity = session.scalars(select(model).filter_by(**filters)).first()
    if entity is None:
        return ResponseBuilder.not_found(f"{table} not found")

    if action == "update":
        for key, value in data.items():
            if key not in filters:  # no se cambia la identidad de la fila
                setattr(entity, key, value)
        session.commit()
        return ResponseBuilder.ok(table, entity)

    if action == "delete":
        session.delete(entity)
        session.commit()
        return ResponseBuilder.no_content()

    return ResponseBuilder.not_found("Not implemented")
