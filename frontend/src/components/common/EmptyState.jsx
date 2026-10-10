export default function EmptyState({ title, message }) {
  return (
    <div className="rounded-xl border border-dashed border-slate-700 bg-slate-900/60 p-6 text-center text-slate-300">
      <h3 className="text-lg font-semibold text-slate-100">{title}</h3>
      <p className="mt-2 text-sm text-slate-400">{message}</p>
    </div>
  );
}
