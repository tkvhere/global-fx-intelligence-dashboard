export default function VolatilityCard({ volatility }) {
  if (!volatility) return <div className="rounded-xl border border-slate-800 p-4 text-slate-400">Volatility data unavailable.</div>;

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-5">
      <div className="text-lg font-semibold text-white">Historical Volatility</div>
      <div className="mt-4 text-3xl font-semibold text-amber-300">{Number(volatility.volatility_pct || 0).toFixed(2)}%</div>
      <div className="mt-2 text-sm text-slate-400">Annualized: {Number(volatility.annualized_volatility_pct || 0).toFixed(2)}% · {volatility.classification}</div>
      <p className="mt-3 text-sm text-slate-300">{volatility.explanation}</p>
      <p className="mt-2 text-xs text-red-300">{volatility.warning}</p>
    </div>
  );
}
