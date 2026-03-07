import api from './api'

export const submissionsAPI = {
  // Submit code for judging
  submitCode: async (problemSlug, code, language) => {
    const response = await api.post('/api/submissions/submit/', {
      problem_slug: problemSlug,
      code: code,
      language: language,
    })
    return response.data
  },

  // Run code against public test cases only
  runCode: async (problemSlug, code, language) => {
    const response = await api.post('/api/submissions/run/', {
      problem_slug: problemSlug,
      code: code,
      language: language,
    })
    return response.data
  },

  // Get user's submission history
  getSubmissions: async (problemSlug = null) => {
    const url = problemSlug 
      ? `/api/submissions/?problem=${problemSlug}`
      : '/api/submissions/'
    const response = await api.get(url)
    return response.data
  },

  // Get single submission details
  getSubmission: async (id) => {
    const response = await api.get(`/api/submissions/${id}/`)
    return response.data
  },
}

