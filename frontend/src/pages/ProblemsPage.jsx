
// ═══════════════════════════════════════════════════════════════
// FILE 29: pages/ProblemsPage.jsx
// Location: frontend/src/pages/ProblemsPage.jsx
// PROBLEMS LIST PAGE - Shows all problems with filters
// ═══════════════════════════════════════════════════════════════

import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { problemsAPI } from '../services/problemsAPI'
import { useAuth } from '../context/AuthContext'
import DifficultyBadge from '../components/problem/DifficultyBadge'
import TopicTag from '../components/problem/TopicTag'
import LoadingSpinner from '../components/common/LoadingSpinner'
import ErrorMessage from '../components/common/ErrorMessage'
import { FiCheck, FiSearch, FiFilter } from 'react-icons/fi'

const ProblemsPage = () => {
  const { isAuthenticated } = useAuth()
  const [problems, setProblems] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  
  // Filters
  const [difficulty, setDifficulty] = useState('')
  const [status, setStatus] = useState('')
  const [searchTerm, setSearchTerm] = useState('')
  const [topics, setTopics] = useState([])
  const [selectedTopic, setSelectedTopic] = useState('')

  useEffect(() => {
    fetchProblems()
    fetchTopics()
  }, [difficulty, status, selectedTopic])

  const fetchProblems = async () => {
    try {
      setLoading(true)
      const params = {}
      
      if (difficulty) params.difficulty = difficulty
      if (status) params.status = status
      if (selectedTopic) params.topic = selectedTopic
      
      const data = await problemsAPI.getProblems(params)
      setProblems(data.results || data)
      setError(null)
    } catch (err) {
      console.error('Error fetching problems:', err)
      setError('Failed to load problems')
    } finally {
      setLoading(false)
    }
  }

  const fetchTopics = async () => {
    try {
      const data = await problemsAPI.getTopics()
      setTopics(data || [])
    } catch (err) {
      console.error('Error fetching topics:', err)
    }
  }

  // Filter problems by search term
  const filteredProblems = problems.filter(problem =>
    problem.title.toLowerCase().includes(searchTerm.toLowerCase())
  )

  if (loading) {
    return <LoadingSpinner text="Loading problems..." />
  }

  if (error) {
    return <ErrorMessage message={error} onRetry={fetchProblems} />
  }

  return (
    <div className="min-h-screen bg-gray-900 py-8">
      <div className="max-w-7xl mx-auto px-4">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">Problems</h1>
          <p className="text-gray-400">Solve coding problems and improve your skills</p>
        </div>

        {/* Filters */}
        <div className="bg-gray-800 rounded-lg p-6 mb-6 border border-gray-700">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {/* Search */}
            <div className="md:col-span-2">
              <div className="relative">
                <FiSearch className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search problems..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
                />
              </div>
            </div>

            {/* Difficulty Filter */}
            <div>
              <select
                value={difficulty}
                onChange={(e) => setDifficulty(e.target.value)}
                className="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-blue-500"
              >
                <option value="">All Difficulties</option>
                <option value="EASY">Easy</option>
                <option value="MEDIUM">Medium</option>
                <option value="HARD">Hard</option>
              </select>
            </div>

            {/* Status Filter (only for authenticated users) */}
            {isAuthenticated && (
              <div>
                <select
                  value={status}
                  onChange={(e) => setStatus(e.target.value)}
                  className="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-blue-500"
                >
                  <option value="">All Status</option>
                  <option value="solved">Solved</option>
                  <option value="unsolved">Unsolved</option>
                </select>
              </div>
            )}
          </div>

          {/* Topic Filter */}
          {topics.length > 0 && (
            <div className="mt-4">
              <div className="flex items-center gap-2 flex-wrap">
                <FiFilter className="text-gray-400" />
                <button
                  onClick={() => setSelectedTopic('')}
                  className={`px-3 py-1 rounded-lg text-sm transition ${
                    selectedTopic === ''
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                  }`}
                >
                  All Topics
                </button>
                {topics.slice(0, 10).map((topic) => (
                  <button
                    key={topic.slug}
                    onClick={() => setSelectedTopic(topic.slug)}
                    className={`px-3 py-1 rounded-lg text-sm transition ${
                      selectedTopic === topic.slug
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                    }`}
                  >
                    {topic.name}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
            <div className="text-2xl font-bold text-white">{filteredProblems.length}</div>
            <div className="text-sm text-gray-400">Total Problems</div>
          </div>
          <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
            <div className="text-2xl font-bold text-green-500">
              {filteredProblems.filter(p => p.difficulty === 'EASY').length}
            </div>
            <div className="text-sm text-gray-400">Easy</div>
          </div>
          <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
            <div className="text-2xl font-bold text-yellow-500">
              {filteredProblems.filter(p => p.difficulty === 'MEDIUM').length}
            </div>
            <div className="text-sm text-gray-400">Medium</div>
          </div>
          <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
            <div className="text-2xl font-bold text-red-500">
              {filteredProblems.filter(p => p.difficulty === 'HARD').length}
            </div>
            <div className="text-sm text-gray-400">Hard</div>
          </div>
        </div>

        {/* Problems Table */}
        <div className="bg-gray-800 rounded-lg border border-gray-700 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-900 border-b border-gray-700">
                <tr>
                  <th className="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase tracking-wider w-12">
                    Status
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                    Title
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                    Difficulty
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                    Topics
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                    Acceptance
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-700">
                {filteredProblems.length === 0 ? (
                  <tr>
                    <td colSpan="5" className="px-6 py-8 text-center text-gray-400">
                      No problems found matching your filters
                    </td>
                  </tr>
                ) : (
                  filteredProblems.map((problem) => (
                    <tr
                      key={problem.id}
                      className="hover:bg-gray-700 transition cursor-pointer"
                      onClick={() => window.location.href = `/problems/${problem.slug}`}
                    >
                      <td className="px-6 py-4">
                        {problem.is_solved && (
                          <FiCheck className="text-green-500 text-xl" />
                        )}
                      </td>
                      <td className="px-6 py-4">
                        <Link
                          to={`/problems/${problem.slug}`}
                          className="text-white hover:text-blue-400 font-medium transition"
                        >
                          {problem.id}. {problem.title}
                        </Link>
                      </td>
                      <td className="px-6 py-4">
                        <DifficultyBadge difficulty={problem.difficulty} />
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex gap-2 flex-wrap">
                          {problem.topics?.slice(0, 2).map((topic) => (
                            <TopicTag key={topic.slug} topic={topic.name} />
                          ))}
                          {problem.topics?.length > 2 && (
                            <span className="text-xs text-gray-400">
                              +{problem.topics.length - 2}
                            </span>
                          )}
                        </div>
                      </td>
                      <td className="px-6 py-4 text-gray-400">
                        {problem.acceptance_rate.toFixed(1)}%
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ProblemsPage