import React, { useEffect, useState } from 'react';
import { fetchKpis } from '../services/api';

export default function KPISection({ refreshToken }) {
  const [kpis, setKpis] = useState(null);

  useEffect(() => {
    fetchKpis().then(setKpis).catch(() => setKpis(null));
  }, [refreshToken]);

  const cards = [
    ['Total Revenue', kpis ? `$${(kpis.total_revenue / 1000000).toFixed(2)}M` : '—'],
    ['Avg Churn', kpis ? `${(kpis.avg_churn * 100).toFixed(1)}%` : '—'],
    ['Avg ARPU', kpis ? `$${kpis.avg_arpu}` : '—'],
    ['Avg NPS', kpis ? kpis.avg_nps : '—']
  ];

  return <div className="kpi-grid">{cards.map(([label, value]) => <div className="kpi-card" key={label}><span>{label}</span><strong>{value}</strong></div>)}</div>;
}
