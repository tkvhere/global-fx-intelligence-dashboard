import pandas as pd

from ml.train_model import train_model_for_pair


DEFAULT_FEATURE_COLUMNS = [
    'rate',
    'lag_1', 'lag_2', 'lag_3', 'lag_5', 'lag_10',
    'rolling_mean_3', 'rolling_mean_5', 'rolling_mean_7',
    'rolling_std_3', 'rolling_std_5', 'rolling_std_7',
    'pct_change', 'diff_1',
]


def recursive_forecast(model, series, horizon=7):
    prediction_values = list(series)
    if len(prediction_values) < 2:
        raise ValueError('Not enough observations for forecasting.')

    feature_names = list(getattr(model, 'feature_names_in_', DEFAULT_FEATURE_COLUMNS))
    if not feature_names:
        feature_names = DEFAULT_FEATURE_COLUMNS.copy()

    for _ in range(horizon):
        df = pd.DataFrame({'rate': prediction_values})
        for lag in [1, 2, 3, 5, 10]:
            df[f'lag_{lag}'] = df['rate'].shift(lag)
        for window in [3, 5, 7]:
            df[f'rolling_mean_{window}'] = df['rate'].rolling(window).mean()
            df[f'rolling_std_{window}'] = df['rate'].rolling(window).std().fillna(0)
        df['pct_change'] = df['rate'].pct_change().fillna(0)
        df['diff_1'] = df['rate'].diff().fillna(0)
        last_row = df.iloc[-1].to_dict()
        features = pd.DataFrame([
            {col: last_row.get(col, 0.0) for col in feature_names}
        ], columns=feature_names)
        next_value = float(model.predict(features)[0])
        prediction_values.append(next_value)
    return prediction_values[-horizon:]


def generate_forecast(base_currency='USD', target_currency='INR', horizon=7, days=365):
    training = train_model_for_pair(base_currency=base_currency, target_currency=target_currency, days=days)
    model = training['model']
    raw_prices = training['feature_df']['rate'].tolist()
    actual_test = training['y_test'].tolist()
    test_predictions = training['test_predictions'].tolist()
    future_values = recursive_forecast(model, raw_prices, horizon=horizon)

    metrics = {
        'mae': float(training['metrics']['mae']),
        'rmse': float(training['metrics']['rmse']),
        'mape': training['metrics']['mape'],
        'baseline_mae': float(training['metrics']['baseline_mae']),
        'baseline_rmse': float(training['metrics']['baseline_rmse']),
    }

    return {
        'base': base_currency,
        'target': target_currency,
        'model_name': training['model_name'],
        'horizon': horizon,
        'training_start': training['training_start'],
        'training_end': training['training_end'],
        'source': 'Frankfurter API',
        'training_observations': len(training['feature_df']),
        'test_observations': len(actual_test),
        'actual_test_values': actual_test,
        'predicted_test_values': test_predictions,
        'future_forecast': future_values,
        'metrics': metrics,
        'warning': 'This model is educational only and does not guarantee future exchange-rate movements.',
    }


def get_forecast_evaluation(base_currency='USD', target_currency='INR', days=365):
    training = train_model_for_pair(base_currency=base_currency, target_currency=target_currency, days=days)
    return {
        'base': base_currency,
        'target': target_currency,
        'model_name': training['model_name'],
        'training_start': training['training_start'],
        'training_end': training['training_end'],
        'source': 'Frankfurter API',
        'metrics': {
            'mae': float(training['metrics']['mae']),
            'rmse': float(training['metrics']['rmse']),
            'mape': training['metrics']['mape'],
            'baseline_mae': float(training['metrics']['baseline_mae']),
            'baseline_rmse': float(training['metrics']['baseline_rmse']),
        },
        'n_test': len(training['y_test']),
        'warning': 'Forecasts are educational and not financial advice.',
    }
