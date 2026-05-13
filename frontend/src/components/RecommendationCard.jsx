import React from 'react';

export default function RecommendationCard({ analysis }) {
  if (!analysis) return <section className="card muted"><h3>Insight panel</h3><p>Ask a question or click a query shortcut to generate recommendations.</p></section>;
  const pct = Math.round(Number(analysis.confidence) * 100);
  return <section className="card recommendation"><div className="confidence"><span>Confidence</span><strong>{pct}%</strong></div><h3>Executive Insight</h3><p>{analysis.insight}</p><h4>Likely Cause</h4><p>{analysis.cause}</p><h4>Recommended Action</h4><p>{analysis.recommendation}</p><h4>Expected Business Impact</h4><p>{analysis.impact}</p></section>;
}
