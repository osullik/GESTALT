import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true, // Important for session cookies
  headers: {
    'Content-Type': 'application/json',
  }
});

// Add CSRF token handling for Django
api.interceptors.request.use(
  (config) => {
    // Get CSRF token from cookie if it exists
    const csrfToken = document.cookie
      .split('; ')
      .find(row => row.startsWith('csrftoken='))
      ?.split('=')[1];
    
    if (csrfToken && config.method !== 'get') {
      config.headers['X-CSRFToken'] = csrfToken;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const gestaltAPI = {
  // Get available regions
  getRegions: () => api.get('/regions/'),
  
  // Set selected region
  setRegion: (regionName) => api.post('/regions/set/', { name: regionName }),
  
  // Get available objects for selected region
  getObjects: () => api.get('/objects/'),
  
  // Set search parameters
  setSearchParams: (params) => api.post('/search/params/', params),
  
  // Get search results
  getSearchResults: () => api.get('/search/result/'),
  
  // Generate objects from text input
  generateFromText: (textInput) => api.post('/generate-from-text/', { text_input: textInput }),
};

export default api;

