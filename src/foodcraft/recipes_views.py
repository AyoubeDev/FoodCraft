from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from foodcraft import api_client
from foodcraft.users_views import show_error

console = Console()


def show_recipes_menu() -> None:
    table = Table(title="Recipes menu")
    table.add_column("Option")
    table.add_column("Action")

    table.add_row("1", "Add")
    table.add_row("2", "Update")
    table.add_row("3", "Delete")
    table.add_row("4", "Get")
    table.add_row("5", "GetAll")
    table.add_row("0", "Exit")

    console.print(table)

    option = Prompt.ask("Choose an option")

    if option == "1":
        add_recipe()
    elif option == "2":
        update_recipe()
    elif option == "3":
        delete_recipe()
    elif option == "4":
        get_recipe()
    elif option == "5":
        list_recipes()


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

    table = Table(title="Recipe")
    table.add_column("Field")
    table.add_column("Value")

    table.add_row("ID", str(recipe["recipe_id"]))
    table.add_row("Title", recipe["title"])
    table.add_row("Author ID", str(recipe["user_id"]))
    table.add_row("Description", recipe["description"] or "")

    console.print(table)


def list_recipes() -> None:
    recipes, error = api_client.get_all("recipes")
    if show_error(error):
        return

    table = Table(title="All recipes")
    table.add_column("ID")
    table.add_column("Title")
    table.add_column("Author ID")

    for recipe in recipes:
        table.add_row(str(recipe["recipe_id"]), recipe["title"], str(recipe["user_id"]))

    console.print(table)
