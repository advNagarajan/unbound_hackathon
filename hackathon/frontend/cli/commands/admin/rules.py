# cli/commands/admin/rules.py

import typer
from rich import print
from cli.client import get, post, delete

app = typer.Typer(help="Admin - Rule management")


@app.command("add")
def add_rule(pattern: str, action: str, priority: int):
    resp = post("/admin/rules", json={
        "pattern": pattern,
        "action": action,
        "priority": priority,
    })
    print(resp.json())


@app.command("list")
def list_rules():
    resp = get("/admin/rules")
    print(resp.json())


@app.command("delete")
def delete_rule(rule_id: int):
    resp = delete(f"/admin/rules/{rule_id}")
    print(resp.json())
