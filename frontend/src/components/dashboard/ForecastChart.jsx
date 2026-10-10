import { Line } from 'react-chartjs-2';

export default function ForecastChart({ labels, values }) {
  const data = {
    labels,
    datasets: [{
      label: 'Forecast',
      data: values,
      borderColor: '#60a5fa',
      backgroundColor: 'rgba(96,165,250,0.15)',
      fill: true,
      tension: 0.35,
    }],
  };

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-4">
      <Line data={data} options={{ responsive: true, plugins: { legend: { labels: { color: '#cbd5e1' } } }, scales: { x: { ticks: { color: '#cbd5e1' }, grid: { color: '#1e293b' } }, y: { ticks: { color: '#cbd5e1' }, grid: { color: '#1e293b' } } } }} />
    </div>
  );
}
