# API Documentation

## Base URL

- Local development: `http://127.0.0.1:5000`

## Routes

### `GET /api/health`
Returns application status metadata.

Example response:

```json
{
  "status": "ok",
  "service": "Global FX Intelligence API",
  "version": "1.0.0"
}
```

### `GET /api/currencies`
Returns the supported currency list and default base currency.

### `GET /api/rates`
Fetches the latest FX rates for a base currency.

Query parameters:

- `base`: base currency code, defaults to `USD`

### `GET /api/rates/history`
Fetches historical exchange-rate data for a pair or set of symbols.

### `GET /api/convert`
Converts an amount from one currency to another.

Query parameters:

- `from`: source currency
- `to`: target currency
- `amount`: numeric amount

### `GET /api/analytics`
Returns summary metrics and daily percentage change for a pair.

### `GET /api/volatility`
Calculates volatility for a selected pair over a date window.

### `GET /api/forecast`
Generates a forecast for a selected currency pair.

### `GET /api/forecast/evaluation`
Returns forecast evaluation metrics for the pair.

### `GET /api/alerts`
Returns active alerts and historical alert records.

### `POST /api/alerts`
Creates a new alert.

### `PATCH /api/alerts/<id>`
Toggles the enabled state of an alert.

### `DELETE /api/alerts/<id>`
Deletes an alert.

## Response conventions

The API uses JSON response objects with standard HTTP status codes and descriptive error payloads when validation or provider errors occur.
