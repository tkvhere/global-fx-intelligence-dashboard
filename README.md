# Global FX Intelligence

AI-Powered Global Currency Intelligence Dashboard for the FIN623 academic project. The application combines daily foreign-exchange data, currency conversion, historical analytics, volatility analysis, a currency-strength view, machine-learning forecasting, and persistent rate alerts in a responsive web dashboard.

## Problem and objectives

Foreign-exchange information is often spread across separate tools and difficult to compare quickly. This project provides one interface for exploring supported currency pairs, understanding historical movement, testing conversions, reviewing volatility, and evaluating an interpretable forecast model. The objectives are to demonstrate full-stack development, financial data analysis, machine learning, persistence, and technical documentation in one academic submission.

## Features

- Latest rates for 10 supported currencies through the Frankfurter API.
- Currency conversion for user-selected amounts and pairs.
- Historical pair analytics with period change, minimum, maximum, and daily changes.
- Volatility classification based on historical rate observations.
- Currency-strength heatmap based on percentage movement over the selected window.
- Linear regression forecasting with lag, rolling, percentage-change, and difference features.
- Chronological model evaluation using MAE, RMSE, MAPE, and a naive baseline comparison.
- SQLite-persisted threshold alerts with enable/disable, deletion, trigger history, and duplicate protection.
- Responsive React dashboard with dedicated overview, rates, analytics, forecast, alerts, and about views.

## Technology stack

- Frontend: React 18, React Router, Vite, Tailwind CSS, Chart.js, Axios.
- Backend: Python 3.13, Flask, Flask-CORS, Requests.
- Analytics and ML: pandas, NumPy, scikit-learn `LinearRegression`.
- Persistence: SQLite with SQL schema initialization.
- External data: Frankfurter API at `https://api.frankfurter.app`.

## Architecture

The React single-page application calls Flask blueprints over JSON HTTP endpoints. Flask routes delegate to focused services for rates, conversion, historical analytics, volatility, forecasting, and alerts. The exchange service retrieves and caches provider responses; SQLite stores alert data and local application metadata; the ML service fetches historical observations, engineers features, trains a chronological model, evaluates it, and returns forecast results.

