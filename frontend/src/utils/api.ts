import axios, { AxiosError } from "axios";
import type { AxiosInstance, AxiosRequestConfig, AxiosResponse } from "axios";
import { API_ROUTES } from "./constants"; // Assuming constants.ts exists and API_ROUTES is defined

// Create an Axios instance with base URL, credentials, and headers
const api: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_APP_API_BASE_URL,
  withCredentials: true, // Send cookies with requests
  headers: {
    "Content-Type": "application/json", // Default content type
  },
});

// Flag to indicate if a token refresh is currently in progress
let isRefreshing = false;
// A promise that holds the refresh token request. This allows multiple 401s
// to wait for a single refresh operation to complete.
let refreshTokenPromise: Promise<unknown> | null = null;

// Add a response interceptor to handle token expiration (401 errors)
api.interceptors.response.use(
  (response) => response, // If response is successful, just return it
  async (error: AxiosError): Promise<AxiosResponse> => {
    // Cast the error config to include a custom _retry flag
    const originalRequest = error.config as AxiosRequestConfig & {
      _retry?: boolean;
    };

    // Check if the error status is 401 (Unauthorized) and if this request hasn't been retried yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true; // Mark this request as having been retried

      // If a refresh token request is already in progress,
      // subsequent 401s should wait for that refresh to complete.
      if (isRefreshing && refreshTokenPromise) {
        try {
          // Wait for the ongoing refresh token promise to resolve
          await refreshTokenPromise;
          // Once resolved, retry the original failed request with the new token
          return api(originalRequest);
        } catch (refreshWaitError) {
          // If waiting for the refresh token promise fails (meaning the refresh itself failed),
          // redirect to login and re-throw the error.
          window.location.href = "/login";
          throw refreshWaitError;
        }
      }

      // If no refresh token request is in progress, initiate one.
      isRefreshing = true;
      // Create a new promise for the refresh token request.
      refreshTokenPromise = new Promise((resolve, reject) => {
        try {
          // Make a request to the refresh token endpoint
          const response = api.get(
            API_ROUTES.AUTH.REFRESH_TOKEN,
            { withCredentials: true } // Ensure cookies are sent for refresh token
          );
          // If successful, resolve the promise with the response
          resolve(response);
        } catch (refreshError) {
          // If refresh fails, reject the promise
          reject(refreshError);
        } finally {
          // In either case (success or failure), reset the flags
          isRefreshing = false;
          refreshTokenPromise = null;
        }
      });

      try {
        // Wait for the newly initiated refresh token promise to complete
        await refreshTokenPromise;
        // Once completed (successfully), retry the original request
        return api(originalRequest);
      } catch (refreshError) {
        // If the refresh token operation fails, redirect the user to the login page
        window.location.href = "/login";
        // Re-throw the error to propagate it down the promise chain
        throw refreshError;
      }
    }

    // For unknown other type of error, or if it's a 401 that has already been retried,
    // simply re-throw the original error.
    throw error;
  }
);

export default api;
