export default function Header({ title }) {
  return (
    <header className="border-b border-slate-800 bg-slate-950/70 px-4 py-4 backdrop-blur md:px-6">
      <div className="flex items-center justify-between gap-3">
        <div>
          <div className="text-xs uppercase tracking-[0.22em] text-slate-400">AI-Powered Currency Intelligence</div>
          <h1 className="mt-1 text-2xl font-semibold text-white">{title}</h1>
        </div>
        <div className="rounded-full border border-emerald-500/30 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-300">
          Live data source: Frankfurter
        </div>
      </div>
    </header>
  );
}
