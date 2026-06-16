from fastapi.testclient import TestClient

from monitor_comunitario.api.main import app


def test_home_page_returns_public_frontend() -> None:
    with TestClient(app) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert "Monitor Comunitário Celesc" in response.text
    assert "Espaço para anúncio local" in response.text
    assert "Política de Privacidade" in response.text
    assert "accept_legal_terms" in response.text
    assert "consent-banner" in response.text


def test_static_stylesheet_is_served() -> None:
    with TestClient(app) as client:
        response = client.get("/static/styles.css")

    assert response.status_code == 200
    assert "--accent" in response.text


def test_public_config_is_served_without_secret_values() -> None:
    with TestClient(app) as client:
        response = client.get("/public/config")

    assert response.status_code == 200

    body = response.json()

    assert "ads_enabled" in body
    assert "analytics_enabled" in body
    assert "consent_required" in body
    assert "consent_version" in body


def test_privacy_policy_page_is_served() -> None:
    with TestClient(app) as client:
        response = client.get("/privacidade")

    assert response.status_code == 200
    assert "Política de Privacidade" in response.text
    assert "LGPD" in response.text


def test_terms_page_is_served() -> None:
    with TestClient(app) as client:
        response = client.get("/termos")

    assert response.status_code == 200
    assert "Termos de Uso" in response.text


def test_cookie_policy_page_is_served() -> None:
    with TestClient(app) as client:
        response = client.get("/cookies")

    assert response.status_code == 200
    assert "Armazenamento Local" in response.text
    assert "ADS_ENABLED" in response.text