The architecture and UML diagrams are documented in [docs/architecture.md](docs/architecture.md). Supporting design documents are listed in [Technical documentation](#technical-documentation).

## Repository structure

```text
backend/
  app.py                       Flask entry point
  config.py                    Currency and local-path configuration
  routes/                      Flask API blueprints
  services/                    Domain services
  ml/                          Forecast preprocessing, features, training, evaluation
  database/                    SQLite connection and schema
  tests/                       pytest tests
  requirements.txt             Python dependencies
frontend/
  src/                         React application, pages, components, and API client
  package.json                 npm scripts and dependencies
  package-lock.json            Locked frontend dependency versions
docs/                          Reports, UML, API, design, testing, and demo documents
screenshots/                   Application evidence images
.env.example                   Safe frontend environment example
pytest.ini                     Root pytest configuration
```

## Prerequisites

- Python 3.11 or later. The current environment was verified with Python 3.13.
- Node.js and npm.
- Internet access for live Frankfurter API requests.
- Windows PowerShell, macOS/Linux shell, or an equivalent terminal.

## Installation and configuration

From the repository root, create and activate a virtual environment, then install backend dependencies:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r backend\requirements.txt
```

Install frontend dependencies:

```powershell
cd frontend
npm install
cd ..
```

The frontend accepts an optional `VITE_API_URL` variable. Copy `.env.example` to `.env.local` only when the API is not running at the default URL:

```text
VITE_API_URL=http://127.0.0.1:5000
```

Do not commit `.env` or `.env.local` files. The backend has no secret credential or database server requirement; it creates `backend/database/global_fx.db` locally when started.

## Run locally

Start the Flask API in one terminal:

```powershell
.venv\Scripts\Activate.ps1
cd backend
python app.py
```

Start the Vite development server in a second terminal:

```powershell
cd frontend
npm run dev
```

Open `http://localhost:5173`. The API health endpoint is available at `http://127.0.0.1:5000/api/health`.

## Data integration and analytics

The dashboard uses the public Frankfurter API for latest and historical rates. Frankfurter provides daily reference-rate observations rather than tick-by-tick or guaranteed intraday market prices. Weekends and public holidays can therefore produce gaps or the latest available working-day observation. Network access and provider availability are required for live rates, historical analytics, volatility, heatmap values, and forecast training.

Conversion uses a current provider rate for the selected pair. Historical analytics calculates start/latest values, absolute and percentage change, minimum, maximum, and daily movement from the returned observations. Volatility is calculated from the historical rate series and classified for display.

## Forecasting approach

The implemented model is scikit-learn `LinearRegression`, not a neural network or external hosted AI model. The pipeline sorts observations chronologically, creates lag features (`1`, `2`, `3`, `5`, and `10`), rolling means and standard deviations, percentage change, and first difference, then performs a chronological 80/20 train/test split. It reports MAE, RMSE, MAPE, and naive constant-rate baseline metrics. Future values are generated recursively from the trained model. Forecasts are educational estimates and are not financial advice.

## Alerts and database

Users can create `above` or `below` threshold rules for a currency pair. Alerts are stored in SQLite, can be enabled or disabled, and record trigger events. The backend rejects duplicate active configurations with the same pair, threshold, and direction; the frontend also disables the submit button while a request is pending. The schema is available at [backend/database/schema.sql](backend/database/schema.sql), with design notes in [docs/database-design.md](docs/database-design.md).

## API

The main endpoints are:

| Endpoint | Purpose |
| --- | --- |
| `GET /api/health` | API health status |
| `GET /api/currencies` | Supported currency list |
| `GET /api/rates` | Latest rates for a base currency |
| `GET /api/rates/history` | Historical observations |
| `GET /api/convert` | Currency conversion |
| `GET /api/analytics` | Historical pair summary and daily changes |
| `GET /api/volatility` | Historical volatility result |
| `GET /api/forecast` | Forecast values and evaluation metrics |
| `GET /api/forecast/evaluation` | Forecast metrics only |
| `GET/POST /api/alerts` | List or create alerts |
| `PATCH/DELETE /api/alerts/<id>` | Toggle or delete an alert |

Full request and response notes are in [docs/api-documentation.md](docs/api-documentation.md).

## Testing and verification

Run the backend test suite from the repository root:

```powershell
pytest backend/tests -q
```

Build the frontend for production:

```powershell
cd frontend
npm run build
```

Verification completed for this publication preparation:

- PASS: 9 backend tests passed with `pytest backend/tests -q`.
- PASS: Vite production build completed successfully with `npm run build`.
- PASS: Live `GET /api/forecast?base=USD&target=INR&horizon=3` returned HTTP 200, three future values, and MAE/RMSE metrics.
- PASS: Live duplicate alert submission returned HTTP 400 on the second identical request.
- PASS: API health endpoint was previously verified at `http://127.0.0.1:5000/api/health`.
- NOT RUN: automated browser end-to-end tests; no browser test framework is configured in this repository.

The written testing report is available at [docs/testing-report.md](docs/testing-report.md).

## Screenshots

The repository includes genuine application screenshots:

| View | Evidence |
| --- | --- |
| Overview | [screenshots/overview.png](screenshots/overview.png) |
| Rates | [screenshots/rates.png](screenshots/rates.png) |
| Analytics | [screenshots/analytics.png](screenshots/analytics.png) |
| Forecast | [screenshots/forecast.png](screenshots/forecast.png) |
| Alerts | [screenshots/alerts.png](screenshots/alerts.png) |

## Technical documentation

- [Project report](docs/project-report.md)
- [Final report PDF](docs/Global_FX_Intelligence_Report.pdf)
- [Architecture and UML diagrams](docs/architecture.md)
- [API documentation](docs/api-documentation.md)
- [Database design](docs/database-design.md)
- [ML methodology](docs/ml-methodology.md)
- [Testing report](docs/testing-report.md)
- [User manual](docs/user-manual.md)
- [Demonstration script](docs/demonstration-script.md)
- [References](docs/references.md)

## Known limitations

- Frankfurter data is daily reference data and depends on external network availability.
- The SQLite database is intended for local educational use, not concurrent production deployment.
- Forecasts use a simple linear model and should not be interpreted as trading advice.
- No authentication or multi-user alert ownership is implemented.
- No automated browser end-to-end test suite is currently configured.

## Academic information

This repository contains the FIN623 coursework project titled **AI-Powered Global Currency Intelligence Dashboard**. It demonstrates integration of financial data, analytics, machine learning, software architecture, persistence, frontend engineering, testing, and technical documentation.

## Attribution and references

Market data is provided by [Frankfurter](https://www.frankfurter.app/), an open-source exchange-rate API. The implementation also relies on the official documentation for [Flask](https://flask.palletsprojects.com/), [React](https://react.dev/), [Vite](https://vite.dev/), [Tailwind CSS](https://tailwindcss.com/), [scikit-learn](https://scikit-learn.org/), and [SQLite](https://www.sqlite.org/docs.html). A consolidated list is available in [docs/references.md](docs/references.md).
