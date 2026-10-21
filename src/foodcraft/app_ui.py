from collections.abc import Callable
from pathlib import Path

from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from foodcraft import api_client

console = Console()


def show_error(error) -> bool:
    if error:
        console.print(f"[red]Error: {error}[/red]")
    return error is not None


def print_table(title: str, columns: list[str], rows: list[list[str]]) -> None:
    table = Table(title=title)
    for column in columns:
        table.add_column(column)

    if rows:
        for row in rows:
            table.add_row(*row)
    else:
        table.add_row("-", "No data available", *(["-"] * max(0, len(columns) - 2)))

    console.print(table)


def show_record(title: str, fields: list[tuple[str, str]]) -> None:
    table = Table(title=title)
    table.add_column("Field")
    table.add_column("Value")
    for name, value in fields:
        table.add_row(name, value)
    console.print(table)


def show_logo() -> None:
    path = Path(__file__).parent / "logo.txt"
    if path.exists():
        console.print(path.read_text(encoding="utf-8"))
    else:
        console.print("[bold cyan]FoodCraft back-office[/bold cyan]")


def action_menu(title: str, actions: dict[str, tuple[str, Callable[[], None]]]) -> None:
    table = Table(title=title)
    table.add_column("Option")
    table.add_column("Action")
    for option, (label, _) in actions.items():
        table.add_row(option, label)
    table.add_row("0", "Exit")
    console.print(table)

    action = actions.get(Prompt.ask("Choose an option"))
    if action is not None:
        action[1]()


def add_user() -> None:
    console.print("[bold cyan]Add new user[/bold cyan]")
    data = {
        "username": Prompt.ask("Username"),
        "email": Prompt.ask("Email"),
        "password_hash": Prompt.ask("Password hash"),
    }
    _, error = api_client.create("users", data)
    if not show_error(error):
        console.print("[green]User added successfully![/green]")


def update_user() -> None:
    user_id = Prompt.ask("ID of user to update")
    user, error = api_client.get("users", user_id)
    if show_error(error):
        return

    console.print("[yellow]Leave fields empty to keep current value[/yellow]")
    data = {
        "username": Prompt.ask("Username", default=user["username"]),
        "email": Prompt.ask("Email", default=user["email"]),
    }
    _, error = api_client.update("users", user_id, data)
    if not show_error(error):
        console.print("[green]User updated successfully[/green]")


def delete_user() -> None:
    user_id = Prompt.ask("ID to delete")
    _, error = api_client.delete("users", user_id)
    if not show_error(error):
        console.print("[green]User deleted[/green]")


def get_user() -> None:
    user_id = Prompt.ask("ID")
    user, error = api_client.get("users", user_id)
    if show_error(error):
        return

    show_record("User", [
        ("ID", str(user["user_id"])),
        ("Username", user["username"]),
        ("Email", user["email"]),
    ])


def list_users() -> None:
    users, error = api_client.get_all("users")
    if show_error(error):
        return

    print_table("All users", ["ID", "Username", "Email"], [
        [str(user["user_id"]), user["username"], user["email"]]
        for user in users
    ])


def add_recipe() -> None:
    console.print("[bold cyan]Add new recipe[/bold cyan]")
    data = {
        "user_id": Prompt.ask("Author user ID"),
        "title": Prompt.ask("Title"),
        "description": Prompt.ask("Description", default=""),
    }
    _, error = api_client.create("recipes", data)
    if not show_error(error):
        console.print("[green]Recipe added successfully![/green]")


def update_recipe() -> None:
    recipe_id = Prompt.ask("ID of recipe to update")
    recipe, error = api_client.get("recipes", recipe_id)
    if show_error(error):
        return

    console.print("[yellow]Leave fields empty to keep current value[/yellow]")
    data = {
        "user_id": Prompt.ask("Author user ID", default=str(recipe["user_id"])),
        "title": Prompt.ask("Title", default=recipe["title"]),
        "description": Prompt.ask("Description", default=recipe["description"] or ""),
    }
    _, error = api_client.update("recipes", recipe_id, data)
    if not show_error(error):
        console.print("[green]Recipe updated successfully[/green]")


