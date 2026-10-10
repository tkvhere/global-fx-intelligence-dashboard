import requests
from datetime import datetime, timedelta, timezone

from config import FRANKFURTER_BASE_URL, SUPPORTED_CURRENCIES

CACHE = {}
CACHE_TTL_SECONDS = 300


def _now_iso():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S%z')


def _cache_key(url):
    return url


def _get_cached(url):
    cache_entry = CACHE.get(url)
    if not cache_entry:
        return None
    if datetime.utcnow().timestamp() - cache_entry["timestamp"] > CACHE_TTL_SECONDS:
        CACHE.pop(url, None)
        return None
    return cache_entry["payload"]


def _set_cache(url, payload):
    CACHE[url] = {"timestamp": datetime.now(timezone.utc).timestamp(), "payload": payload}


def _request_json(url):
    cached = _get_cached(url)
    if cached is not None:
        return cached

    response = requests.get(url, timeout=12)
    if response.status_code >= 400:
        raise RuntimeError(f"Frankfurter API request failed with status {response.status_code}: {response.text}")

    payload = response.json()
    _set_cache(url, payload)
    return payload


def normalize_base(base_currency):
    if not base_currency:
        raise ValueError("Base currency is required.")
    base_currency = base_currency.upper()
    if base_currency not in SUPPORTED_CURRENCIES:
        raise ValueError(f"Unsupported base currency: {base_currency}")
    return base_currency


def normalize_symbols(symbols):
    if not symbols:
        return list(SUPPORTED_CURRENCIES.keys())
    if isinstance(symbols, str):
        raw_symbols = [item.strip().upper() for item in symbols.split(',') if item and item.strip()]
    else:
        raw_symbols = [str(item).strip().upper() for item in symbols]
    filtered = [code for code in raw_symbols if code in SUPPORTED_CURRENCIES]
    return sorted(set(filtered), key=lambda x: list(SUPPORTED_CURRENCIES.keys()).index(x))


def get_latest_rates(base_currency='USD'):
    base_currency = normalize_base(base_currency)
    symbols = [code for code in SUPPORTED_CURRENCIES if code != base_currency]
    url = f"{FRANKFURTER_BASE_URL}/latest?from={base_currency}&to={','.join(symbols)}"
    payload = _request_json(url)
    rates = payload.get('rates', {})
    data = {
        'base': base_currency,
        'date': payload.get('date'),
        'source': 'Frankfurter API',
        'rates': {code: float(value) for code, value in rates.items() if code in SUPPORTED_CURRENCIES},
    }
    return data


def get_snapshot_for_pair(base_currency, target_currency):
    base_currency = normalize_base(base_currency)
    target_currency = target_currency.upper()
    if target_currency not in SUPPORTED_CURRENCIES:
        raise ValueError(f"Unsupported target currency: {target_currency}")
    if base_currency == target_currency:
        return {'base': base_currency, 'target': target_currency, 'rate': 1.0, 'date': datetime.now(timezone.utc).strftime('%Y-%m-%d'), 'source': 'Frankfurter API'}
    url = f"{FRANKFURTER_BASE_URL}/latest?from={base_currency}&to={target_currency}"
    payload = _request_json(url)
    rate = payload.get('rates', {}).get(target_currency)
    if rate is None:
        raise ValueError(f"No rate available for {base_currency} to {target_currency}.")
    return {
        'base': base_currency,
        'target': target_currency,
        'rate': float(rate),
        'date': payload.get('date'),
        'source': 'Frankfurter API',
    }


def get_historical_rates(base_currency='USD', symbols=None, days=90):
    base_currency = normalize_base(base_currency)
    selected_symbols = normalize_symbols(symbols or [code for code in SUPPORTED_CURRENCIES if code != base_currency])
    if days < 1:
        raise ValueError("days must be at least 1.")
    end_date = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    start_date = (datetime.now(timezone.utc) - timedelta(days=days)).strftime('%Y-%m-%d')
    url = f"{FRANKFURTER_BASE_URL}/{start_date}..{end_date}?from={base_currency}&to={','.join(selected_symbols)}"
    payload = _request_json(url)
    records = []
    for date_str, rate_map in sorted(payload.get('rates', {}).items()):
        entry = {'date': date_str, 'rates': {}} 
        for code in selected_symbols:
            value = rate_map.get(code)
            if value is not None:
                entry['rates'][code] = float(value)
        if entry['rates']:
            records.append(entry)
    return {
        'base': base_currency,
        'symbols': selected_symbols,
        'days': days,
        'source': 'Frankfurter API',
        'rates': records,
        'from': start_date,
        'to': end_date,
    }


def export_historical_csv(base_currency, target_currency, days=365, csv_path=None):
    data = get_historical_rates(base_currency=base_currency, symbols=[target_currency], days=days)
    records = []
    for item in data['rates']:
        rate_value = item.get('rates', {}).get(target_currency)
        if rate_value is not None:
            records.append({'date': item['date'], 'rate': float(rate_value)})
    if not records:
        return []
    import os
    from pathlib import Path

    target_dir = Path(csv_path) if csv_path else Path(__file__).resolve().parents[1] / 'data'
    if not target_dir.exists():
        target_dir.mkdir(parents=True, exist_ok=True)
    file_path = target_dir / f'{base_currency}_{target_currency}_historical.csv'
    import pandas as pd
    df = pd.DataFrame(records).sort_values('date')
    df.to_csv(file_path, index=False)
    return records
