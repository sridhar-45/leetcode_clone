import api from './api'

export const contestsAPI = {
  // Get all contests
  getContests: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString()
    const response = await api.get(`/api/contests/?${queryString}`)
    return response.data
  },

  // Get contest details
  getContestDetail: async (slug) => {
    const response = await api.get(`/api/contests/${slug}/`)
    return response.data
  },

  // Create new contest
  createContest: async (data) => {
    const response = await api.post('/api/contests/create/', data)
    return response.data
  },

  // Join contest
  joinContest: async (slug, joinCode = null) => {
    const data = joinCode ? { join_code: joinCode } : {}
    const response = await api.post(`/api/contests/${slug}/join/`, data)
    return response.data
  },

  // Get contest leaderboard
  getContestLeaderboard: async (slug) => {
    const response = await api.get(`/api/contests/${slug}/leaderboard/`)
    return response.data
  },

  // Get user's contests
  getMyContests: async () => {
    const response = await api.get('/api/contests/my/')
    return response.data
  },

  // Get contests user created
  getCreatedContests: async () => {
    const response = await api.get('/api/contests/created/')
    return response.data
  },
}

