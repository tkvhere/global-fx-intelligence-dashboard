import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

from ml.data_preprocessing import fetch_pair_dataframe, validate_chronological_split
from ml.evaluation import compute_mae, compute_mape, compute_rmse
from ml.feature_engineering import engineer_features


def train_model_for_pair(base_currency='USD', target_currency='INR', days=365):
    raw_df = fetch_pair_dataframe(base_currency=base_currency, target_currency=target_currency, days=days)
    raw_df = validate_chronological_split(raw_df)
    feature_df = engineer_features(raw_df)
    feature_columns = [col for col in feature_df.columns if col not in {'date', 'target'}]
    X = feature_df[feature_columns]
    y = feature_df['target']

    split_index = max(2, int(len(X) * 0.8))
    X_train = X.iloc[:split_index]
    X_test = X.iloc[split_index:]
    y_train = y.iloc[:split_index]
    y_test = y.iloc[split_index:]

    model = LinearRegression()
    model.fit(X_train, y_train)
    train_predictions = model.predict(X_train)
    test_predictions = model.predict(X_test)

    mae = compute_mae(y_test, test_predictions)
    rmse = compute_rmse(y_test, test_predictions)
    mape = compute_mape(y_test, test_predictions)
    baseline_predictions = np.full(len(y_test), float(y_train.iloc[-1]))
    baseline_mae = compute_mae(y_test, baseline_predictions)
    baseline_rmse = compute_rmse(y_test, baseline_predictions)

    result = {
        'base': base_currency,
        'target': target_currency,
        'model_name': 'LinearRegression',
        'days': days,
        'feature_columns': feature_columns,
        'training_start': raw_df['date'].min().strftime('%Y-%m-%d'),
        'training_end': raw_df['date'].max().strftime('%Y-%m-%d'),
        'train_size': len(X_train),
        'test_size': len(X_test),
        'metrics': {
            'mae': mae,
            'rmse': rmse,
            'mape': mape,
            'baseline_mae': baseline_mae,
            'baseline_rmse': baseline_rmse,
        },
        'model': model,
        'feature_df': feature_df,
        'X_train': X_train,
        'X_test': X_test,
        'y_train': y_train,
        'y_test': y_test,
        'test_predictions': test_predictions,
        'train_predictions': train_predictions,
    }
    return result
