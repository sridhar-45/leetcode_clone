import api from './api'

export const problemsAPI = {
  // Get all problems with filters
  getProblems: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString()
    const response = await api.get(`/api/problems/?${queryString}`)
    return response.data
  },

  // Get single problem details
  getProblemDetail: async (slug) => {
    const response = await api.get(`/api/problems/${slug}/`)
    return response.data
  },

  // Get all topics
  getTopics: async () => {
    const response = await api.get('/api/problems/topics/')
    return response.data
  },

  // Get all tags
  getTags: async () => {
    const response = await api.get('/api/problems/tags/')
    return response.data
  },

  // Get random problem
  getRandomProblem: async (difficulty = null) => {
    const url = difficulty 
      ? `/api/problems/random/?difficulty=${difficulty}`
      : '/api/problems/random/'
    const response = await api.get(url)
    return response.data
  },

  // Get daily problem
  getDailyProblem: async () => {
    const response = await api.get('/api/users/daily-problem/')
    return response.data
  },
}