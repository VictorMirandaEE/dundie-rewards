"""CLI (Command Line Interface) module of dundie"""

import importlib.metadata

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
@click.argument("filepath", type=click.Path(exists=True))
def load(filepath):
    """Load employees from a CSV file and display them.

    ## Features

    - Validates the data.
    - Parses the data.
    - Displays the data.
    """
    table = Table(title="Dunder Mifflin Employees")
    headers = ["Name", "Department", "Role", "e-mail"]
    for header in headers:
        table.add_column(header, header_style="magenta", highlight=True)

    employees = core.load(filepath)
    for employee in employees:
        table.add_row(*[field.strip() for field in employee.split(",")])

    console = Console()
    console.print(table)
