import numpy as np
import pandas as pd

from ml.data_preprocessing import validate_chronological_split
from ml.feature_engineering import engineer_features
from ml.forecast_service import recursive_forecast


def test_time_series_preprocessing_keeps_chronological_order():
    df = pd.DataFrame(
        {
            'date': pd.date_range('2024-01-01', periods=12, freq='D'),
            'rate': [82.0, 82.2, 82.5, 82.7, 83.1, 82.9, 83.4, 83.7, 84.0, 84.2, 84.5, 84.8],
        }
    )
    prepared = validate_chronological_split(df)
    assert prepared['date'].is_monotonic_increasing
    assert len(prepared) == 12
    feature_df = engineer_features(prepared)
    assert 'lag_1' in feature_df.columns
    assert 'target' in feature_df.columns
    assert len(feature_df) == 11


def test_recursive_forecast_uses_model_feature_names():
    class DummyModel:
        def predict(self, features):
            return np.full(len(features), 84.5)

    forecast = recursive_forecast(DummyModel(), [80.0, 81.0, 82.0, 83.0, 84.0], horizon=2)
    assert len(forecast) == 2
    assert np.allclose(forecast, [84.5, 84.5])
