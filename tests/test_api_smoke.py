from fastapi.testclient import TestClient

import main
from database_models import get_db
from services.aceai import PlayerProfile, Racquet, StringItem, genera_consulenza


client = TestClient(main.app)


def test_app_is_available():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "ACEAPP API is running!"


def test_database_dependency_yields_a_session():
    generator = get_db()
    session = next(generator)
    assert session is not None
    generator.close()


def test_sensitive_write_endpoints_require_a_token():
    requests = [
        ("/prodotti/", {"nome": "Test"}),
        (
            "/negozi/",
            {"nome": "Test Tennis", "citta": "Roma"},
        ),
        (
            "/dashboard/registra-richiesta",
            {
                "negozio_id": 1,
                "negozio_citta": "Roma",
                "prodotto_tipo": "racchetta",
                "prodotto_nome": "Test",
            },
        ),
        (
            "/evolution/salva",
            {
                "nome_utente": "Ignorato",
                "livello": "intermedio",
                "racchetta": "Test",
                "corda": "Test",
                "tensione_main": 23,
                "tensione_cross": 22,
                "superficie": "cemento",
            },
        ),
    ]

    for path, payload in requests:
        assert client.post(path, json=payload).status_code == 401


def test_aceai_match_generates_a_score():
    result = genera_consulenza(
        PlayerProfile(level="intermediate", style="aggressivo"),
        [Racquet("Test", "R1", 65, "16x19", 23, 300)],
        [StringItem("S1", "poly")],
    )
    assert result["profilo"]["score_profilo"] == 62.5
