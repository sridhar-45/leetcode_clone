import api from './api'

export const groupsAPI = {
  // Get all groups
  getGroups: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString()
    const response = await api.get(`/api/groups/?${queryString}`)
    return response.data
  },

  // Get group details
  getGroupDetail: async (slug) => {
    const response = await api.get(`/api/groups/${slug}/`)
    return response.data
  },

  // Create new group
  createGroup: async (data) => {
    const response = await api.post('/api/groups/create/', data)
    return response.data
  },

  // Join group
  joinGroup: async (slug, joinCode = null) => {
    const data = joinCode ? { join_code: joinCode } : {}
    const response = await api.post(`/api/groups/${slug}/join/`, data)
    return response.data
  },

  // Leave group
  leaveGroup: async (slug) => {
    const response = await api.post(`/api/groups/${slug}/leave/`)
    return response.data
  },

  // Get group members
  getGroupMembers: async (slug) => {
    const response = await api.get(`/api/groups/${slug}/members/`)
    return response.data
  },

  // Get user's groups
  getMyGroups: async () => {
    const response = await api.get('/api/groups/my/')
    return response.data
  },

  // Invite user to group
  inviteToGroup: async (slug, username, message = '') => {
    const response = await api.post(`/api/groups/${slug}/invite/`, {
      username,
      message,
    })
    return response.data
  },

  // Get group leaderboard
  getGroupLeaderboard: async (limit = 100) => {
    const response = await api.get(`/api/leaderboard/groups/?limit=${limit}`)
    return response.data
  },
}
