from pathlib import Path

from sqlalchemy import select
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from foodcraft.recipes_views import show_recipes_menu as show_recipes_actions
from foodcraft.users_views import show_users_menu as show_users_actions

from domain import (
    CategoryRepository,
    IngredientRepository,
    RecipeRepository,
    Session,
    UserRepository,
)
from domain.models import Rating

console = Console()


def show_logo():
    base = Path(__file__).parent      # directori de app.py  /
    path = base / "logo.txt"         # logo.txt al costat del script

    if path.exists():
        console.print(path.read_text(encoding="utf-8"))
    else:
        console.print("[bold cyan]FoodCraft back-office[/bold cyan]")


def _print_table(title: str, columns: list[str], rows: list[list[str]]) -> None:
    table = Table(caption=title)

    for column in columns:
        table.add_column(column)

    if rows:
        for row in rows:
            table.add_row(*row)
    else:
        table.add_row("-", "No data available", *(["-"] * max(0, len(columns) - 2)))

    console.print(table)


def show_users_menu():
    with Session() as session:
        users = UserRepository(session).get_all()
        rows = [
            [
                str(user.user_id),
                user.username,
                user.email,
                str(len(user.recipes)),
                str(len(user.ratings)),
            ]
            for user in users
        ]

    _print_table(
        "Users",
        ["ID", "Username", "Email", "Recipes", "Ratings"],
        rows,
    )
    show_users_actions()


def show_recipes_menu():
    with Session() as session:
        recipes = RecipeRepository(session).get_all()
        rows = [
            [
                str(recipe.recipe_id),
                recipe.title,
                recipe.author.username if recipe.author else "-",
                str(recipe.prep_time or "-"),
                str(recipe.cook_time or "-"),
                str(recipe.servings or "-"),
            ]
            for recipe in recipes
        ]

    _print_table(
        "Recipes",
        ["ID", "Title", "Author", "Prep", "Cook", "Servings"],
        rows,
    )
    show_recipes_actions()


def show_categories_menu():
    with Session() as session:
        categories = CategoryRepository(session).get_all()
        rows = [[str(category.category_id), category.name] for category in categories]

    _print_table("Categories", ["ID", "Name"], rows)


def show_ingredients_menu():
    with Session() as session:
        ingredients = IngredientRepository(session).get_all()
        rows = [[str(ingredient.ingredient_id), ingredient.name] for ingredient in ingredients]

    _print_table("Ingredients", ["ID", "Name"], rows)


def show_ratings_menu():
    with Session() as session:
        ratings = session.scalars(select(Rating)).all()
        rows = [
            [
                str(rating.rating_id),
                rating.user.username if rating.user else "-",
                rating.recipe.title if rating.recipe else "-",
                str(rating.stars),
                rating.comment or "-",
            ]
            for rating in ratings
        ]

    _print_table(
        "Ratings",
        ["ID", "User", "Recipe", "Stars", "Comment"],
        rows,
    )


def main_menu():
    table = Table(caption="Main menu")

    table.add_column("Option")
    table.add_column("Menu")

    table.add_row("1", "Users", " -->")
    table.add_row("2", "Recipes", " -->")
    table.add_row("3", "Categories")
    table.add_row("4", "Ingredients")
    table.add_row("5", "Ratings")
    table.add_row("0", "Exit")

    console.print(table)

    return Prompt.ask("Choose an option")


def run_back_office():
    show_logo()

    while True:
        option = main_menu()
        handle_option(option)


def handle_option(option: str):
    if option == "1":
        show_users_menu()
    elif option == "2":
        show_recipes_menu()
    elif option == "3":
        show_categories_menu()
    elif option == "4":
        show_ingredients_menu()
    elif option == "5":
        show_ratings_menu()
    elif option == "0":
        console.print("[bold red]Exiting...[/bold red]")
        raise SystemExit
    else:
        console.print("[red]Invalid option[/red]")


if __name__ == "__main__":
    run_back_office()