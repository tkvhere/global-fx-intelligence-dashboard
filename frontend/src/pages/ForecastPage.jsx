import { useEffect, useState } from 'react';
import api from '../services/api';
import ForecastChart from '../components/dashboard/ForecastChart';
import Loading from '../components/common/Loading';
import ErrorMessage from '../components/common/ErrorMessage';

export default function ForecastPage() {
  const [forecast, setForecast] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchForecast = async () => {
      try {
        const response = await api.get('/api/forecast', { params: { base: 'USD', target: 'INR', horizon: 7 } });
        setForecast(response.data);
      } catch (err) {
        setError(err.response?.data?.error || 'Unable to load forecast.');
      } finally {
        setLoading(false);
      }
    };
    fetchForecast();
  }, []);

  if (loading) return <Loading label="Running machine learning forecast..." />;
  if (error) return <ErrorMessage message={error} />;

  const labels = Array.from({ length: forecast?.future_forecast?.length || 0 }, (_, index) => `F${index + 1}`);
  const values = forecast?.future_forecast || [];

  return (
    <div className="space-y-5">
      <div className="grid gap-4 md:grid-cols-3">
        <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-4">
          <div className="text-sm text-slate-400">Model</div>
          <div className="mt-2 text-xl text-white">{forecast?.model_name || 'LinearRegression'}</div>
        </div>
        <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-4">
          <div className="text-sm text-slate-400">MAE</div>
          <div className="mt-2 text-xl text-white">{forecast?.metrics?.mae ? Number(forecast.metrics.mae).toFixed(4) : 'N/A'}</div>
        </div>
        <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-4">
          <div className="text-sm text-slate-400">RMSE</div>
          <div className="mt-2 text-xl text-white">{forecast?.metrics?.rmse ? Number(forecast.metrics.rmse).toFixed(4) : 'N/A'}</div>
        </div>
      </div>

      <ForecastChart labels={labels} values={values} />
      <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-4 text-sm text-slate-300">
        <div className="font-medium text-white">Forecast statement</div>
        <p className="mt-2">{forecast?.warning || 'Forecast output is displayed for educational use.'}</p>
      </div>
    </div>
  );
}
