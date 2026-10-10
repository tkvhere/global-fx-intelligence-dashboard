import os
from pathlib import Path

import pandas as pd

from config import DATA_DIR
from services.exchange_rate_service import get_historical_rates


def fetch_pair_dataframe(base_currency='USD', target_currency='INR', days=365):
    if base_currency == target_currency:
        return pd.DataFrame({'date': [], 'rate': []})
    payload = get_historical_rates(base_currency=base_currency, symbols=[target_currency], days=days)
    rows = []
    for item in payload.get('rates', []):
        rate_value = item.get('rates', {}).get(target_currency)
        if rate_value is not None:
            rows.append({'date': item['date'], 'rate': float(rate_value)})
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').drop_duplicates(subset='date').dropna().reset_index(drop=True)
    os.makedirs(DATA_DIR, exist_ok=True)
    csv_path = Path(DATA_DIR) / f'{base_currency}_{target_currency}_history.csv'
    df.to_csv(csv_path, index=False)
    return df


def validate_chronological_split(df):
    if df is None or df.empty:
        raise ValueError('Historical dataset is empty. Need more data for forecasting.')
    if len(df) < 10:
        raise ValueError('Insufficient historical data to train a forecasting model.')
    if df['date'].is_monotonic_increasing is False:
        df = df.sort_values('date').reset_index(drop=True)
    return df
