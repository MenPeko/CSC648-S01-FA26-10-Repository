import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, render_template

APP_DIR = Path(__file__).resolve().parent
PROJECT_DIR = APP_DIR.parent
REPO_DIR = PROJECT_DIR.parent

TEAM = {
    "course": "Software Engineering (CSC 648)",
    "school": "San Francisco State University",
    "semester": "Fall 2026",
    "section": "01",
    "number": "10",
}


def create_app():
    # .env lives at the repository root and is never committed.
    load_dotenv(REPO_DIR / ".env")
    load_dotenv(PROJECT_DIR / ".env")

    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-do-not-use-in-production")
    app.config["TEAM"] = TEAM

    from .routes import bp

    app.register_blueprint(bp)

    @app.errorhandler(404)
    def not_found(error):
        return render_template("404.html"), 404

    @app.context_processor
    def inject_team():
        return {"team": TEAM}

    return app
