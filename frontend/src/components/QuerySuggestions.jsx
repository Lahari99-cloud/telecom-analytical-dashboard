import React from 'react';

const suggestions = ['Show churn by region', 'Show revenue trend', 'Show product recommendation mix', 'Show ARPU by segment', 'Show risk vs revenue', 'Show network quality by region'];

export default function QuerySuggestions({ onSelect }) {
  return <div className="suggestions">{suggestions.map(item => <button key={item} onClick={() => onSelect(item)}>{item}</button>)}</div>;
}
