import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "global_fx.db")
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")

SUPPORTED_CURRENCIES = {
    "USD": "US Dollar",
    "EUR": "Euro",
    "GBP": "British Pound",
    "JPY": "Japanese Yen",
    "INR": "Indian Rupee",
    "AED": "UAE Dirham",
    "CHF": "Swiss Franc",
    "CNY": "Chinese Yuan",
    "AUD": "Australian Dollar",
    "CAD": "Canadian Dollar",
}

DEFAULT_BASE = "USD"
FRANKFURTER_BASE_URL = "https://api.frankfurter.app"
ALLOWED_BASES = tuple(SUPPORTED_CURRENCIES.keys())
