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
  generateFromText: (textInput, apiKey) => api.post('/generate-from-text/', { text_input: textInput, api_key: apiKey }),

  // Generate objects from uploaded image
  generateFromImage: async (formData, apiKey) => {
    formData.append('api_key', apiKey);
    const imageEntry = formData.get('image');
    console.log('[IMAGE_DEBUG] api.generateFromImage: starting request', {
      url: `${API_BASE_URL}/generate-objects-from-image/`,
      hasImage: !!imageEntry,
      imageName: imageEntry?.name,
      imageSize: imageEntry?.size,
      imageType: imageEntry?.type,
      hasApiKey: !!apiKey?.trim(),
      formDataKeys: [...formData.keys()],
    });

    const start = performance.now();
    try {
      const response = await api.post('/generate-objects-from-image/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log('[IMAGE_DEBUG] api.generateFromImage: success', {
        status: response.status,
        elapsedMs: Math.round(performance.now() - start),
        dataKeys: Object.keys(response.data ?? {}),
        objectCount: Object.keys(response.data?.objects ?? {}).length,
        llmTextLength: response.data?.llm_text?.length ?? 0,
        llmTextPreview: response.data?.llm_text?.slice(0, 300),
        objects: response.data?.objects,
      });
      return response;
    } catch (error) {
      console.error('[IMAGE_DEBUG] api.generateFromImage: failed', {
        elapsedMs: Math.round(performance.now() - start),
        message: error.message,
        status: error.response?.status,
        statusText: error.response?.statusText,
        responseData: error.response?.data,
        responseHeaders: error.response?.headers,
      });
      throw error;
    }
  },
};

export default api;

