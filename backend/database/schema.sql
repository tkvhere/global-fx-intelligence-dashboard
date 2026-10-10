CREATE TABLE IF NOT EXISTS exchange_rate_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    base_currency TEXT NOT NULL,
    target_currency TEXT NOT NULL,
    rate_value REAL NOT NULL,
    observation_date TEXT NOT NULL,
    source TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_snapshot_currency_date ON exchange_rate_snapshots(base_currency, target_currency, observation_date);

CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    currency_pair TEXT NOT NULL,
    threshold REAL NOT NULL,
    direction TEXT NOT NULL CHECK(direction IN ('above', 'below')),
    enabled INTEGER NOT NULL DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

DELETE FROM alerts
WHERE id NOT IN (
    SELECT MIN(id)
    FROM alerts
    GROUP BY currency_pair, threshold, direction
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_alerts_unique_pair_threshold_direction
ON alerts(currency_pair, threshold, direction);

CREATE INDEX IF NOT EXISTS idx_alerts_pair_enabled ON alerts(currency_pair, enabled);

CREATE TABLE IF NOT EXISTS alert_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alert_id INTEGER NOT NULL,
    pair TEXT NOT NULL,
    threshold REAL NOT NULL,
    direction TEXT NOT NULL,
    observed_rate REAL NOT NULL,
    triggered_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(alert_id) REFERENCES alerts(id)
);

CREATE INDEX IF NOT EXISTS idx_alert_events_pair_time ON alert_events(pair, triggered_at);

CREATE TABLE IF NOT EXISTS forecast_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_name TEXT NOT NULL,
    base_currency TEXT NOT NULL,
    target_currency TEXT NOT NULL,
    forecast_horizon INTEGER NOT NULL,
    training_start TEXT,
    training_end TEXT,
    model_date TEXT DEFAULT CURRENT_TIMESTAMP,
    mae REAL,
    rmse REAL,
    mape REAL,
    baseline_mae REAL,
    baseline_rmse REAL,
    dataset_points INTEGER,
    source TEXT
);

CREATE INDEX IF NOT EXISTS idx_forecast_runs_pair ON forecast_runs(base_currency, target_currency, model_date);
