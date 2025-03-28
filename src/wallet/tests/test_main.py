from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_read_wallets():
    response = client.get("/api/v1/wallet/")
    assert response.status_code == 200


def test_read_wallet_not_found():
    response = client.get("/api/v1/wallet/1")
    assert response.status_code == 404
    assert response.json() == {"msg": "Not Found."}


def test_create_wallet():
    new_wallet = {"wallet_address": "TCFLL5dx5ZJdKnWuesXxi1VPwjLVmWZZy9"}
    response = client.post("/api/v1/wallet/", json=new_wallet)
    assert response.status_code == 200
    assert response.json()["wallet_address"] == new_wallet["wallet_address"]

