import json

from services.historical_service import build_pair_summary
from services.volatility_service import compute_volatility


class FakeResponse:
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code
        self.text = json.dumps(payload)

    def json(self):
        return self._payload


def test_percentage_change_calculation(monkeypatch):
    payload = {
        'rates': {
            '2024-01-01': {'INR': 80.0},
            '2024-01-02': {'INR': 81.0},
            '2024-01-03': {'INR': 83.0},
        }
    }
    monkeypatch.setattr('requests.get', lambda *args, **kwargs: FakeResponse(payload))
    summary = build_pair_summary('USD', 'INR', days=30)
    expected = ((summary['latest_rate'] - summary['start_rate']) / summary['start_rate']) * 100
    assert abs(summary['percentage_change'] - expected) < 1e-6


def test_volatility_calculation():
    rates = [100.0, 101.0, 99.5, 103.0, 102.0]
    result = compute_volatility(rates)
    assert result['volatility_pct'] is not None
    assert 'Low volatility' in result['classification'] or 'Moderate volatility' in result['classification'] or 'High volatility' in result['classification']
