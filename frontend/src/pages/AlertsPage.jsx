import { useEffect, useState } from 'react';
import api from '../services/api';
import AlertsPanel from '../components/dashboard/AlertsPanel';
import Loading from '../components/common/Loading';
import ErrorMessage from '../components/common/ErrorMessage';

export default function AlertsPage() {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const response = await api.get('/api/alerts');
        setAlerts(response.data.alerts || []);
      } catch (err) {
        setError(err.response?.data?.error || 'Unable to load alerts.');
      } finally {
        setLoading(false);
      }
    };
    fetchAlerts();
  }, []);

  if (loading) return <Loading label="Loading alert configuration..." />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <div className="space-y-5">
      <AlertsPanel />
      <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-4">
        <h3 className="text-lg font-semibold text-white">Trigger history</h3>
        <ul className="mt-3 space-y-2 text-sm text-slate-300">
          {alerts.length === 0 ? <li>No alert history yet.</li> : alerts.map((alert) => (
            <li key={alert.id} className="rounded-lg border border-slate-700 bg-slate-950/60 p-3">{alert.currency_pair} · {alert.direction} {Number(alert.threshold).toFixed(2)}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
