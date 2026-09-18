"""Loads team member data.

Each member owns exactly one file in application/members/, named after their
GitHub username in lowercase. Nobody has to edit a shared list, so individual
pages can be developed on separate branches and merged without conflicts.
"""

import json

from . import PROJECT_DIR

MEMBERS_DIR = PROJECT_DIR / "members"

DEFAULT_PHOTO = "img/default-avatar.svg"


def _load_one(path):
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)

    username = data.get("github") or path.stem
    photo = data.get("photo")

    return {
        "slug": path.stem.lower(),
        "name": data.get("name", username),
        "github": username,
        "email": data.get("email", ""),
        "role": data.get("role", ""),
        "headline": data.get("headline", ""),
        "bio": data.get("bio", ""),
        "photo": f"img/members/{photo}" if photo else DEFAULT_PHOTO,
        "photo_alt": data.get("photo_alt") or f"Photo of {data.get('name', username)}",
        "links": data.get("links", {}),
        "order": data.get("order", 99),
    }


def load_members():
    """Return every member, ordered by their "order" field then name."""
    if not MEMBERS_DIR.is_dir():
        return []

    members = [_load_one(path) for path in MEMBERS_DIR.glob("*.json")]
    members.sort(key=lambda member: (member["order"], member["name"].lower()))
    return members


def get_member(slug):
    """Return one member by URL slug, or None. Lookup is case-insensitive."""
    slug = slug.lower()
    for member in load_members():
        if member["slug"] == slug:
            return member
    return None
