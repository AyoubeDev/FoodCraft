# Cada ruta es (metodo, url, nombre). {algo} es un valor que cambia: /users/7 -> id = 7.


def crud(name, url):
    return [
        ("POST", f"/{url}", f"{name}.add"),
        ("GET", f"/{url}", f"{name}.get_all"),
        ("GET", f"/{url}/{{id}}", f"{name}.get"),
        ("PUT", f"/{url}/{{id}}", f"{name}.update"),
        ("DELETE", f"/{url}/{{id}}", f"{name}.delete"),
    ]


ROUTES = (
    crud("user", "users")
    + crud("recipe", "recipes")
    + crud("category", "categories")
    + crud("ingredient", "ingredients")
    + crud("rating", "ratings")
    + [
        ("GET", "/users/{id}/recipes", "recipe.get_by_author"),
        ("GET", "/recipes/{id}/ratings", "rating.get_by_recipe"),
        # Tablas hijas, siempre colgando de su padre
        ("GET", "/users/{id}/favorites", "favorite.get_all"),
        ("POST", "/users/{id}/favorites", "favorite.add"),
        ("DELETE", "/users/{id}/favorites/{recipe_id}", "favorite.delete"),
        ("GET", "/users/{id}/following", "follow.get_following"),
        ("GET", "/users/{id}/followers", "follow.get_followers"),
        ("POST", "/users/{id}/following", "follow.add"),
        ("DELETE", "/users/{id}/following/{followed_id}", "follow.delete"),
        ("GET", "/recipes/{id}/categories", "recipe_category.get_all"),
        ("POST", "/recipes/{id}/categories", "recipe_category.add"),
        ("DELETE", "/recipes/{id}/categories/{category_id}", "recipe_category.delete"),
        ("GET", "/recipes/{id}/ingredients", "recipe_ingredient.get_all"),
        ("POST", "/recipes/{id}/ingredients", "recipe_ingredient.add"),
        ("PUT", "/recipes/{id}/ingredients/{ingredient_id}", "recipe_ingredient.update"),
        ("DELETE", "/recipes/{id}/ingredients/{ingredient_id}", "recipe_ingredient.delete"),
        ("GET", "/recipes/{id}/images", "recipe_image.get_all"),
        ("POST", "/recipes/{id}/images", "recipe_image.add"),
        ("DELETE", "/recipes/{id}/images/{image_id}", "recipe_image.delete"),
        ("GET", "/recipes/{id}/steps", "recipe_step.get_all"),
        ("POST", "/recipes/{id}/steps", "recipe_step.add"),
        ("PUT", "/recipes/{id}/steps/{step_id}", "recipe_step.update"),
        ("DELETE", "/recipes/{id}/steps/{step_id}", "recipe_step.delete"),
    ]
)


def find_route(method, path):
    """Devuelve (nombre, parametros) o None si no existe la ruta."""
    path_parts = path.strip("/").split("/")

    for route_method, url, name in ROUTES:
        url_parts = url.strip("/").split("/")
        if route_method != method or len(url_parts) != len(path_parts):
            continue

        params = {}
        for url_part, path_part in zip(url_parts, path_parts):
            if url_part.startswith("{"):
                params[url_part.strip("{}")] = path_part
            elif url_part != path_part:
                break
        else:
            return name, params

    return None
