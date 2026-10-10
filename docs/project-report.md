# Project Report

## 1. Objective

The Global FX Intelligence dashboard was built to satisfy the FIN623 project requirement for a modern currency intelligence platform. The goal was to design and implement a complete, working, full-stack application that integrates financial data retrieval, analytics, forecasting, and user interaction in a polished dashboard.

## 2. Business value

The application provides a practical business-facing view of foreign exchange performance across major currencies. It allows users to:

- monitor live exchange rates,
- compare currency pairs over time,
- estimate short-term movement risk,
- convert amounts across currencies,
- create threshold-based alerts,
- interpret market direction with AI-based forecast signals.

## 3. Solution overview

The system is split into a Flask API and a Vite React frontend. The backend retrieves market data from the Frankfurter API, stores historical snapshots and alert state in SQLite, and runs forecasting logic using a supervised learning pipeline. The frontend consumes the API and renders a responsive analytics dashboard.

## 4. Functional scope

The implemented platform includes:

- exchange-rate overview cards,
- currency table and rate views,
- historical trend charts,
- financial pair summary analytics,
- forecast generation and predictive metrics,
- volatility classification,
- alert subscription workflows,
- utility and documentation pages.

## 5. Key technical decisions

- The backend uses Flask Blueprints to keep endpoints modular.
- SQLite is used to persist alerts and supported generated records.
- Data preparation for forecasting uses rolling lag features and chronological validation.
- React Router drives the dashboard layout and page navigation.
- Tailwind CSS ensures a professional fintech dashboard aesthetic.

## 6. Deliverables

The repository contains both implementation code and supporting documentation. This enables easy review, local execution, and demonstration during a viva or presentation.

## 7. Conclusion

The project succeeds as a working, testable currency intelligence solution. It demonstrates strong integration between finance, web application development, analytics, and machine learning in one coherent dashboard.
