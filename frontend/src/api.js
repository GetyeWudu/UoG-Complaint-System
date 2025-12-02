import axios from 'axios';

// Determine API base URL based on environment
const getBaseURL = () => {
  // Vite uses import.meta.env instead of process.env
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL;
  }
  
  // Otherwise, use current hostname with port 8000
  const hostname = window.location.hostname;
  const baseURL = `http://${hostname}:8000/api/`;
  
  // Debug: Log the API URL (remove in production)
  console.log('🔗 API Base URL:', baseURL);
  
  return baseURL;
};

const api = axios.create({
  baseURL: getBaseURL(),
});

// Automatically add the token to every request if we are logged in
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

export default api;
