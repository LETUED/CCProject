import inquirer
from rich.console import Console
from rich.panel import Panel
from rich import box
from rich.align import Align
import click
import yaml

console = Console()


def set_top_screen():
    click.echo("\033[H", nl=False)
def clear_screen():
    click.echo("\033[2J", nl=False)
