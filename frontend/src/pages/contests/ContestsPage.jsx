import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { contestsAPI } from '../../services/contestsAPI'
import { useAuth } from '../../context/AuthContext'
import LoadingSpinner from '../../components/common/LoadingSpinner'
import { FiCode, FiUser, FiLogOut, FiUsers } from "react-icons/fi"
import { FaTrophy } from "react-icons/fa"
import { formatDate, getTimeRemaining } from '../../utils/helpers'

const ContestsPage = () => {
  const { isAuthenticated } = useAuth()
  const [contests, setContests] = useState([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('all')

  useEffect(() => {
    fetchContests()
  }, [filter])

  const fetchContests = async () => {
    try {
      setLoading(true)
      const params = {}
      if (filter === 'live') params.status = 'live'
      if (filter === 'upcoming') params.status = 'upcoming'
      if (filter === 'past') params.status = 'past'
      
      const data = await contestsAPI.getContests(params)
      setContests(data || [])
    } catch (error) {
      console.error('Error fetching contests:', error)
    } finally {
      setLoading(false)
    }
  }

  const getStatusBadge = (contest) => {
    const now = new Date()
    const start = new Date(contest.start_time)
    const end = new Date(contest.end_time)

    if (now < start) {
      return <span className="px-2 py-1 bg-blue-600 text-white text-xs rounded-full">Upcoming</span>
    } else if (now >= start && now <= end) {
      return <span className="px-2 py-1 bg-green-600 text-white text-xs rounded-full">Live</span>
    } else {
      return <span className="px-2 py-1 bg-gray-600 text-white text-xs rounded-full">Ended</span>
    }
  }

  if (loading) return <LoadingSpinner text="Loading contests..." />

  return (
    <div className="min-h-screen bg-gray-900 py-8">
      <div className="max-w-7xl mx-auto px-4">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-4xl font-bold text-white mb-2">Contests</h1>
            <p className="text-gray-400">Compete with others and climb the ranks</p>
          </div>

          {isAuthenticated && (
            <Link
              to="/contests/create"
              className="flex items-center gap-2 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition"
            >
              <FiPlus />
              Create Contest
            </Link>
          )}
        </div>

        {/* Filters */}
        <div className="flex gap-2 mb-6">
          {['all', 'live', 'upcoming', 'past'].map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                filter === f
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-800 text-gray-400 hover:text-white'
              }`}
            >
              {f.charAt(0).toUpperCase() + f.slice(1)}
            </button>
          ))}
        </div>

        {/* Contests Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {contests.map((contest) => (
            <Link
              key={contest.id}
              to={`/contests/${contest.slug}`}
              className="bg-gray-800 rounded-lg border border-gray-700 hover:border-blue-500 transition overflow-hidden"
            >
              <div className="p-6">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 bg-gradient-to-br from-yellow-500 to-orange-500 rounded-lg flex items-center justify-center">
                      <FiTrophy className="text-white text-2xl" />
                    </div>
                    {getStatusBadge(contest)}
                  </div>
                  {contest.is_official && (
                    <span className="px-2 py-1 bg-purple-600 text-white text-xs rounded-full">
                      Official
                    </span>
                  )}
                </div>

                <h3 className="text-xl font-bold text-white mb-2">{contest.title}</h3>
                <p className="text-gray-400 text-sm mb-4 line-clamp-2">{contest.description}</p>

                <div className="space-y-2 text-sm">
                  <div className="flex items-center gap-2 text-gray-400">
                    <FiClock className="text-blue-400" />
                    <span>{formatDate(contest.start_time)}</span>
                  </div>
                  <div className="flex items-center gap-2 text-gray-400">
                    <FiUsers className="text-green-400" />
                    <span>{contest.total_participants} participants</span>
                  </div>
                  {contest.status === 'LIVE' && (
                    <div className="text-green-400 font-medium">
                      Ends in: {getTimeRemaining(contest.end_time)}
                    </div>
                  )}
                </div>
              </div>
            </Link>
          ))}
        </div>

        {contests.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-400 text-lg">No contests found</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default ContestsPage