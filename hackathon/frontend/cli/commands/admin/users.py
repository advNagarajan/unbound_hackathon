# cli/commands/admin/users.py

import typer
from rich import print
from cli.client import get, post

app = typer.Typer(help="Admin - User management")


@app.command("create")
def create_user(username: str, role: str = "member", credits: int = 100):
    resp = post("/admin/users", json={
        "username": username,
        "role": role,
        "credits": credits
    })
    print(resp.json())


@app.command("list")
def list_users():
    resp = get("/admin/users")
    print(resp.json())


@app.command("credits")
def set_credits(user_id: int, credits: int):
    resp = post(f"/admin/users/{user_id}/credits", json={"credits": credits})
    print(resp.json())
