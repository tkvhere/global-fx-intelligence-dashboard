import numpy as np


def compute_mae(actual, predicted):
    actual_arr = np.asarray(actual, dtype=float)
    predicted_arr = np.asarray(predicted, dtype=float)
    return float(np.mean(np.abs(actual_arr - predicted_arr)))


def compute_rmse(actual, predicted):
    actual_arr = np.asarray(actual, dtype=float)
    predicted_arr = np.asarray(predicted, dtype=float)
    return float(np.sqrt(np.mean((actual_arr - predicted_arr) ** 2)))


def compute_mape(actual, predicted):
    actual_arr = np.asarray(actual, dtype=float)
    predicted_arr = np.asarray(predicted, dtype=float)
    mask = np.abs(actual_arr) > 0
    if not np.any(mask):
        return None
    return float(np.mean(np.abs((actual_arr[mask] - predicted_arr[mask]) / actual_arr[mask])) * 100)
