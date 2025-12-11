# cli/commands/me.py

import typer
from rich import print
from cli.client import get

app = typer.Typer(help="User info commands")

@app.command()
def info():
    """
    Show current user details.
    """
    resp = get("/me")
    print(resp.json())
