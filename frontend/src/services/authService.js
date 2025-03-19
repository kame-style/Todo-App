import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance with token interceptor
const axiosInstance = axios.create({
  baseURL: API_URL,
});

// Add a request interceptor to attach the auth token
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

const AuthService = {
  async register(email, password) {
    const response = await axios.post(`${API_URL}/register`, {
      email,
      password,
    });
    return response.data;
  },

  async login(email, password) {
    // FormData is required for token endpoint using OAuth2PasswordRequestForm
    const formData = new FormData();
    formData.append('username', email); // Backend expects username field but we use email
    formData.append('password', password);

    const response = await axios.post(`${API_URL}/token`, formData);
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('isLoggedIn', 'true');
    }
    return response.data;
  },

  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('isLoggedIn');
  },

  getCurrentUser() {
    return axiosInstance.get(`${API_URL}/users/me`);
  },

  isLoggedIn() {
    return localStorage.getItem('isLoggedIn') === 'true';
  },

  getAuthHeader() {
    const token = localStorage.getItem('token');
    return token ? { Authorization: `Bearer ${token}` } : {};
  },
};

export { AuthService, axiosInstance }; 