def delete_recipe() -> None:
    recipe_id = Prompt.ask("ID to delete")
    _, error = api_client.delete("recipes", recipe_id)
    if not show_error(error):
        console.print("[green]Recipe deleted[/green]")


def get_recipe() -> None:
    recipe_id = Prompt.ask("ID")
    recipe, error = api_client.get("recipes", recipe_id)
    if show_error(error):
        return

    show_record("Recipe", [
        ("ID", str(recipe["recipe_id"])),
        ("Title", recipe["title"]),
        ("Author ID", str(recipe["user_id"])),
        ("Description", recipe["description"] or ""),
    ])


def list_recipes() -> None:
    recipes, error = api_client.get_all("recipes")
    if show_error(error):
        return

    print_table("All recipes", ["ID", "Title", "Author ID"], [
        [str(recipe["recipe_id"]), recipe["title"], str(recipe["user_id"])]
        for recipe in recipes
    ])


def show_users_menu() -> None:
    users, error = api_client.get_all("users")
    if show_error(error):
        return

    print_table("Users", ["ID", "Username", "Email"], [
        [str(user["user_id"]), user["username"], user["email"]]
        for user in users
    ])
    action_menu("Users menu", {
        "1": ("Add", add_user),
        "2": ("Update", update_user),
        "3": ("Delete", delete_user),
        "4": ("Get", get_user),
        "5": ("GetAll", list_users),
    })


def show_recipes_menu() -> None:
    recipes, error = api_client.get_all("recipes")
    if show_error(error):
        return

    print_table("Recipes", ["ID", "Title", "Author ID", "Prep", "Cook", "Servings"], [
        [
            str(recipe["recipe_id"]),
            recipe["title"],
            str(recipe["user_id"]),
            str(recipe["prep_time"] or "-"),
            str(recipe["cook_time"] or "-"),
            str(recipe["servings"] or "-"),
        ]
        for recipe in recipes
    ])
    action_menu("Recipes menu", {
        "1": ("Add", add_recipe),
        "2": ("Update", update_recipe),
        "3": ("Delete", delete_recipe),
        "4": ("Get", get_recipe),
        "5": ("GetAll", list_recipes),
    })


def show_categories_menu() -> None:
    categories, error = api_client.get_all("categories")
    if not show_error(error):
        print_table("Categories", ["ID", "Name"], [
            [str(category["category_id"]), category["name"]]
            for category in categories
        ])


def show_ingredients_menu() -> None:
    ingredients, error = api_client.get_all("ingredients")
    if not show_error(error):
        print_table("Ingredients", ["ID", "Name"], [
            [str(ingredient["ingredient_id"]), ingredient["name"]]
            for ingredient in ingredients
        ])


def show_ratings_menu() -> None:
    ratings, error = api_client.get_all("ratings")
    if not show_error(error):
        print_table("Ratings", ["ID", "User ID", "Recipe ID", "Stars", "Comment"], [
            [
                str(rating["rating_id"]),
                str(rating["user_id"]),
                str(rating["recipe_id"]),
                str(rating["stars"]),
                rating["comment"] or "-",
            ]
            for rating in ratings
        ])


def main_menu() -> str:
    table = Table(title="Main menu")
    table.add_column("Option")
    table.add_column("Menu")
    table.add_row("1", "Users")
    table.add_row("2", "Recipes")
    table.add_row("3", "Categories")
    table.add_row("4", "Ingredients")
    table.add_row("5", "Ratings")
    table.add_row("0", "Exit")
    console.print(table)
    return Prompt.ask("Choose an option")


def run_back_office() -> None:
    show_logo()
    actions = {
        "1": show_users_menu,
        "2": show_recipes_menu,
        "3": show_categories_menu,
        "4": show_ingredients_menu,
        "5": show_ratings_menu,
    }

    while True:
        option = main_menu()
        if option == "0":
            console.print("[bold red]Exiting...[/bold red]")
            return

        action = actions.get(option)
        if action is not None:
            action()
        else:
            console.print("[red]Invalid option[/red]")


if __name__ == "__main__":
    run_back_office()
