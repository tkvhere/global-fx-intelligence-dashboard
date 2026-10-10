from datetime import datetime, timezone

from services.exchange_rate_service import get_snapshot_for_pair


def convert_amount(amount, from_currency, to_currency):
    try:
        numeric_amount = float(amount)
    except (TypeError, ValueError):
        raise ValueError('Amount must be a valid number.')

    if numeric_amount < 0:
        raise ValueError('Amount must be zero or positive.')

    from_currency = str(from_currency).upper()
    to_currency = str(to_currency).upper()

    if from_currency == to_currency:
        return {
            'from': from_currency,
            'to': to_currency,
            'amount': numeric_amount,
            'converted_amount': numeric_amount,
            'rate': 1.0,
            'date': datetime.now(timezone.utc).strftime('%Y-%m-%d'),
            'source': 'Frankfurter API',
        }

    snapshot = get_snapshot_for_pair(from_currency, to_currency)
    converted = numeric_amount * snapshot['rate']
    return {
        'from': from_currency,
        'to': to_currency,
        'amount': numeric_amount,
        'converted_amount': converted,
        'rate': snapshot['rate'],
        'date': snapshot['date'],
        'source': snapshot['source'],
    }
