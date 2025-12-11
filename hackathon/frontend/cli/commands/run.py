# cli/commands/run.py

import typer
from rich import print
from cli.client import post

app = typer.Typer(help="Run commands through the gateway")

@app.command()
def cmd(command: str):
    """
    Submit a command for execution.
    """
    resp = post("/commands", json={"command_text": command})
    print(resp.json())
