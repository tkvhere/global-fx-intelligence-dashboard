from ml.forecast_service import generate_forecast as generate_ml_forecast, get_forecast_evaluation as get_ml_forecast_evaluation


def generate_forecast(base_currency='USD', target_currency='INR', horizon=7, days=365):
    return generate_ml_forecast(base_currency=base_currency, target_currency=target_currency, horizon=horizon, days=days)


def get_forecast_evaluation(base_currency='USD', target_currency='INR', days=365):
    return get_ml_forecast_evaluation(base_currency=base_currency, target_currency=target_currency, days=days)
