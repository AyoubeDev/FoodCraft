from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from domain import RecipeRepository, Session, UserRepository
from domain.models import Recipe

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
    elif option == "0":
        return


def add_recipe() -> None:
    console.print("[bold cyan]Add new recipe[/bold cyan]")

    with Session() as session:
        user_repo = UserRepository(session)
        recipe_repo = RecipeRepository(session)

        author_id = int(Prompt.ask("Author user ID"))
        author = user_repo.get(author_id)
        if author is None:
            console.print("[red]Author not found[/red]")
            return

        recipe = Recipe(
            author=author,
            title=Prompt.ask("Title"),
            description=Prompt.ask("Description", default=""),
        )

        try:
            recipe_repo.save(recipe)
            session.commit()
            console.print("[green]Recipe added successfully![/green]")
        except Exception as error:
            console.print(f"[red]Error: {error}[/red]")


def update_recipe() -> None:
    recipe_id = Prompt.ask("ID of recipe to update")

    with Session() as session:
        user_repo = UserRepository(session)
        recipe_repo = RecipeRepository(session)
        recipe = recipe_repo.get(int(recipe_id))

        if recipe is None:
            console.print("[red]Recipe not found[/red]")
            return

        console.print("[yellow]Leave fields empty to keep current value[/yellow]")

        current_author = recipe.author.user_id if recipe.author else recipe.user_id
        author_id = int(Prompt.ask("Author user ID", default=str(current_author)))
        author = user_repo.get(author_id)
        if author is None:
            console.print("[red]Author not found[/red]")
            return

        recipe.author = author
        recipe.title = Prompt.ask("Title", default=recipe.title)
        recipe.description = Prompt.ask("Description", default=recipe.description or "")

        recipe_repo.update(recipe)

    console.print("[green]Recipe updated successfully[/green]")


def delete_recipe() -> None:
    recipe_id = Prompt.ask("ID to delete")

    with Session() as session:
        repo = RecipeRepository(session)
        recipe = repo.get(int(recipe_id))

        if recipe is None:
            console.print("[red]Recipe not found[/red]")
            return

        repo.delete(int(recipe_id))
        session.commit()

    console.print("[green]Recipe deleted[/green]")


def get_recipe() -> None:
    recipe_id = Prompt.ask("ID")

    with Session() as session:
        repo = RecipeRepository(session)
        recipe = repo.get(int(recipe_id))

    if recipe is None:
        console.print("[red]Recipe not found[/red]")
        return

    table = Table(title="Recipe")
    table.add_column("Field")
    table.add_column("Value")

    table.add_row("ID", str(recipe.recipe_id))
    table.add_row("Title", recipe.title)
    table.add_row("Author ID", str(recipe.user_id))
    table.add_row("Description", recipe.description or "")

    console.print(table)


def list_recipes() -> None:
    with Session() as session:
        repo = RecipeRepository(session)
        recipes = repo.get_all()

    table = Table(title="All recipes")
    table.add_column("ID")
    table.add_column("Title")
    table.add_column("Author ID")

    for recipe in recipes:
        table.add_row(str(recipe.recipe_id), recipe.title, str(recipe.user_id))

    console.print(table)