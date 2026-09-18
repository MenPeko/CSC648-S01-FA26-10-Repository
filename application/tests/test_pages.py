import pytest

from app import create_app
from app.members import load_members


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Meet Team 10" in response.data


def test_home_page_links_every_member(client):
    body = client.get("/").get_data(as_text=True)
    for member in load_members():
        assert f"/members/{member['slug']}" in body


@pytest.mark.parametrize("member", load_members(), ids=lambda m: m["slug"])
def test_member_page_shows_name_and_image(client, member):
    response = client.get(f"/members/{member['slug']}")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert member["name"] in body
    assert "<img" in body


def test_member_lookup_is_case_insensitive(client):
    assert client.get("/members/MenPeko").status_code == 200


def test_unknown_member_returns_404(client):
    assert client.get("/members/not-a-real-user").status_code == 404
