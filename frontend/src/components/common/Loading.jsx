export default function Loading({ label = 'Loading data...' }) {
  return (
    <div className="flex items-center gap-3 rounded-xl border border-slate-700 bg-slate-900/80 p-4 text-slate-300">
      <div className="h-4 w-4 animate-spin rounded-full border-2 border-emerald-400 border-t-transparent" />
      <span>{label}</span>
    </div>
  );
}
