import { useEffect, useState } from 'react';
import api from '../services/api';
import Converter from '../components/dashboard/Converter';
import CurrencyHeatmap from '../components/dashboard/CurrencyHeatmap';
import ExchangeRateChart from '../components/dashboard/ExchangeRateChart';
import MetricCard from '../components/dashboard/MetricCard';
import RatesTable from '../components/dashboard/RatesTable';
import VolatilityCard from '../components/dashboard/VolatilityCard';
import Loading from '../components/common/Loading';
import ErrorMessage from '../components/common/ErrorMessage';

export default function DashboardPage() {
  const [rates, setRates] = useState({});
  const [snapshotDate, setSnapshotDate] = useState('');
  const [analytics, setAnalytics] = useState(null);
  const [volatility, setVolatility] = useState(null);
  const [heatmapData, setHeatmapData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const buildHeatmapFromHistory = (historySeries, liveRates) => {
    if (!historySeries || historySeries.length < 2) return [];

    const firstPoint = historySeries[0]?.rates || {};
    const lastPoint = historySeries[historySeries.length - 1]?.rates || {};
    const currencies = Object.keys(liveRates || {});

    return currencies.map((code) => {
      const startRate = firstPoint[code];
      const endRate = lastPoint[code];
      if (startRate == null || endRate == null || startRate === 0) {
        return { label: code, value: 0 };
      }
      const value = ((endRate - startRate) / startRate) * 100;
      return { label: code, value: Number(value.toFixed(2)) };
    });
  };

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const [ratesRes, analyticsRes, volatilityRes, historyRes] = await Promise.all([
          api.get('/api/rates', { params: { base: 'USD' } }),
          api.get('/api/analytics', { params: { base: 'USD', target: 'INR', days: 90 } }),
          api.get('/api/volatility', { params: { base: 'USD', target: 'INR', days: 90 } }),
          api.get('/api/rates/history', { params: { base: 'USD', symbols: 'EUR,GBP,JPY,INR,AED,CHF,CNY,AUD,CAD', days: 90 } }),
        ]);

        const liveRates = ratesRes.data.rates || {};
        setRates(liveRates);
        setSnapshotDate(ratesRes.data.date || '');
        setAnalytics(analyticsRes.data.summary || {});
        setVolatility(volatilityRes.data.volatility || {});
        setHeatmapData(buildHeatmapFromHistory(historyRes.data.rates || [], liveRates));
      } catch (err) {
        setError(err.response?.data?.error || 'Unable to load dashboard data.');
      } finally {
        setLoading(false);
      }
    };

    fetchSummary();
  }, []);

  if (loading) return <Loading label="Loading dashboard metrics..." />;
  if (error) return <ErrorMessage message={error} />;

  const chartLabels = (analytics?.series || []).map((entry) => entry.date);
  const chartValues = (analytics?.series || []).map((entry) => Number(entry.rate));

  return (
    <div className="space-y-6">
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <MetricCard label="Base Currency" value="USD" trend="Source: Frankfurter API" accent="blue" />
        <MetricCard label="Latest INR rate" value={Number(Object.values(rates)[0] || 0).toFixed(4)} trend="Rate snapshot" accent="emerald" />
        <MetricCard label="Period change" value={analytics?.percentage_change ? `${Number(analytics.percentage_change).toFixed(2)}%` : 'N/A'} trend="90-day comparison" accent="yellow" />
        <MetricCard label="Volatility" value={volatility?.volatility_pct ? `${Number(volatility.volatility_pct).toFixed(2)}%` : 'N/A'} trend={volatility?.classification || 'Awaiting data'} accent="red" />
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.5fr_1fr]">
        <div className="space-y-6">
          <div>
            <h2 className="mb-3 text-xl font-semibold text-white">Market overview</h2>
            {chartLabels.length > 0 ? (
              <ExchangeRateChart labels={chartLabels} values={chartValues} label="USD/INR trend" />
            ) : (
              <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-4 text-slate-400">No historical trend data available yet.</div>
            )}
          </div>
          <div>
            <h2 className="mb-3 text-xl font-semibold text-white">Live rates table</h2>
            <RatesTable rates={rates} base="USD" snapshotDate={snapshotDate} />
          </div>
        </div>

        <div className="space-y-6">
          <Converter />
          <VolatilityCard volatility={volatility} />
          <CurrencyHeatmap values={heatmapData} />
        </div>
      </div>
    </div>
  );
}
