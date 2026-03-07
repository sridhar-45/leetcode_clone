import api from './api'

export const authAPI = {
  // Register new user
  register: async (userData) => {
    const response = await api.post('/api/users/register/', userData)
    return response.data
  },

  // Login user
  login: async (credentials) => {
    const response = await api.post('/api/users/login/', credentials)
    return response.data
  },

  // Logout user
  logout: async (refreshToken) => {
    const response = await api.post('/api/users/logout/', { refresh: refreshToken })
    return response.data
  },

  // Get current user profile
  getProfile: async () => {
    const response = await api.get('/api/users/profile/')
    return response.data
  },

  // Update profile
  updateProfile: async (data) => {
    const response = await api.put('/api/users/profile/', data)
    return response.data
  },

  // Get user streak info
  getStreak: async () => {
    const response = await api.get('/api/users/streak/')
    return response.data
  },

  // Get public user profile
  getUserProfile: async (username) => {
    const response = await api.get(`/api/users/${username}/`)
    return response.data
  },

  // Get leaderboard
  getLeaderboard: async (limit = 100) => {
    const response = await api.get(`/api/users/leaderboard/?limit=${limit}`)
    return response.data
  },
}

