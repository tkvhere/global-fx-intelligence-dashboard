# User Manual

## Starting the application

### Backend

```powershell
cd backend
python app.py
```

### Frontend

```powershell
cd frontend
npm install
npm run dev -- --host 0.0.0.0
```

## Using the dashboard

1. Open `http://localhost:5173/` in a browser.
2. Navigate using the sidebar.
3. Review the overview summary on the dashboard.
4. Use the rates pages to inspect live FX values.
5. Use the converter to calculate an exchange amount.
6. Review analytics and volatility for historical trends.
7. Visit the forecast section to view the model output.
8. Create and manage rate alerts in the alerts page.

## Notes

- The application depends on external FX data from Frankfurter.
- Forecast values are educational signals and should not be treated as financial guarantees.
