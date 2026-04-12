import axios, { AxiosInstance } from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export const apiService = {
  // Assets
  getAssets: (limit = 100) => apiClient.get(`/assets?limit=${limit}`),
  getAsset: (ticker: string) => apiClient.get(`/assets/${ticker}`),

  // Market Data
  getMarketData: (ticker: string) => apiClient.get(`/market-data/${ticker}`),
  getMarketHistory: (ticker: string, days = 30) =>
    apiClient.get(`/market-data/${ticker}/history?days=${days}`),
  refreshMarketData: (ticker: string) => apiClient.post(`/market-data/refresh/${ticker}`),

  // Scoring
  getScoring: (ticker: string) => apiClient.get(`/scoring/${ticker}`),
  calculateScoring: (ticker: string) => apiClient.post(`/scoring/calculate/${ticker}`),

  // Opportunities
  getOpportunities: (limit = 50) => apiClient.get(`/opportunities?limit=${limit}`),
  getTopOpportunities: (limit = 10) => apiClient.get(`/opportunities/top?limit=${limit}`),

  // Alerts
  getAlerts: (limit = 20, unreadOnly = false) =>
    apiClient.get(`/alerts?limit=${limit}&unread_only=${unreadOnly}`),
  markAlertRead: (alertId: number) => apiClient.post(`/alerts/${alertId}/read`),

  // Monitoring
  getMonitoring: () => apiClient.get(`/monitoring`),
  addMonitoring: (ticker: string, assetType = 'STOCK') =>
    apiClient.post(`/monitoring/${ticker}?asset_type=${assetType}`),

  // Dashboard & Stats
  getDashboard: () => apiClient.get(`/dashboard`),
  getStats: () => apiClient.get(`/stats`),

  // Scan
  scanMarket: (tickers: string[]) =>
    apiClient.post(`/scan/market?${tickers.map((t) => `tickers=${t}`).join('&')}`),
};

export default apiClient;
