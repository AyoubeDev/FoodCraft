from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from foodcraft import api_client

console = Console()


def show_users_menu() -> None:
    table = Table(title="Users menu")
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
        add_user()
    elif option == "2":
        update_user()
    elif option == "3":
        delete_user()
    elif option == "4":
        get_user()
    elif option == "5":
        list_users()


def show_error(error) -> bool:
    """Muestra el error en rojo. Devuelve True si hubo error."""
    if error:
        console.print(f"[red]Error: {error}[/red]")
    return error is not None


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

    table = Table(title="User")
    table.add_column("Field")
    table.add_column("Value")

    table.add_row("ID", str(user["user_id"]))
    table.add_row("Username", user["username"])
    table.add_row("Email", user["email"])

    console.print(table)


def list_users() -> None:
    users, error = api_client.get_all("users")
    if show_error(error):
        return

    table = Table(title="All users")
    table.add_column("ID")
    table.add_column("Username")
    table.add_column("Email")

    for user in users:
        table.add_row(str(user["user_id"]), user["username"], user["email"])

    console.print(table)
