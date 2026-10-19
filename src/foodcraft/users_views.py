from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from domain import Session, UserRepository
from domain.models import User

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
    elif option == "0":
        return


def add_user() -> None:
    console.print("[bold cyan]Add new user[/bold cyan]")

    user = User(
        username=Prompt.ask("Username"),
        email=Prompt.ask("Email"),
        password_hash=Prompt.ask("Password hash"),
    )

    try:
        with Session() as session:
            repo = UserRepository(session)
            repo.save(user)
            session.commit()
        console.print("[green]User added successfully![/green]")
    except Exception as error:
        console.print(f"[red]Error: {error}[/red]")


def update_user() -> None:
    user_id = Prompt.ask("ID of user to update")

    with Session() as session:
        repo = UserRepository(session)
        user = repo.get(int(user_id))

        if user is None:
            console.print("[red]User not found[/red]")
            return

        console.print("[yellow]Leave fields empty to keep current value[/yellow]")

        user.username = Prompt.ask("Username", default=user.username)
        user.email = Prompt.ask("Email", default=user.email)
        user.password_hash = Prompt.ask("Password hash", default=user.password_hash)
        repo.update(user)

    console.print("[green]User updated successfully[/green]")


def delete_user() -> None:
    user_id = Prompt.ask("ID to delete")

    with Session() as session:
        repo = UserRepository(session)
        user = repo.get(int(user_id))

        if user is None:
            console.print("[red]User not found[/red]")
            return

        repo.delete(int(user_id))
        session.commit()

    console.print("[green]User deleted[/green]")


def get_user() -> None:
    user_id = Prompt.ask("ID")

    with Session() as session:
        repo = UserRepository(session)
        user = repo.get(int(user_id))

    if user is None:
        console.print("[red]User not found[/red]")
        return

    table = Table(title="User")
    table.add_column("Field")
    table.add_column("Value")

    table.add_row("ID", str(user.user_id))
    table.add_row("Username", user.username)
    table.add_row("Email", user.email)

    console.print(table)


def list_users() -> None:
    with Session() as session:
        repo = UserRepository(session)
        users = repo.get_all()

    table = Table(title="All users")
    table.add_column("ID")
    table.add_column("Username")
    table.add_column("Email")

    for user in users:
        table.add_row(str(user.user_id), user.username, user.email)

    console.print(table)