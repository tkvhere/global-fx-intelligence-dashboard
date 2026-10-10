import json

from app import app
from services import exchange_rate_service


class FakeResponse:
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code
        self.text = json.dumps(payload)

    def json(self):
        return self._payload


def test_currencies_list():
    client = app.test_client()
    response = client.get('/api/currencies')
    assert response.status_code == 200
    payload = response.get_json()
    assert 'currencies' in payload
    assert len(payload['currencies']) >= 10


def test_rates_endpoint(monkeypatch):
    exchange_rate_service.CACHE.clear()

    payload = {
        'amount': 1,
        'base': 'USD',
        'date': '2026-10-10',
        'rates': {'EUR': 0.92, 'INR': 83.5, 'JPY': 150.2}
    }

    monkeypatch.setattr('requests.get', lambda *args, **kwargs: FakeResponse(payload))
    client = app.test_client()
    response = client.get('/api/rates?base=USD')
    assert response.status_code == 200
    data = response.get_json()
    assert data['base'] == 'USD'
    assert 'INR' in data['rates']
    assert data['rates']['EUR'] == 0.92
