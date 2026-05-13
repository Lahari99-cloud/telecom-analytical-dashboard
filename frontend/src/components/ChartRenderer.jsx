import React from 'react';
import { Bar, Doughnut, Line, Scatter, Radar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  RadialLinearScale,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  RadialLinearScale,
  Tooltip,
  Legend,
  Filler
);

const COLORS = [
  '#2563eb',
  '#10b981',
  '#f97316',
  '#8b5cf6',
  '#ef4444',
  '#06b6d4',
  '#f59e0b',
  '#ec4899',
  '#6366f1',
  '#14b8a6',
];

const FILLS = [
  'rgba(37,99,235,0.78)',
  'rgba(16,185,129,0.78)',
  'rgba(249,115,22,0.78)',
  'rgba(139,92,246,0.78)',
  'rgba(239,68,68,0.78)',
  'rgba(6,182,212,0.78)',
  'rgba(245,158,11,0.78)',
  'rgba(236,72,153,0.78)',
  'rgba(99,102,241,0.78)',
  'rgba(20,184,166,0.78)',
];

function buildDataset(ds, idx, type) {
  const base = {
    ...ds,
    label: ds.label || 'Metric',
    data: ds.data || [],
    borderWidth: 2,
  };

  if (type === 'doughnut') {
    return {
      ...base,
      backgroundColor: FILLS,
      borderColor: '#ffffff',
      borderWidth: 4,
      hoverBackgroundColor: COLORS,
      hoverBorderColor: '#ffffff',
      hoverOffset: 12,
    };
  }

  if (type === 'bar') {
    return {
      ...base,
      backgroundColor: FILLS,
      borderColor: COLORS,
      borderRadius: 12,
      maxBarThickness: 62,
    };
  }

  if (type === 'line') {
    return {
      ...base,
      borderColor: COLORS[idx % COLORS.length],
      backgroundColor: 'rgba(37,99,235,0.16)',
      pointBackgroundColor: COLORS[idx % COLORS.length],
      pointBorderColor: '#ffffff',
      pointBorderWidth: 2,
      pointRadius: 5,
      pointHoverRadius: 8,
      tension: 0.35,
      fill: true,
    };
  }

  if (type === 'scatter') {
    return {
      ...base,
      backgroundColor: FILLS,
      borderColor: COLORS,
      pointBackgroundColor: FILLS,
      pointBorderColor: COLORS,
      pointBorderWidth: 2,
      pointRadius: 7,
      pointHoverRadius: 9,
    };
  }

  if (type === 'radar') {
    return {
      ...base,
      borderColor: COLORS[idx % COLORS.length],
      backgroundColor: 'rgba(37,99,235,0.22)',
      pointBackgroundColor: COLORS[idx % COLORS.length],
      pointBorderColor: '#ffffff',
      pointRadius: 5,
      fill: true,
    };
  }

  return base;
}

export default function ChartRenderer({ chart }) {
  if (!chart) {
    return (
      <div className="empty-state">
        <h2>Ask the chatbot a telecom business question</h2>
        <p>Charts will render here dynamically from SQLite-backed intent-to-SQL analytics.</p>
      </div>
    );
  }

  const type = chart.type || 'bar';
  const data = {
    labels: chart.labels || [],
    datasets: (chart.datasets || []).map((ds, i) => buildDataset(ds, i, type)),
  };

  const commonOptions = {
    responsive: true,
    maintainAspectRatio: false,
    animation: false,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          usePointStyle: true,
          boxWidth: 10,
          color: '#334155',
          font: { size: 12, weight: '700' },
        },
      },
      tooltip: {
        backgroundColor: '#0f172a',
        titleColor: '#ffffff',
        bodyColor: '#e2e8f0',
        padding: 12,
        cornerRadius: 10,
      },
    },
  };

  const axisOptions = {
    ...commonOptions,
    scales: {
      x: { grid: { display: false }, ticks: { color: '#475569', font: { weight: '700' } } },
      y: { grid: { color: 'rgba(148,163,184,0.24)' }, ticks: { color: '#475569', font: { weight: '700' } } },
    },
  };

  let chartComponent;
  if (type === 'doughnut') chartComponent = <Doughnut data={data} options={{ ...commonOptions, cutout: '62%' }} />;
  else if (type === 'line') chartComponent = <Line data={data} options={axisOptions} />;
  else if (type === 'scatter') {
    chartComponent = (
      <Scatter
        data={data}
        options={{
          ...commonOptions,
          scales: {
            x: { title: { display: true, text: chart.xAxis || 'Risk' }, grid: { color: 'rgba(148,163,184,0.24)' } },
            y: { title: { display: true, text: chart.yAxis || 'Revenue' }, grid: { color: 'rgba(148,163,184,0.24)' } },
          },
        }}
      />
    );
  } else if (type === 'radar') chartComponent = <Radar data={data} options={commonOptions} />;
  else chartComponent = <Bar data={data} options={axisOptions} />;

  return (
    <section className="chart-card">
      <div className="chart-header">
        <h2>{chart.title}</h2>
        <span>{type.toUpperCase()}</span>
      </div>
      <div className="chart-shell colored-chart">{chartComponent}</div>
    </section>
  );
}
