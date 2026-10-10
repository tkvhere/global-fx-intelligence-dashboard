import { useEffect, useState } from 'react';
import api from '../services/api';
import Loading from '../components/common/Loading';
import ErrorMessage from '../components/common/ErrorMessage';

export default function RatesPage() {
  const [base, setBase] = useState('USD');
  const [rates, setRates] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchRates = async () => {
      try {
        const response = await api.get('/api/rates', { params: { base } });
        setRates(response.data.rates || {});
      } catch (err) {
        setError(err.response?.data?.error || 'Unable to load rates.');
      } finally {
        setLoading(false);
      }
    };
    fetchRates();
  }, [base]);

  if (loading) return <Loading label="Loading exchange rates..." />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <div className="space-y-5">
      <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-5">
        <label className="block text-sm text-slate-300">Select base currency</label>
        <select value={base} onChange={(e) => setBase(e.target.value)} className="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-white md:max-w-xs">
          {['USD', 'EUR', 'GBP', 'JPY', 'INR', 'AED', 'CHF', 'CNY', 'AUD', 'CAD'].map((currency) => (
            <option key={currency} value={currency}>{currency}</option>
          ))}
        </select>
      </div>

      <div className="overflow-hidden rounded-2xl border border-slate-800">
        <table className="min-w-full divide-y divide-slate-800 text-left text-sm">
          <thead className="bg-slate-950/70 text-slate-300">
            <tr>
              <th className="px-4 py-3">Currency</th>
              <th className="px-4 py-3">Exchange rate</th>
              <th className="px-4 py-3">Latest date</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800 bg-slate-900/60">
            {Object.entries(rates).map(([currency, value]) => (
              <tr key={currency}>
                <td className="px-4 py-3 text-white">{currency}</td>
                <td className="px-4 py-3 text-emerald-300">{Number(value).toFixed(4)}</td>
                <td className="px-4 py-3 text-slate-400">{new Date().toISOString().slice(0, 10)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
