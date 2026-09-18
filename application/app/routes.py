from flask import Blueprint, abort, current_app, render_template

from .members import get_member, load_members

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return render_template("index.html", members=load_members())


@bp.route("/members/<username>")
def member(username):
    member = get_member(username)
    if member is None:
        abort(404)

    # A member may hand-write templates/members/<username>.html for full control
    # over their own page; otherwise their data is rendered with the shared layout.
    custom = f"members/{member['slug']}.html"
    template = custom if custom in current_app.jinja_env.list_templates() else "member.html"
    return render_template(template, member=member, members=load_members())
