import { useEffect, useState } from 'react';
import api from '../services/api';
import ExchangeRateChart from '../components/dashboard/ExchangeRateChart';
import Loading from '../components/common/Loading';
import ErrorMessage from '../components/common/ErrorMessage';

export default function AnalyticsPage() {
  const [summary, setSummary] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const response = await api.get('/api/analytics', { params: { base: 'USD', target: 'INR', days: 90 } });
        setSummary(response.data.summary || {});
      } catch (err) {
        setError(err.response?.data?.error || 'Unable to load analytics.');
      } finally {
        setLoading(false);
      }
    };
    fetchAnalytics();
  }, []);

  if (loading) return <Loading label="Loading historical analytics..." />;
  if (error) return <ErrorMessage message={error} />;

  const labels = summary.series ? summary.series.map((item) => item.date.slice(5)) : [];
  const values = summary.series ? summary.series.map((item) => item.rate) : [];

  return (
    <div className="space-y-6">
      <div className="grid gap-4 md:grid-cols-3">
        <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-4">
          <div className="text-sm text-slate-400">Start rate</div>
          <div className="mt-2 text-2xl text-white">{summary.start_rate ? Number(summary.start_rate).toFixed(4) : 'N/A'}</div>
        </div>
        <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-4">
          <div className="text-sm text-slate-400">Latest rate</div>
          <div className="mt-2 text-2xl text-white">{summary.latest_rate ? Number(summary.latest_rate).toFixed(4) : 'N/A'}</div>
        </div>
        <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-4">
          <div className="text-sm text-slate-400">Percentage change</div>
          <div className="mt-2 text-2xl text-emerald-300">{summary.percentage_change ? `${Number(summary.percentage_change).toFixed(2)}%` : 'N/A'}</div>
        </div>
      </div>

      <ExchangeRateChart labels={labels} values={values} label="USD/INR historical trend" />
    </div>
  );
}
