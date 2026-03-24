import axios from 'axios';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8888';

const api = axios.create({
  baseURL: BASE_URL,
  headers: { 'Content-Type': 'application/json' },
  timeout: 30000,
});

export const chatAPI = {
  send: (query, history = [], simple_mode = false, language = null) =>
    api.post('/chat', { query, history, simple_mode, ...(language && { language }) }),
};

export const herbsAPI = {
  list: () => api.get('/herb'),
  get: (name) => api.get(`/herb/${encodeURIComponent(name)}`),
};

export const doshaAPI = {
  assess: (answers) => api.post('/assess-dosha', { answers }),
};

export const routineAPI = {
  get: (season) => api.get('/daily-routine', { params: season ? { season } : {} }),
};

export const samhitaAPI = {
  search: (query, top_k = 5, sthana = null) =>
    api.post('/search-samhita', { query, top_k, sthana }),
};

export const transcribeAPI = {
  upload: (formData) =>
    api.post('/transcribe', formData, { headers: { 'Content-Type': 'multipart/form-data' } }),
};

export const healthAPI = {
  check: () => api.get('/health'),
};

export default api;
