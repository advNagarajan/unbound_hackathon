# cli/commands/login.py

import typer
from rich import print
from cli.config import save_api_key

def login(api_key: str):
    """
    Store API key locally.
    """
    save_api_key(api_key)
    print("[green]API key saved![/green]")
