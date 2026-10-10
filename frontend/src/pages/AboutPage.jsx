export default function AboutPage() {
  return (
    <div className="space-y-5">
      <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-6">
        <h2 className="text-2xl font-semibold text-white">Global FX Intelligence</h2>
        <p className="mt-3 text-slate-300">
          This application is designed for the FIN623 international financial management assignment. It combines live exchange-rate data, historical analytics, volatility measurement, and a supervised machine-learning forecasting module.
        </p>
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-5">
          <h3 className="text-lg font-semibold text-white">Core features</h3>
          <ul className="mt-3 space-y-2 text-sm text-slate-300">
            <li>• Real-time FX data from Frankfurter</li>
            <li>• Historical trend and percentage change analysis</li>
            <li>• Converter, volatility, and heatmap views</li>
            <li>• ML forecast with evaluation metrics</li>
            <li>• SQLite alerts and trigger tracking</li>
          </ul>
        </div>
        <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-5">
          <h3 className="text-lg font-semibold text-white">Limitations</h3>
          <ul className="mt-3 space-y-2 text-sm text-slate-300">
            <li>• Forecasts are educational and not guaranteed advice.</li>
            <li>• API availability depends on the external provider.</li>
            <li>• Historical data may contain gaps during weekends or holidays.</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
