import { useEffect, useState } from 'react';
import api from '../../services/api';

export default function AlertsPanel() {
  const [alerts, setAlerts] = useState([]);
  const [pair, setPair] = useState('USD/INR');
  const [threshold, setThreshold] = useState('85');
  const [direction, setDirection] = useState('above');
  const [message, setMessage] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const loadAlerts = async () => {
    try {
      const response = await api.get('/api/alerts');
      setAlerts(response.data.alerts || []);
    } catch (error) {
      setMessage('Unable to load alerts.');
    }
  };

  useEffect(() => {
    loadAlerts();
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (isSubmitting) return;
    setIsSubmitting(true);
    try {
      await api.post('/api/alerts', {
        currency_pair: pair,
        threshold,
        direction,
        enabled: true,
      });
      setMessage('Alert created successfully.');
      loadAlerts();
    } catch (error) {
      setMessage(error.response?.data?.error || 'Unable to create alert');
    } finally {
      setIsSubmitting(false);
    }
  };

  const removeAlert = async (id) => {
    try {
      await api.delete(`/api/alerts/${id}`);
      loadAlerts();
    } catch (error) {
      setMessage('Alert deletion failed.');
    }
  };

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-5">
      <h3 className="text-lg font-semibold text-white">Threshold Alerts</h3>
      <form className="mt-4 space-y-3" onSubmit={handleSubmit}>
        <div className="grid gap-3 md:grid-cols-3">
          <input value={pair} onChange={(e) => setPair(e.target.value)} className="rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-white" placeholder="USD/INR" />
          <input value={threshold} onChange={(e) => setThreshold(e.target.value)} type="number" step="0.01" className="rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-white" placeholder="Threshold" />
          <select value={direction} onChange={(e) => setDirection(e.target.value)} className="rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-white">
            <option value="above">Above</option>
            <option value="below">Below</option>
          </select>
        </div>
        <button disabled={isSubmitting} className="rounded-xl bg-emerald-500 px-4 py-2 font-medium text-slate-950 disabled:cursor-not-allowed disabled:bg-emerald-900 disabled:text-slate-300">
          {isSubmitting ? 'Creating...' : 'Create Alert'}
        </button>
      </form>
      {message ? <div className="mt-3 text-sm text-amber-300">{message}</div> : null}

      <div className="mt-5 space-y-2">
        {alerts.length === 0 ? <div className="text-sm text-slate-400">No active alerts configured.</div> : alerts.map((alert) => (
          <div key={alert.id} className="flex items-center justify-between rounded-xl border border-slate-700 bg-slate-950/60 p-3">
            <div>
              <div className="font-medium text-white">{alert.currency_pair}</div>
              <div className="text-xs text-slate-400">{alert.direction} {Number(alert.threshold).toFixed(2)}</div>
            </div>
            <button onClick={() => removeAlert(alert.id)} className="rounded-lg bg-red-500/10 px-3 py-1 text-xs text-red-200">Delete</button>
          </div>
        ))}
      </div>
    </div>
  );
}
