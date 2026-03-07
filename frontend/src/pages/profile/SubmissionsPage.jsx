import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { submissionsAPI } from '../../services/submissionsAPI'
import LoadingSpinner from '../../components/common/LoadingSpinner'
import { FiCheck, FiX, FiClock } from 'react-icons/fi'
import { formatRelativeTime, formatRuntime, formatMemory } from '../../utils/helpers'
import { STATUS_COLORS } from '../../utils/constants'

const SubmissionsPage = () => {
  const [submissions, setSubmissions] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchSubmissions()
  }, [])

  const fetchSubmissions = async () => {
    try {
      setLoading(true)
      const data = await submissionsAPI.getSubmissions()
      setSubmissions(data || [])
    } catch (error) {
      console.error('Error fetching submissions:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <LoadingSpinner text="Loading submissions..." />

  return (
    <div className="min-h-screen bg-gray-900 py-8">
      <div className="max-w-7xl mx-auto px-4">
        <h1 className="text-3xl font-bold text-white mb-8">My Submissions</h1>

        <div className="bg-gray-800 rounded-lg border border-gray-700 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-900 border-b border-gray-700">
                <tr>
                  <th className="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase">
                    Status
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase">
                    Problem
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase">
                    Language
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase">
                    Runtime
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase">
                    Memory
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase">
                    Time
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-700">
                {submissions.length === 0 ? (
                  <tr>
                    <td colSpan="6" className="px-6 py-8 text-center text-gray-400">
                      No submissions yet. Start solving problems!
                    </td>
                  </tr>
                ) : (
                  submissions.map((submission) => (
                    <tr key={submission.id} className="hover:bg-gray-700 transition">
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-2">
                          {submission.status === 'ACCEPTED' ? (
                            <FiCheck className="text-green-500 text-xl" />
                          ) : (
                            <FiX className="text-red-500 text-xl" />
                          )}
                          <span
                            className="text-sm font-medium"
                            style={{ color: STATUS_COLORS[submission.status] || '#6b7280' }}
                          >
                            {submission.status.replace(/_/g, ' ')}
                          </span>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <Link
                          to={`/problems/${submission.problem_slug}`}
                          className="text-white hover:text-blue-400 transition"
                        >
                          {submission.problem_title}
                        </Link>
                      </td>
                      <td className="px-6 py-4">
                        <span className="px-2 py-1 bg-gray-900 text-gray-300 text-xs rounded">
                          {submission.language}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-gray-400">
                        {formatRuntime(submission.runtime)}
                      </td>
                      <td className="px-6 py-4 text-gray-400">
                        {formatMemory(submission.memory)}
                      </td>
                      <td className="px-6 py-4 text-gray-400 text-sm">
                        <div className="flex items-center gap-1">
                          <FiClock className="text-gray-500" />
                          {formatRelativeTime(submission.created_at)}
                        </div>
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

export default SubmissionsPage