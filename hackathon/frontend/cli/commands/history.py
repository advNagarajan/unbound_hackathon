# cli/commands/history.py

import typer
from rich import print
from cli.client import get

app = typer.Typer(help="View your command history")

@app.command()
def show():
    resp = get("/commands")
    print(resp.json())
