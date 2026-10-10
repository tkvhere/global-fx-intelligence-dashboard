import { useState } from 'react';
import api from '../../services/api';

export default function Converter() {
  const [fromCurrency, setFromCurrency] = useState('USD');
  const [toCurrency, setToCurrency] = useState('INR');
  const [amount, setAmount] = useState('100');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleSwap = () => {
    setFromCurrency(toCurrency);
    setToCurrency(fromCurrency);
  };

  const handleConvert = async (event) => {
    event.preventDefault();
    try {
      const response = await api.get('/api/convert', {
        params: { from: fromCurrency, to: toCurrency, amount },
      });
      setResult(response.data);
      setError('');
    } catch (err) {
      setError(err.response?.data?.error || 'Conversion failed.');
      setResult(null);
    }
  };

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-5">
      <h3 className="text-lg font-semibold text-white">Currency Converter</h3>
      <form className="mt-4 space-y-4" onSubmit={handleConvert}>
        <div className="grid gap-4 md:grid-cols-2">
          <label className="block">
            <span className="mb-2 block text-sm text-slate-300">From</span>
            <select value={fromCurrency} onChange={(e) => setFromCurrency(e.target.value)} className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-white">
              {['USD', 'EUR', 'GBP', 'JPY', 'INR', 'AED', 'CHF', 'CNY', 'AUD', 'CAD'].map((code) => (
                <option key={code} value={code}>{code}</option>
              ))}
            </select>
          </label>

          <label className="block">
            <span className="mb-2 block text-sm text-slate-300">To</span>
            <select value={toCurrency} onChange={(e) => setToCurrency(e.target.value)} className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-white">
              {['USD', 'EUR', 'GBP', 'JPY', 'INR', 'AED', 'CHF', 'CNY', 'AUD', 'CAD'].map((code) => (
                <option key={code} value={code}>{code}</option>
              ))}
            </select>
          </label>
        </div>

        <div className="flex gap-3">
          <label className="flex-1">
            <span className="mb-2 block text-sm text-slate-300">Amount</span>
            <input type="number" min="0" step="0.01" value={amount} onChange={(e) => setAmount(e.target.value)} className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-white" placeholder="Enter amount" />
          </label>
          <button type="button" onClick={handleSwap} className="self-end rounded-xl border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-slate-100">Swap</button>
        </div>

        <button type="submit" className="w-full rounded-xl bg-emerald-500 px-4 py-2 font-medium text-slate-950 transition hover:bg-emerald-400">Convert</button>
      </form>

      {error ? <div className="mt-4 text-sm text-red-300">{error}</div> : null}
      {result ? (
        <div className="mt-4 rounded-xl border border-emerald-500/30 bg-emerald-500/10 p-4 text-sm text-emerald-100">
          <div className="text-lg font-semibold">{Number(result.converted_amount).toLocaleString(undefined, { maximumFractionDigits: 4 })} {result.to}</div>
          <div className="mt-2 text-slate-200">Exchange rate used: {Number(result.rate).toFixed(6)}</div>
          <div className="text-slate-300">Date: {result.date} · Source: {result.source}</div>
        </div>
      ) : null}
    </div>
  );
}
