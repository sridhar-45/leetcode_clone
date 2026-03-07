import { useState, useEffect } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { contestsAPI } from '../../services/contestsAPI'
import { useAuth } from '../../context/AuthContext'
import LoadingSpinner from '../../components/common/LoadingSpinner'
import Button from '../../components/common/Button'
import toast from 'react-hot-toast'
import { FiCode, FiUser, FiLogOut, FiUsers } from "react-icons/fi";
import { FaTrophy } from "react-icons/fa";
import { formatDate, getTimeRemaining } from '../../utils/helpers'

const ContestDetailPage = () => {
  const { slug } = useParams()
  const navigate = useNavigate()
  const { isAuthenticated } = useAuth()
  const [contest, setContest] = useState(null)
  const [leaderboard, setLeaderboard] = useState([])
  const [loading, setLoading] = useState(true)
  const [joining, setJoining] = useState(false)
  const [showJoinCode, setShowJoinCode] = useState(false)
  const [joinCode, setJoinCode] = useState('')

  useEffect(() => {
    fetchContest()
    fetchLeaderboard()
  }, [slug])

  const fetchContest = async () => {
    try {
      setLoading(true)
      const data = await contestsAPI.getContestDetail(slug)
      setContest(data)
    } catch (error) {
      console.error('Error fetching contest:', error)
      toast.error('Failed to load contest')
    } finally {
      setLoading(false)
    }
  }

  const fetchLeaderboard = async () => {
    try {
      const data = await contestsAPI.getContestLeaderboard(slug)
      setLeaderboard(data.leaderboard || [])
    } catch (error) {
      console.error('Error fetching leaderboard:', error)
    }
  }

  const handleJoin = async () => {
    if (!isAuthenticated) {
      toast.error('Please login to join contest')
      navigate('/login')
      return
    }

    if (!contest.is_public && !joinCode) {
      setShowJoinCode(true)
      return
    }

    try {
      setJoining(true)
      await contestsAPI.joinContest(slug, contest.is_public ? null : joinCode)
      toast.success('Successfully joined contest!')
      fetchContest()
      fetchLeaderboard()
    } catch (error) {
      toast.error(error.response?.data?.error || 'Failed to join contest')
    } finally {
      setJoining(false)
      setShowJoinCode(false)
    }
  }

  if (loading) return <LoadingSpinner text="Loading contest..." />
  if (!contest) return <div className="text-white">Contest not found</div>

  const isParticipating = leaderboard.some(p => p.user?.username === 'current_user')

  return (
    <div className="min-h-screen bg-gray-900 py-8">
      <div className="max-w-7xl mx-auto px-4">
        {/* Header */}
        <div className="bg-gray-800 rounded-lg border border-gray-700 p-8 mb-6">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <h1 className="text-3xl font-bold text-white mb-4">{contest.title}</h1>
              <p className="text-gray-400 mb-6">{contest.description}</p>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                <div className="flex items-center gap-3">
                  <FiClock className="text-blue-400 text-2xl" />
                  <div>
                    <div className="text-sm text-gray-400">Starts</div>
                    <div className="text-white">{formatDate(contest.start_time)}</div>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <FiUsers className="text-green-400 text-2xl" />
                  <div>
                    <div className="text-sm text-gray-400">Participants</div>
                    <div className="text-white">{contest.total_participants}</div>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <FiCode className="text-purple-400 text-2xl" />
                  <div>
                    <div className="text-sm text-gray-400">Problems</div>
                    <div className="text-white">{contest.problems?.length || 0}</div>
                  </div>
                </div>
              </div>

              {!contest.is_public && (
                <div className="bg-yellow-900/20 border border-yellow-700 rounded-lg p-4 mb-4">
                  <p className="text-yellow-400 text-sm">
                    🔒 This is a private contest. You need a join code to participate.
                  </p>
                </div>
              )}
            </div>

            <div>
              {!isParticipating && (
                <Button
                  onClick={handleJoin}
                  variant="success"
                  size="large"
                  loading={joining}
                >
                  Join Contest
                </Button>
              )}
            </div>
          </div>

          {/* Join Code Modal */}
          {showJoinCode && (
            <div className="mt-4 bg-gray-900 rounded-lg p-4">
              <label className="block text-sm text-gray-400 mb-2">Enter Join Code</label>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={joinCode}
                  onChange={(e) => setJoinCode(e.target.value.toUpperCase())}
                  placeholder="XXXXXXXX"
                  className="flex-1 px-4 py-2 bg-gray-800 border border-gray-700 rounded text-white"
                  maxLength={8}
                />
                <Button onClick={handleJoin} loading={joining}>
                  Join
                </Button>
              </div>
            </div>
          )}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Problems List */}
          <div className="lg:col-span-2">
            <div className="bg-gray-800 rounded-lg border border-gray-700 p-6">
              <h2 className="text-xl font-bold text-white mb-4">Problems</h2>
              <div className="space-y-3">
                {contest.problems?.map((contestProblem, index) => (
                  <Link
                    key={contestProblem.id}
                    to={`/problems/${contestProblem.problem.slug}`}
                    className="flex items-center justify-between p-4 bg-gray-900 rounded-lg hover:bg-gray-700 transition"
                  >
                    <div className="flex items-center gap-4">
                      <span className="text-2xl font-bold text-gray-500">
                        {String.fromCharCode(65 + index)}
                      </span>
                      <div>
                        <div className="text-white font-medium">
                          {contestProblem.problem.title}
                        </div>
                        <div className="text-sm text-gray-400">
                          {contestProblem.points} points
                        </div>
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
            </div>
          </div>

          {/* Leaderboard */}
          <div>
            <div className="bg-gray-800 rounded-lg border border-gray-700 p-6">
              <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                <FiTrophy className="text-yellow-500" />
                Leaderboard
              </h2>
              <div className="space-y-2">
                {leaderboard.slice(0, 10).map((participant, index) => (
                  <div
                    key={participant.id}
                    className="flex items-center gap-3 p-3 bg-gray-900 rounded-lg"
                  >
                    <span
                      className={`text-lg font-bold ${
                        index === 0
                          ? 'text-yellow-500'
                          : index === 1
                          ? 'text-gray-400'
                          : index === 2
                          ? 'text-orange-600'
                          : 'text-gray-500'
                      }`}
                    >
                      #{index + 1}
                    </span>
                    <div className="flex-1">
                      <div className="text-white text-sm">{participant.user.username}</div>
                      <div className="text-xs text-gray-400">
                        {participant.problems_solved} solved • {participant.total_score} pts
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ContestDetailPage
