import numpy as np


def compute_volatility(rate_series):
    if rate_series is None or len(rate_series) < 2:
        return {
            'window': len(rate_series) if rate_series else 0,
            'volatility_pct': None,
            'annualized_volatility_pct': None,
            'classification': 'Insufficient data',
            'explanation': 'At least two observations are required to estimate volatility.',
            'warning': 'Historical volatility does not guarantee future volatility.',
        }

    series = np.array(rate_series, dtype=float)
    returns = ((series[1:] / series[:-1]) - 1.0) * 100.0
    if len(returns) < 2:
        return {
            'window': len(series),
            'volatility_pct': None,
            'annualized_volatility_pct': None,
            'classification': 'Insufficient data',
            'explanation': 'More than one return observation is needed for a reliable volatility estimate.',
            'warning': 'Historical volatility does not guarantee future volatility.',
        }

    daily_std = float(np.std(returns, ddof=1) if len(returns) > 1 else np.std(returns))
    annualized = daily_std * np.sqrt(252)

    if annualized < 5:
        classification = 'Low volatility'
    elif annualized < 12:
        classification = 'Moderate volatility'
    else:
        classification = 'High volatility'

    return {
        'window': len(series),
        'volatility_pct': round(daily_std, 4),
        'annualized_volatility_pct': round(annualized, 4),
        'classification': classification,
        'explanation': 'Volatility is measured using percentage returns: ((Rate_t / Rate_(t-1)) - 1) * 100. Daily return standard deviation is annualized using sqrt(252).',
        'warning': 'Historical volatility does not guarantee future volatility.',
    }
