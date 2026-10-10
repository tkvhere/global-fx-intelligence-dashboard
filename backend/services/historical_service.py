from datetime import datetime

from services.exchange_rate_service import get_historical_rates


def build_pair_summary(base_currency='USD', target_currency='INR', days=90):
    payload = get_historical_rates(base_currency=base_currency, symbols=[target_currency], days=days)
    series = []
    for item in payload['rates']:
        value = item.get('rates', {}).get(target_currency)
        if value is not None:
            series.append({'date': item['date'], 'rate': float(value)})

    if len(series) < 2:
        return {
            'pair': f'{base_currency}/{target_currency}',
            'days': days,
            'source': payload['source'],
            'data_points': len(series),
            'start_rate': None,
            'latest_rate': None,
            'absolute_change': None,
            'percentage_change': None,
            'min_rate': None,
            'max_rate': None,
            'previous_rate': None,
            'daily_change_pct': None,
            'series': series,
        }

    start_rate = series[0]['rate']
    previous_rate = series[-2]['rate'] if len(series) >= 2 else start_rate
    latest_rate = series[-1]['rate']
    min_rate = min(item['rate'] for item in series)
    max_rate = max(item['rate'] for item in series)
    abs_change = latest_rate - start_rate
    pct_change = ((latest_rate - start_rate) / start_rate) * 100 if start_rate else 0.0
    daily_change_pct = ((latest_rate - previous_rate) / previous_rate) * 100 if previous_rate else 0.0

    return {
        'pair': f'{base_currency}/{target_currency}',
        'days': days,
        'source': payload['source'],
        'data_points': len(series),
        'start_rate': start_rate,
        'latest_rate': latest_rate,
        'absolute_change': abs_change,
        'percentage_change': pct_change,
        'min_rate': min_rate,
        'max_rate': max_rate,
        'previous_rate': previous_rate,
        'daily_change_pct': daily_change_pct,
        'period_start': series[0]['date'],
        'period_end': series[-1]['date'],
        'series': series,
    }


def get_daily_percentage_change(base_currency='USD', target_currency='INR', days=30):
    payload = get_historical_rates(base_currency=base_currency, symbols=[target_currency], days=days)
    series = []
    for item in payload['rates']:
        rate_value = item.get('rates', {}).get(target_currency)
        if rate_value is not None:
            series.append({'date': item['date'], 'rate': float(rate_value)})
    if len(series) < 2:
        return {'pair': f'{base_currency}/{target_currency}', 'changes': [], 'source': payload['source']}

    changes = []
    for idx in range(1, len(series)):
        prev = series[idx - 1]['rate']
        curr = series[idx]['rate']
        changes.append({
            'date': series[idx]['date'],
            'previous_rate': prev,
            'current_rate': curr,
            'change_pct': ((curr - prev) / prev) * 100 if prev else 0.0,
        })
    return {'pair': f'{base_currency}/{target_currency}', 'changes': changes, 'source': payload['source']}


def get_rates_table(base_currency='USD', target_currency='INR', days=90):
    summary = build_pair_summary(base_currency, target_currency, days)
    return {
        'pair': summary['pair'],
        'start_rate': summary['start_rate'],
        'latest_rate': summary['latest_rate'],
        'absolute_change': summary['absolute_change'],
        'percentage_change': summary['percentage_change'],
        'min_rate': summary['min_rate'],
        'max_rate': summary['max_rate'],
        'source': summary['source'],
        'records': summary['series'],
    }
