import React, { useEffect, useState } from 'react';
import { fetchGeoRegions } from '../services/api';

export default function GeoView({ refreshToken }) {
  const [regions, setRegions] = useState([]);
  useEffect(() => { fetchGeoRegions().then(setRegions).catch(() => setRegions([])); }, [refreshToken]);
  return <section className="geo-card"><div><h3>Region Intelligence View</h3><p>Map-like regional performance layer for telecom operations.</p></div><div className="geo-grid">{regions.map(r => <div className="region-tile" key={r.region}><strong>{r.region}</strong><span>Churn {(Number(r.churn)*100).toFixed(1)}%</span><span>Revenue ${Number(r.revenue).toLocaleString()}</span><span>NPS {r.nps}</span><span>Latency {r.latency} ms</span></div>)}</div></section>;
}
