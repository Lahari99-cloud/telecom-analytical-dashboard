import React from 'react';

const queries = [
  'Show churn by region',
  'Revenue by segment',
  'Revenue mix by product',
  'Risk vs revenue scatter',
  'Monthly churn trend',
  'Network quality by region'
];

export default function QueryButtons({ onQuery, disabled }) {
  return <section className="query-buttons"><div><h3>Demo Query Shortcuts</h3><p>Click one to trigger deterministic intent-to-SQL analytics.</p></div><div className="query-grid">{queries.map(q => <button disabled={disabled} key={q} onClick={() => onQuery(q)}>{q}</button>)}</div></section>;
}
