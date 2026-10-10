function getColor(value) {
  if (value > 2) return 'bg-emerald-500/80';
  if (value > 0) return 'bg-emerald-400/60';
  if (value < -2) return 'bg-red-500/80';
  if (value < 0) return 'bg-red-400/60';
  return 'bg-slate-700';
}

export default function CurrencyHeatmap({ values = [] }) {
  const items = values.length ? values : [
    { label: 'USD', value: 0 },
    { label: 'EUR', value: 0 },
    { label: 'GBP', value: 0 },
    { label: 'JPY', value: 0 },
    { label: 'INR', value: 0 },
    { label: 'AED', value: 0 },
    { label: 'CHF', value: 0 },
    { label: 'CNY', value: 0 },
    { label: 'AUD', value: 0 },
    { label: 'CAD', value: 0 },
  ];

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-5">
      <div className="mb-4 flex items-center justify-between">
        <h3 className="text-lg font-semibold text-white">Currency strength heatmap</h3>
        <div className="text-xs text-slate-400">Method: percentage change over selected window</div>
      </div>
      <div className="grid grid-cols-5 gap-2 text-center text-xs text-slate-200">
        {items.map((item) => (
          <div key={item.label} className={`rounded-lg p-3 ${getColor(item.value)}`}>
            {item.label}
            <div className="mt-1 font-semibold">{item.value.toFixed(1)}%</div>
          </div>
        ))}
      </div>
      <div className="mt-4 flex items-center gap-4 text-xs text-slate-400">
        <span className="rounded bg-emerald-500/70 px-2 py-1 text-white">Positive</span>
        <span className="rounded bg-red-500/70 px-2 py-1 text-white">Negative</span>
        <span className="rounded bg-slate-700 px-2 py-1 text-white">Near zero</span>
      </div>
    </div>
  );
}
