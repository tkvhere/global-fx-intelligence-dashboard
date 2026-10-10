export default function RatesTable({ rates, base = 'USD', snapshotDate = '' }) {
  if (!rates || Object.keys(rates).length === 0) {
    return <div className="text-slate-400">No exchange-rate data available.</div>;
  }

  const tableDate = snapshotDate || new Date().toISOString().slice(0, 10);

  return (
    <div className="overflow-hidden rounded-xl border border-slate-800">
      <table className="min-w-full divide-y divide-slate-800 text-left text-sm">
        <thead className="bg-slate-950/70 text-slate-300">
          <tr>
            <th className="px-4 py-3 font-medium">Currency</th>
            <th className="px-4 py-3 font-medium">Rate</th>
            <th className="px-4 py-3 font-medium">Date</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-800 bg-slate-900/60">
          {Object.entries(rates).map(([code, value]) => (
            <tr key={code} className="hover:bg-slate-800/30">
              <td className="px-4 py-3 font-medium text-white">{code}</td>
              <td className="px-4 py-3 text-emerald-300">{Number(value).toFixed(4)}</td>
              <td className="px-4 py-3 text-slate-400">{tableDate}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
