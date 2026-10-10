import { Activity, AlertTriangle, BarChart3, CircleDollarSign, Home, Info, Landmark, TrendingUp } from 'lucide-react';
import { NavLink } from 'react-router-dom';

const items = [
  { to: '/', label: 'Overview', icon: Home },
  { to: '/rates', label: 'Live Rates', icon: CircleDollarSign },
  { to: '/converter', label: 'Converter', icon: Landmark },
  { to: '/analytics', label: 'Historical Analytics', icon: BarChart3 },
  { to: '/forecast', label: 'AI Forecasting', icon: TrendingUp },
  { to: '/alerts', label: 'Rate Alerts', icon: AlertTriangle },
  { to: '/about', label: 'Project Info', icon: Info },
];

export default function Sidebar() {
  return (
    <aside className="w-full border-b border-slate-800 bg-slate-950/80 p-4 md:w-72 md:border-b-0 md:border-r">
      <div className="mb-8 flex items-center gap-3 px-2">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-500/15 text-emerald-400">
          <Activity className="h-5 w-5" />
        </div>
        <div>
          <div className="text-xs uppercase tracking-[0.22em] text-slate-400">FIN623</div>
          <div className="text-lg font-semibold text-white">Global FX</div>
        </div>
      </div>

      <nav className="flex flex-wrap gap-2 md:flex-col">
        {items.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-xl px-3 py-2 text-sm transition ${isActive ? 'bg-emerald-500/15 text-emerald-300' : 'text-slate-300 hover:bg-slate-800'}`
            }
          >
            <Icon className="h-4 w-4" />
            {label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
