from pathlib import Path

from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from foodcraft import api_client
from foodcraft.recipes_views import show_recipes_menu as show_recipes_actions
from foodcraft.users_views import show_error
from foodcraft.users_views import show_users_menu as show_users_actions

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
    users, error = api_client.get_all("users")
    if show_error(error):
        return

    rows = [[str(u["user_id"]), u["username"], u["email"]] for u in users]
    _print_table("Users", ["ID", "Username", "Email"], rows)
    show_users_actions()


def show_recipes_menu():
    recipes, error = api_client.get_all("recipes")
    if show_error(error):
        return

    rows = [
        [
            str(r["recipe_id"]),
            r["title"],
            str(r["user_id"]),
            str(r["prep_time"] or "-"),
            str(r["cook_time"] or "-"),
            str(r["servings"] or "-"),
        ]
        for r in recipes
    ]
    _print_table("Recipes", ["ID", "Title", "Author ID", "Prep", "Cook", "Servings"], rows)
    show_recipes_actions()


def show_categories_menu():
    categories, error = api_client.get_all("categories")
    if show_error(error):
        return

    rows = [[str(c["category_id"]), c["name"]] for c in categories]
    _print_table("Categories", ["ID", "Name"], rows)


def show_ingredients_menu():
    ingredients, error = api_client.get_all("ingredients")
    if show_error(error):
        return

    rows = [[str(i["ingredient_id"]), i["name"]] for i in ingredients]
    _print_table("Ingredients", ["ID", "Name"], rows)


def show_ratings_menu():
    ratings, error = api_client.get_all("ratings")
    if show_error(error):
        return

    rows = [
        [
            str(r["rating_id"]),
            str(r["user_id"]),
            str(r["recipe_id"]),
            str(r["stars"]),
            r["comment"] or "-",
        ]
        for r in ratings
    ]
    _print_table("Ratings", ["ID", "User ID", "Recipe ID", "Stars", "Comment"], rows)


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
