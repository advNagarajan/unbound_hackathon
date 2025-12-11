🚀 Command Gateway

A security-focused command execution gateway where users submit shell-like commands that are validated against admin-defined rules. Safe commands execute automatically. Dangerous commands are blocked. Everything is tracked with credits, audit logs, and API-key authentication.

This project includes:

Backend API (FastAPI + SQLAlchemy + SQLite)

CLI Frontend (Typer)

Rule Engine with regex matching

User Credits System

Mock Command Execution

Full Audit Trail

API Key Authentication

⚠️ NOTE: This version includes Phases 1–4 only.
Approval workflows, voting thresholds, and email notifications are not included yet.

🧱 Architecture Overview
backend/
    app/
        main.py
        db.py
        models.py
        schemas.py
        auth.py
        routers/
        services/
frontend/
    cli/
        app.py
        commands/
        config.py


The backend exposes REST endpoints that enforce rule-based command validation, user credits, and auditing.
The frontend is a Python-based CLI that interacts with the backend using API keys.

🔐 Authentication

Every request includes:

Authorization: ApiKey <user_api_key>


No login session, no passwords — purely API-key-based identity.

🧑‍💼 User Roles
Role	Permissions
member	Submit commands, check credits, view history
admin	Everything members can do plus: manage rules, users, credits, and audit logs
💰 Credit System

Each user has a credit balance.

Submitting a command costs 1 credit (only on successful execution).

Commands are rejected if credits = 0.

📏 Rule Engine

Admins configure regex-based rules:

Pattern	Action	Example
`:(){ :	:& };:`	AUTO_REJECT
rm\s+-rf\s+/	AUTO_REJECT	rm -rf /
`git\s+(status	log	diff)`
`^(ls	cat	pwd

The engine performs first-match-wins.

Actions:

AUTO_ACCEPT → execute immediately

AUTO_REJECT → reject immediately

Execution is mocked (no real shell commands run).

📜 Audit Logging

Every important action is logged:

Command submissions

Rejections

Executions

Admin actions (rule creation, user creation, credit updates)

Logs are viewable only by admins.

💻 CLI Usage

All commands use:

python -m cli.app <command> ...

▶️ 1. Login (store API key)
gateway login <API_KEY>


Stores your API key in:

~/.gateway/config.json

▶️ 2. View your identity
gateway me

▶️ 3. Run a command
gateway run "ls -la"

▶️ 4. View history
gateway history

▶️ 5. Admin – List users
gateway admin users list

▶️ 6. Admin – Create user
gateway admin users create <username> --email <email> --role member --credits 100

▶️ 7. Admin – List rules
gateway admin rules list

▶️ 8. Admin – Create rule
gateway admin rules add "<regex>" <ACTION> --priority <n>


Example:

gateway admin rules add "docker .*" AUTO_REJECT --priority 10

▶️ 9. Admin – View audit logs
gateway admin audit list

🛠️ Running the Backend
1. Create virtual environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

2. Install dependencies
pip install -r requirements.txt

3. Start FastAPI server
uvicorn app.main:app --reload

4. Database is created automatically

A default admin user and default rule set are seeded on first startup.

🖥️ Running the CLI

Go to:

frontend/cli


Run any command:

python -m cli.app --help


Login first:

python -m cli.app login <ADMIN_OR_USER_API_KEY>

🧪 Testing (Phase 1–4)

Start backend

Seeded admin appears in terminal with API key

Login using CLI

Create a member user

Login as member

Submit commands

Check history

Login as admin

Create rules

Run commands that trigger AUTO_REJECT

Run commands that trigger AUTO_ACCEPT

Everything should work end-to-end.

🧩 Project Status
✔ Phase 1 — Infrastructure + Models
✔ Phase 2 — Rule Engine, Credits, Command Execution
✔ Phase 3 — Admin Management
✔ Phase 4 — CLI Frontend
⏳ Phase 5 — Coming soon

REQUIRE_APPROVAL

Multi-vote thresholds

Email notifications

Approval dashboard

📦 Future Extensions

User profiles

Full approval workflow

Web dashboard (React / Vue)

Time-based rule scheduling

Multi-tier approval logic

Deployment to Render / Railway / AWS

Postgres migration

🏁 Final Notes

This project simulates real-world secure command execution systems like:

CI/CD approval gates

Shell command firewalls

Banking authorization flows

Cloud consoles with protective rules

It is fully functional through Phase 4, with clean code, a CLI, and a safe backend.

