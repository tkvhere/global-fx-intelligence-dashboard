# Database Design

## Schema overview

The SQLite database is initialized through the schema definition in the backend database package. It supports persistence for alerts, snapshots, and forecasting metadata.

## Entities

### alerts
Stores the alert configuration for each rule, including:

- alert id
- currency pair
- threshold value
- direction (above or below)
- enabled flag
- creation and update timestamps

### alert_events
Logs each alert-trigger event so the system can track when rate thresholds were crossed.

### exchange_rate_snapshots
Stores historical market data derived from the exchange service. This supports analytics, trend calculations, and reproducible evaluation.

### forecast_runs
Captures forecast generation details such as pair, horizon, model metadata, and metrics output.

## Design rationale

The database is intentionally lightweight and low complexity, which makes it suitable for a coursework project while still enabling meaningful persistence and alert tracking.

## Example model flow

1. User creates an alert for `USD/INR` above threshold.
2. Backend validates input and inserts a record into the alerts table.
3. market data is refreshed from the FX API.
4. alert evaluation compares the current rate with the threshold.
5. Matching events are recorded in the alert event log.
