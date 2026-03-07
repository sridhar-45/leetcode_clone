import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { contestsAPI } from '../../services/contestsAPI'
import { problemsAPI } from '../../services/problemsAPI'
import Button from '../../components/common/Button'
import toast from 'react-hot-toast'
import { FiPlus, FiX } from 'react-icons/fi'

const CreateContestPage = () => {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [problems, setProblems] = useState([])
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    start_time: '',
    duration_minutes: 120,
    is_public: true,
    max_participants: 100,
    min_participants: 2,
    problem_ids: [],
  })

  useEffect(() => {
    fetchProblems()
  }, [])

  const fetchProblems = async () => {
    try {
      const data = await problemsAPI.getProblems()
      setProblems(data.results || data)
    } catch (error) {
      console.error('Error fetching problems:', error)
    }
  }

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value,
    })
  }

  const toggleProblem = (problemId) => {
    setFormData({
      ...formData,
      problem_ids: formData.problem_ids.includes(problemId)
        ? formData.problem_ids.filter((id) => id !== problemId)
        : [...formData.problem_ids, problemId],
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (formData.problem_ids.length === 0) {
      toast.error('Please select at least one problem')
      return
    }

    try {
      setLoading(true)
      
      // Calculate end_time
      const startTime = new Date(formData.start_time)
      const endTime = new Date(startTime.getTime() + formData.duration_minutes * 60000)

      const contestData = {
        ...formData,
        end_time: endTime.toISOString(),
      }

      const contest = await contestsAPI.createContest(contestData)
      toast.success('Contest created successfully!')
      navigate(`/contests/${contest.slug}`)
    } catch (error) {
      toast.error(error.response?.data?.error || 'Failed to create contest')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-900 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <h1 className="text-3xl font-bold text-white mb-8">Create Contest</h1>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Basic Info */}
          <div className="bg-gray-800 rounded-lg border border-gray-700 p-6">
            <h2 className="text-xl font-semibold text-white mb-4">Basic Information</h2>

            <div className="space-y-4">
              <div>
                <label className="block text-sm text-gray-400 mb-2">Contest Title *</label>
                <input
                  type="text"
                  name="title"
                  value={formData.title}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded text-white"
                  placeholder="My Awesome Contest"
                />
              </div>

              <div>
                <label className="block text-sm text-gray-400 mb-2">Description *</label>
                <textarea
                  name="description"
                  value={formData.description}
                  onChange={handleChange}
                  required
                  rows={4}
                  className="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded text-white"
                  placeholder="Describe your contest..."
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm text-gray-400 mb-2">Start Time *</label>
                  <input
                    type="datetime-local"
                    name="start_time"
                    value={formData.start_time}
                    onChange={handleChange}
                    required
                    className="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded text-white"
                  />
                </div>

                <div>
                  <label className="block text-sm text-gray-400 mb-2">Duration (minutes) *</label>
                  <input
                    type="number"
                    name="duration_minutes"
                    value={formData.duration_minutes}
                    onChange={handleChange}
                    required
                    min="30"
                    className="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded text-white"
                  />
                </div>
              </div>

              <div className="flex items-center gap-2">
                <input
                  type="checkbox"
                  name="is_public"
                  checked={formData.is_public}
                  onChange={handleChange}
                  className="w-4 h-4"
                />
                <label className="text-sm text-gray-400">
                  Public contest (anyone can join)
                </label>
              </div>
            </div>
          </div>

          {/* Problem Selection */}
          <div className="bg-gray-800 rounded-lg border border-gray-700 p-6">
            <h2 className="text-xl font-semibold text-white mb-4">
              Select Problems ({formData.problem_ids.length} selected)
            </h2>

            <div className="max-h-96 overflow-y-auto space-y-2">
              {problems.map((problem) => (
                <div
                  key={problem.id}
                  onClick={() => toggleProblem(problem.id)}
                  className={`p-4 rounded-lg cursor-pointer transition ${
                    formData.problem_ids.includes(problem.id)
                      ? 'bg-blue-900/30 border-2 border-blue-500'
                      : 'bg-gray-900 border border-gray-700 hover:border-gray-600'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="text-white font-medium">{problem.title}</div>
                      <div className="text-sm text-gray-400">
                        {problem.difficulty} • {problem.points} points
                      </div>
                    </div>
                    {formData.problem_ids.includes(problem.id) && (
                      <FiPlus className="text-blue-500 text-xl transform rotate-45" />
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Submit */}
          <div className="flex items-center justify-end gap-4">
            <button
              type="button"
              onClick={() => navigate('/contests')}
              className="px-6 py-3 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition"
            >
              Cancel
            </button>
            <Button type="submit" variant="primary" size="large" loading={loading}>
              Create Contest
            </Button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default CreateContestPage