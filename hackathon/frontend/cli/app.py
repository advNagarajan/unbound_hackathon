import typer

from cli.commands.login import login as login_cmd
from cli.commands.me import app as me_app
from cli.commands.run import app as run_app
from cli.commands.history import app as history_app
from cli.commands.admin.users import app as admin_users_app
from cli.commands.admin.rules import app as admin_rules_app
from cli.commands.admin.audit import app as admin_audit_app

app = typer.Typer()

# Register simple commands
app.command()(login_cmd)

# Register Typer sub-apps
app.add_typer(me_app, name="me")
app.add_typer(run_app, name="run")
app.add_typer(history_app, name="history")

admin_app = typer.Typer()
admin_app.add_typer(admin_users_app, name="users")
admin_app.add_typer(admin_rules_app, name="rules")
admin_app.add_typer(admin_audit_app, name="audit")

app.add_typer(admin_app, name="admin")


def main():
    app()


if __name__ == "__main__":
    main()
