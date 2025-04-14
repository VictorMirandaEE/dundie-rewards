"""CLI (Command Line Interface) module of dundie."""

import importlib.metadata
import json
from datetime import datetime
from decimal import Decimal

import rich_click as click
from rich.console import Console
from rich.table import Table

from dundie import core
from dundie.settings import PROJECT_NAME

click.rich_click.USE_RICH_MARKUP = True
click.rich_click.USE_MARKDOWN = True
click.rich_click.SHOW_ARGUMENTS = True
click.rich_click.GROUP_ARGUMENTS_OPTIONS = True
click.rich_click.SHOW_METAVARS_COLUMN = False
click.rich_click.APPEND_METAVARS_HELP = True


class CustomJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder for Decimal and datetime objects."""

    def default(self, obj):
        """Convert Decimal and datetime objects to string."""
        if isinstance(obj, Decimal):
            return str(obj)
        if isinstance(obj, datetime):
            return str(obj)
        return super().default(obj)


@click.group()
@click.version_option(importlib.metadata.version(PROJECT_NAME))
def main():
    """Dunder Mifflin Rewards System.

    This is a CLI tool for managing the Dunder Mifflin Rewards program.

    ## Features

    - Admins can load employees data to the database and assign points.
    - Users can view their rewards points and transfer them to other employees.
    """


@main.command()
@click.argument("filepath", type=click.Path(exists=True), required=True)
def load(filepath: str) -> None:
    """Load employees data from a CSV file to the database and display them.

    FILEPATH is the path to the CSV file.

    ## Features

    - Validates the data.
    - Parses the data.
    - Displays the data.
    """
    table = Table(title="Dunder Mifflin Employees")
    headers = ["Name", "e-mail", "Role", "Department", "Currency", "Created"]
    for header in headers:
        table.add_column(header, header_style="magenta", highlight=True)

    employees = core.load(filepath)

    if not employees:
        console = Console()
        console.print(
            "ERROR: Check the CSV and the log files for errors",
            style="bold red",
        )
        return

    for employee in employees:
        table.add_row(*[str(entry) for entry in employee.values()])

    console = Console()
    console.print(table)


@main.command()
@click.option("--email", required=False, help="Filter by employee email")
@click.option("--department", required=False, help="Filter by department")
@click.option(
    "--file",
    required=False,
    type=click.File("w"),
    help="Output to file",
)
@click.option(
    "--format",
    type=click.Choice(["txt", "json"], case_sensitive=False),
    default="txt",
    help="Output format (txt or json)",
)
def show(**query) -> None:
    """Show employees data.

    ## Features

    - Filter by email or department.
    - Output to console or file.
    - Output format as TXT or JSON.
    """
    result = core.read(**query)

    if not result:
        console = Console()
        console.print("No results found")
        return

    table = Table(title="Dunder Mifflin Rewards Report")
    for key in result[0].keys():
        table.add_column(key.title(), header_style="magenta", highlight=True)

    for employee in result:
        employee["balance"] = f"{employee['balance']:.2f}"
        employee["total"] = f"{employee['total']:.2f}"
        table.add_row(*[str(entry) for entry in employee.values()])

    if query["format"] == "json":
        output_data = json.dumps(result, indent=4, cls=CustomJSONEncoder)
        if query["file"]:
            query["file"].write(output_data)
        else:
            console = Console()
            console.print(output_data)
    else:
        if query["file"]:
            with query["file"] as file:
                console = Console(file=file)
                console.print(table)
        else:
            console = Console()
            console.print(table)


@main.command()
@click.argument("value", type=click.FLOAT, required=True)
@click.option("--email", required=False, help="Filter by employee email")
@click.option("--department", required=False, help="Filter by department")
@click.pass_context
def update(ctx, value: Decimal, **query) -> None:
    """Update the balance of reward points.

    VALUE is the number of points to add.

    Prefix a negative VALUE with '-- ' to subtract points.

    ## Features

    - Filter by email or department.
    """
    result = core.update(value, **query)
    if result:
        console = Console()
        console.print(result)
        return

    ctx.invoke(show, **query)
