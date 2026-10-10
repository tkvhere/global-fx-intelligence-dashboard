from datetime import datetime, timezone

from database.db import get_connection


def create_alert(currency_pair, threshold, direction, enabled=True):
    pair = str(currency_pair).upper().replace(' ', '')
    if '/' not in pair:
        raise ValueError('Currency pair must be in the format "USD/INR".')
    if direction not in {'above', 'below'}:
        raise ValueError('Direction must be "above" or "below".')
    try:
        threshold_value = float(threshold)
    except (TypeError, ValueError):
        raise ValueError('Threshold must be numeric.')

    with get_connection() as conn:
        duplicate = conn.execute(
            'SELECT id FROM alerts WHERE currency_pair = ? AND ABS(threshold - ?) < 0.000001 AND direction = ? LIMIT 1',
            (pair, threshold_value, direction),
        ).fetchone()
        if duplicate is not None:
            raise ValueError(f'Duplicate alert already exists for {pair} at {threshold_value:.2f} {direction}.')

        cursor = conn.execute(
            'INSERT INTO alerts (currency_pair, threshold, direction, enabled, created_at) VALUES (?, ?, ?, ?, ?)',
            (pair, threshold_value, direction, int(bool(enabled)), datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S%z')),
        )
        conn.commit()
        return {'id': cursor.lastrowid, 'currency_pair': pair, 'threshold': threshold_value, 'direction': direction, 'enabled': bool(enabled)}


def list_alerts():
    with get_connection() as conn:
        rows = conn.execute('SELECT * FROM alerts ORDER BY id DESC').fetchall()
        return [dict(row) for row in rows]


def toggle_alert(alert_id, enabled):
    with get_connection() as conn:
        conn.execute('UPDATE alerts SET enabled = ? WHERE id = ?', (int(bool(enabled)), int(alert_id)))
        conn.commit()
        return {'id': int(alert_id), 'enabled': bool(enabled)}


def delete_alert(alert_id):
    with get_connection() as conn:
        conn.execute('DELETE FROM alerts WHERE id = ?', (int(alert_id),))
        conn.execute('DELETE FROM alert_events WHERE alert_id = ?', (int(alert_id),))
        conn.commit()
        return {'deleted': True, 'id': int(alert_id)}


def get_alert_history():
    with get_connection() as conn:
        rows = conn.execute('SELECT * FROM alert_events ORDER BY triggered_at DESC').fetchall()
        return [dict(row) for row in rows]


def evaluate_alerts_for_rate(currency_pair, rate_value):
    pair = str(currency_pair).upper().replace(' ', '')
    alerts = [row for row in list_alerts() if row['currency_pair'] == pair and row['enabled'] == 1]
    triggered = []
    for alert in alerts:
        threshold = float(alert['threshold'])
        direction = alert['direction']
        should_trigger = (direction == 'above' and rate_value > threshold) or (direction == 'below' and rate_value < threshold)
        if should_trigger:
            with get_connection() as conn:
                conn.execute(
                    'INSERT INTO alert_events (alert_id, pair, threshold, direction, observed_rate, triggered_at) VALUES (?, ?, ?, ?, ?, ?)',
                    (alert['id'], pair, threshold, direction, float(rate_value), datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S%z')),
                )
                conn.commit()
            triggered.append({
                'alert_id': alert['id'],
                'pair': pair,
                'threshold': threshold,
                'direction': direction,
                'observed_rate': float(rate_value),
                'triggered_at': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S%z'),
            })
    return triggered
