import axios, { AxiosRequestConfig } from 'axios';

const hablame = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL}/api`
});

hablame.interceptors.request.use((config: AxiosRequestConfig) => {
  const token = localStorage.getItem('token');
  if (token) {
    if (!config.headers) config.headers = {};
    (config.headers as any).Authorization = `Bearer ${token}`;
  }
  return config;
});

export default hablame;
