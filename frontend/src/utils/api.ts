import axios, { AxiosError } from "axios";
import type { AxiosInstance, AxiosRequestConfig, AxiosResponse } from "axios";
import { API_ROUTES } from "./constants";

const api: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_APP_API_BASE_URL,
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});

let isRefreshing = false;
let refreshTokenPromise: Promise<unknown> | null = null;

api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError): Promise<AxiosResponse | never> => {
    const originalRequest = error.config as AxiosRequestConfig & {
      _retry?: boolean;
    };

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      if (isRefreshing && refreshTokenPromise) {
        try {
          await refreshTokenPromise;
          return api(originalRequest);
        } catch {
          window.location.href = "/login";
          throw error;
        }
      }

      isRefreshing = true;
      refreshTokenPromise = api
        .get(API_ROUTES.AUTH.REFRESH_TOKEN, { withCredentials: true })
        .finally(() => {
          isRefreshing = false;
          refreshTokenPromise = null;
        });

      try {
        await refreshTokenPromise;
        return api(originalRequest);
      } catch {
        window.location.href = "/login";
        throw error;
      }
    }

    if (error.response) {
      if (error.response.status >= 500) {
        return Promise.reject(error);
      }

      return Promise.resolve(error.response);
    }

    return Promise.reject(error);
  }
);

export default api;
