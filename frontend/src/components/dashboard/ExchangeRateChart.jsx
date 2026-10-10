import { Line } from 'react-chartjs-2';
import {
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LinearScale,
  LineElement,
  PointElement,
  Title,
  Tooltip,
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

export default function ExchangeRateChart({ labels, values, label = 'Exchange rate' }) {
  const chartData = {
    labels,
    datasets: [
      {
        label,
        data: values,
        borderColor: '#34d399',
        backgroundColor: 'rgba(52,211,153,0.18)',
        fill: true,
        tension: 0.3,
      },
    ],
  };

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-4">
      <Line data={chartData} options={{ responsive: true, plugins: { legend: { labels: { color: '#cbd5e1' } } }, scales: { x: { ticks: { color: '#cbd5e1' }, grid: { color: '#1e293b' } }, y: { ticks: { color: '#cbd5e1' }, grid: { color: '#1e293b' } } } }} />
    </div>
  );
}
