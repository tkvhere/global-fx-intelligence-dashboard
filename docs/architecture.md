# Architecture Documentation

## High-level system design

```mermaid
flowchart LR
    User[User] --> UI[React Dashboard]
    UI --> API[Flask API]
    API --> Service[Services Layer]
    Service --> Market[Frankfurter FX API]
    Service --> DB[(SQLite Database)]
    Service --> ML[Forecast Model Pipeline]
    ML --> Forecast[Forecast Results]
    DB --> Alerts[Alert Evaluation]
```

## Layer description

### Presentation layer
The React frontend is a single-page dashboard with navigation sections for overview, rates, analytics, forecasting, and alerts.

### Application layer
Flask routes validate inputs, orchestrate calls to the service layer, and return JSON responses to the frontend.

### Data layer
SQLite stores exchange-rate snapshots, alert configuration, alert history, and forecast metadata. This supports persistent alert tracking and local auditability.

### ML layer
The forecasting service prepares time-series features, trains a linear regression model with chronological splitting, and produces prediction values with evaluation metrics.

## Design principles

- separation of concerns,
- stateless external API integration,
- modular service access,
- real-time dashboard responsiveness,
- maintainability through clear blueprint boundaries.

## Scalability note

The current solution is ideal for a local educational deployment. The architecture can be extended with caching, load balancing, and a production-grade database if the application is expanded for production use.

## UML Diagrams

### Use case diagram

```mermaid
flowchart LR
    actor[User] --> Overview[View exchange rates]
    actor --> Convert[Convert currencies]
    actor --> Analytics[Review historical analytics]
    actor --> Forecast[Run AI forecasting]
    actor --> Alerts[Create and manage alerts]

    Overview --> UI[React frontend]
    Convert --> UI
    Analytics --> UI
    Forecast --> UI
    Alerts --> UI

    UI --> API[Flask API]
    API --> Services[Service layer]
    Services --> Market[Frankfurter API]
    Services --> SQLite[(SQLite)]
    Services --> ML[ML forecasting pipeline]
```

### Component diagram

```mermaid
classDiagram
    class DashboardPage
    class Converter
    class RatesTable
    class CurrencyHeatmap
    class AlertsPanel
    class ExchangeRateChart
    class FlaskAPI
    class CurrencyRoutes
    class ForecastRoutes
    class ExchangeRateService
    class HistoricalService
    class AlertService
    class TrainModel
    class SQLiteDB

    DashboardPage --> Converter
    DashboardPage --> RatesTable
    DashboardPage --> CurrencyHeatmap
    DashboardPage --> AlertsPanel
    DashboardPage --> ExchangeRateChart
    FlaskAPI --> CurrencyRoutes
    FlaskAPI --> ForecastRoutes
    CurrencyRoutes --> ExchangeRateService
    CurrencyRoutes --> HistoricalService
    CurrencyRoutes --> AlertService
    ForecastRoutes --> TrainModel
    ExchangeRateService --> SQLiteDB
    AlertService --> SQLiteDB
    TrainModel --> SQLiteDB
```

### Sequence diagram for conversion

```mermaid
sequenceDiagram
    actor User
    participant UI as React Dashboard
    participant API as Flask API
    participant Service as Converter Service
    participant Market as Frankfurter API

    User->>UI: Enter amount and currencies
    UI->>API: GET /api/convert?from=USD&to=INR&amount=100
    API->>Service: convert_amount()
    Service->>Market: Fetch current pair rate
    Market-->>Service: Rate snapshot
    Service-->>API: Converted value
    API-->>UI: JSON result
    UI-->>User: Display conversion result
```

### Activity diagram for forecasting workflow

```mermaid
flowchart TD
    A[User opens Forecast page] --> B[Request /api/forecast]
    B --> C[Fetch FX history]
    C --> D[Validate chronological order]
    D --> E[Engineer lag and rolling features]
    E --> F[Train LinearRegression model]
    F --> G[Generate test metrics]
    G --> H[Recursive next-period forecasting]
    H --> I[Return forecast payload]
    I --> J[Render chart and metrics in UI]
```
