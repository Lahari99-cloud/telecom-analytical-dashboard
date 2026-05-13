import React, { useState } from 'react';
import KPISection from './components/KPISection';
import ChartRenderer from './components/ChartRenderer';
import RecommendationCard from './components/RecommendationCard';
import Chatbot from './components/Chatbot';
import QueryButtons from './components/QueryButtons';
import GeoView from './components/GeoView';
import { askTelecomAssistant } from './services/api';

export default function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [refreshToken] = useState(0);

  async function runQuery(q) {
    setLoading(true);
    try {
      const response = await askTelecomAssistant(q);
      setResult(response);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app">
      <header className="hero">
        <div>
          <p className="eyebrow">Telecom Client Demo Prototype</p>
          <h1>Telecom Decision Intelligence</h1>
          <p>
            Deterministic NL → Intent → SQL → Chart → Insight engine. The UI reads from the backend SQLite database only.
          </p>
        </div>
        <div className="status-pill">No LLM · SQLite source of truth · Explainable</div>
      </header>

      <KPISection refreshToken={refreshToken} />
      <QueryButtons onQuery={runQuery} disabled={loading} />

      {loading && <div className="loading-banner">Analyzing telecom SQLite database...</div>}

      <div className="layout">
        <ChartRenderer chart={result?.chart} />
        <RecommendationCard analysis={result?.analysis} />
      </div>

      <div className="secondary-layout sqlite-only">
        <div className="card source-card">
          <h3>SQLite Data Source</h3>
          <p>
            Data is loaded in the backend from <code>database/telecom_catalog.db</code>. No data ingestion tab is exposed in the UI.
          </p>
          <ul>
            <li>Frontend calls FastAPI endpoints.</li>
            <li>FastAPI routes intents to safe predefined SQL.</li>
            <li>Charts and KPIs are generated from SQLite query results.</li>
          </ul>
        </div>
        <GeoView refreshToken={refreshToken} />
      </div>

      <Chatbot onResult={setResult} onLoading={setLoading} />
    </main>
  );
}
