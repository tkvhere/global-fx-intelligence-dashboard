import pandas as pd


def engineer_features(df):
    if df is None or df.empty:
        raise ValueError('Feature engineering requires a non-empty dataset.')

    df = df.copy()
    df = df.sort_values('date').reset_index(drop=True)
    for lag in [1, 2, 3, 5, 10]:
        df[f'lag_{lag}'] = df['rate'].shift(lag).bfill()
    for window in [3, 5, 7]:
        df[f'rolling_mean_{window}'] = df['rate'].rolling(window).mean().bfill()
        df[f'rolling_std_{window}'] = df['rate'].rolling(window).std().fillna(0)
    df['pct_change'] = df['rate'].pct_change().fillna(0)
    df['diff_1'] = df['rate'].diff().fillna(0)
    df['target'] = df['rate'].shift(-1)
    df = df.dropna(subset=['lag_1', 'target']).reset_index(drop=True)
    return df
