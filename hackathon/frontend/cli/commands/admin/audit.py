# cli/commands/admin/audit.py

import typer
from rich import print
from cli.client import get

app = typer.Typer(help="Admin - Audit logs")

@app.command("show")
def show():
    resp = get("/admin/audit")
    print(resp.json())
