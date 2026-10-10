# Machine Learning Methodology

## Overview

The forecasting module applies a supervised regression approach to exchange-rate time series. The system builds a tabular dataset from historical exchange rates and trains a linear regression model to predict future values.

## Pipeline

1. Load historical FX data for a selected pair.
2. Sort records chronologically.
3. Generate lagged input features and rolling statistics.
4. Split data using time-based ordering rather than random shuffling.
5. Train the regression model on the earlier segment.
6. Evaluate using standard metrics and forecast future output values.

## Feature engineering

The model includes derived features such as:

- previous exchange values,
- rolling averages,
- rate differences,
- trend-aware lag features.

These features improve the model's ability to capture short-term exchange-rate momentum while preserving chronological integrity.

## Model choice

A linear regression model was chosen for its interpretability, simplicity, and suitability for an educational dashboard. It is transparent and easy to explain in a presentation or viva setting.

## Evaluation

The model produces values such as mean absolute error or forecast residual summaries, allowing a user to understand the quality of the prediction without requiring a complex production-grade pipeline.
