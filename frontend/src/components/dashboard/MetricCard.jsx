export default function MetricCard({ label, value, trend, accent = 'emerald' }) {
  const accentMap = {
    emerald: 'text-emerald-300',
    red: 'text-red-300',
    yellow: 'text-yellow-300',
    blue: 'text-blue-300',
  };

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-4 shadow-lg shadow-slate-950/20">
      <div className="text-sm text-slate-400">{label}</div>
      <div className={`mt-3 text-2xl font-semibold ${accentMap[accent] || accentMap.emerald}`}>{value}</div>
      {trend ? <div className="mt-2 text-xs text-slate-400">{trend}</div> : null}
    </div>
  );
}
