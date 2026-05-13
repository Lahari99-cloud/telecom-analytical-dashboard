import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8001';

export async function askTelecomAssistant(message) {
  const { data } = await axios.post(`${API_BASE}/chat`, { message });
  return data;
}

export async function fetchKpis() {
  const { data } = await axios.get(`${API_BASE}/kpis`);
  return data;
}

export async function fetchGeoRegions() {
  const { data } = await axios.get(`${API_BASE}/geo/regions`);
  return data;
}
