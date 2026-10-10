from database.db import get_connection
from services.alert_service import create_alert, evaluate_alerts_for_rate, list_alerts


def reset_alerts():
    with get_connection() as conn:
        conn.execute('DELETE FROM alert_events')
        conn.execute('DELETE FROM alerts')
        conn.commit()


def setup_function():
    reset_alerts()


def teardown_function():
    reset_alerts()


def test_alert_creation_and_threshold_logic():
    alert = create_alert('USD/INR', 85.0, 'above', enabled=True)
    assert alert['currency_pair'] == 'USD/INR'
    assert alert['threshold'] == 85.0
    triggered = evaluate_alerts_for_rate('USD/INR', 86.0)
    assert triggered and triggered[0]['direction'] == 'above'
    alerts = list_alerts()
    assert any(item['currency_pair'] == 'USD/INR' for item in alerts)


def test_duplicate_alert_rejected():
    try:
        create_alert('USD/INR', 85.0, 'above', enabled=True)
        create_alert('USD/INR', 85.0, 'above', enabled=True)
    except ValueError as exc:
        assert 'Duplicate' in str(exc)
    else:
        assert False, 'duplicate alert should be rejected'
