"""CLI (Command Line Interface) module of dundie"""

import importlib.metadata
import json

import rich_click as click
from rich.console import Console
from rich.table import Table

from dundie import core

click.rich_click.USE_RICH_MARKUP = True
click.rich_click.USE_MARKDOWN = True
click.rich_click.SHOW_ARGUMENTS = True
click.rich_click.GROUP_ARGUMENTS_OPTIONS = True
click.rich_click.SHOW_METAVARS_COLUMN = False
click.rich_click.APPEND_METAVARS_HELP = True


@click.group()
@click.version_option(importlib.metadata.version("dundie"))
def main():
    """Dunder Mifflin Rewards System

    This is a CLI tool for managing the Dunder Mifflin Rewards program.
    """


@main.command()
@click.argument("filepath", type=click.Path(exists=True), required=True)
def load(filepath):
    """Load employees data from a CSV file and display them.

    \nFILEPATH is the path to the CSV file.

    ## Features

    - Validates the data.
    - Parses the data.
    - Displays the data.
    """
    table = Table(title="Dunder Mifflin Employees")
    headers = ["Name", "Department", "Role", "e-mail", "Points", "Created"]
    for header in headers:
        table.add_column(header, header_style="magenta", highlight=True)

    employees = core.load(filepath)
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
    type=click.Choice(["table", "json"], case_sensitive=False),
    default="table",
    help="Output format (table or json)",
)
def show(**query):
    """Show employees data

    - Filter by email or department
    - Output to console or file
    - Output format as table or json
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
        table.add_row(*[str(entry) for entry in employee.values()])

    if query["format"] == "json":
        output_data = json.dumps(result, indent=4)
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
@click.argument("value", type=click.INT, required=True)
@click.option("--email", required=False, help="Filter by employee email")
@click.option("--department", required=False, help="Filter by department")
@click.pass_context
def update(ctx, value, **query):
    """Update the balance of reward points

    VALUE is the number of points to add
    \nPrefix '-- ' to a negative VALUE to subtract points

    - Filter by email or department
    """
    core.update(value, **query)
    ctx.invoke(show, **query)
