# Testing Report

## Objective

Testing verifies backend behavior, frontend production compilation, and the critical live API paths used in the FIN623 demonstration.

## Automated backend tests

Command executed from the repository root:

```powershell
pytest backend/tests -q
```

Result: **PASS, 9 tests passed**.

The suite covers health status, supported currencies, conversion and analytics calculations, chronological feature preparation, recursive forecast behavior, and alert creation, triggering, and duplicate rejection.

## Frontend production build

Command executed from `frontend/`:

```powershell
npm run build
```

Result: **PASS**. Vite transformed the application and generated the production bundle in `frontend/dist/`.

## Backend source validation

Command executed from the repository root:

```powershell
python -m compileall -q backend
```

Result: **PASS**. Backend Python files compiled without syntax errors.

## Live API checks

- **PASS:** `GET /api/health` returned the expected healthy service response.
- **PASS:** `GET /api/forecast?base=USD&target=INR&horizon=3` returned HTTP 200, three forecast values, and MAE/RMSE metrics.
- **PASS:** two identical alert creation requests returned HTTP 201 followed by HTTP 400, confirming duplicate protection.

## Not tested

No automated browser end-to-end test framework is configured in this repository. Manual screenshots provide UI evidence for the overview, rates, analytics, forecast, and alerts views.

## Conclusion

The backend test suite, Python compilation check, frontend production build, and selected live API workflows passed for the intended local academic project scope.
