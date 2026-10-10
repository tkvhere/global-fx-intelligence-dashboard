import { Route, Routes } from 'react-router-dom';
import Header from './components/layout/Header';
import Sidebar from './components/layout/Sidebar';
import AboutPage from './pages/AboutPage';
import AlertsPage from './pages/AlertsPage';
import AnalyticsPage from './pages/AnalyticsPage';
import DashboardPage from './pages/DashboardPage';
import ForecastPage from './pages/ForecastPage';
import RatesPage from './pages/RatesPage';

export default function App() {
  const pageTitles = {
    '/': 'Overview Dashboard',
    '/rates': 'Live Exchange Rates',
    '/converter': 'Currency Converter',
    '/analytics': 'Historical Analytics',
    '/forecast': 'AI Forecasting',
    '/alerts': 'Rate Alerts',
    '/about': 'Project Information',
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto flex max-w-[1600px] flex-col md:flex-row">
        <Sidebar />
        <main className="min-h-screen flex-1">
          <Routes>
            <Route path="/" element={<Header title={pageTitles['/']} />} />
            <Route path="/rates" element={<Header title={pageTitles['/rates']} />} />
            <Route path="/converter" element={<Header title={pageTitles['/converter']} />} />
            <Route path="/analytics" element={<Header title={pageTitles['/analytics']} />} />
            <Route path="/forecast" element={<Header title={pageTitles['/forecast']} />} />
            <Route path="/alerts" element={<Header title={pageTitles['/alerts']} />} />
            <Route path="/about" element={<Header title={pageTitles['/about']} />} />
          </Routes>

          <div className="p-4 md:p-6">
            <Routes>
              <Route path="/" element={<DashboardPage />} />
              <Route path="/rates" element={<RatesPage />} />
              <Route path="/converter" element={<DashboardPage />} />
              <Route path="/analytics" element={<AnalyticsPage />} />
              <Route path="/forecast" element={<ForecastPage />} />
              <Route path="/alerts" element={<AlertsPage />} />
              <Route path="/about" element={<AboutPage />} />
            </Routes>
          </div>
        </main>
      </div>
    </div>
  );
}
