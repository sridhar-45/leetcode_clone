import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { groupsAPI } from '../../services/groupsAPI'
import { useAuth } from '../../context/AuthContext'
import LoadingSpinner from '../../components/common/LoadingSpinner'
import Button from '../../components/common/Button'
import toast from 'react-hot-toast'
import { FiUsers, FiTrophy, FiCode, FiLogOut } from 'react-icons/fi'

const GroupDetailPage = () => {
  const { slug } = useParams()
  const navigate = useNavigate()
  const { isAuthenticated, user } = useAuth()
  const [group, setGroup] = useState(null)
  const [members, setMembers] = useState([])
  const [loading, setLoading] = useState(true)
  const [joining, setJoining] = useState(false)
  const [showJoinCode, setShowJoinCode] = useState(false)
  const [joinCode, setJoinCode] = useState('')

  useEffect(() => {
    fetchGroup()
    fetchMembers()
  }, [slug])

  const fetchGroup = async () => {
    try {
      setLoading(true)
      const data = await groupsAPI.getGroupDetail(slug)
      setGroup(data)
    } catch (error) {
      console.error('Error fetching group:', error)
      toast.error('Failed to load group')
    } finally {
      setLoading(false)
    }
  }

  const fetchMembers = async () => {
    try {
      const data = await groupsAPI.getGroupMembers(slug)
      setMembers(data.members || [])
    } catch (error) {
      console.error('Error fetching members:', error)
    }
  }

  const handleJoin = async () => {
    if (!isAuthenticated) {
      toast.error('Please login to join group')
      navigate('/login')
      return
    }

    if (!group.is_public && !joinCode) {
      setShowJoinCode(true)
      return
    }

    try {
      setJoining(true)
      await groupsAPI.joinGroup(slug, group.is_public ? null : joinCode)
      toast.success('Successfully joined group!')
      fetchGroup()
      fetchMembers()
    } catch (error) {
      toast.error(error.response?.data?.error || 'Failed to join group')
    } finally {
      setJoining(false)
      setShowJoinCode(false)
    }
  }

  const handleLeave = async () => {
    if (!window.confirm('Are you sure you want to leave this group?')) return

    try {
      await groupsAPI.leaveGroup(slug)
      toast.success('Left group successfully')
      navigate('/groups')
    } catch (error) {
      toast.error(error.response?.data?.error || 'Failed to leave group')
    }
  }

  if (loading) return <LoadingSpinner text="Loading group..." />
  if (!group) return <div className="text-white">Group not found</div>

  const isMember = group.is_member

  return (
    <div className="min-h-screen bg-gray-900 py-8">
      <div className="max-w-7xl mx-auto px-4">
        {/* Header */}
        <div className="bg-gray-800 rounded-lg border border-gray-700 p-8 mb-6">
          <div className="flex items-start justify-between">
            <div className="flex items-start gap-4 flex-1">
              <div className="w-20 h-20 bg-gradient-to-br from-green-500 to-emerald-500 rounded-xl flex items-center justify-center">
                <FiUsers className="text-white text-4xl" />
              </div>

              <div className="flex-1">
                <h1 className="text-3xl font-bold text-white mb-2">{group.name}</h1>
                <p className="text-gray-400 mb-4">{group.description || 'No description'}</p>

                {!group.is_public && (
                  <div className="bg-yellow-900/20 border border-yellow-700 rounded-lg p-3 mb-4 inline-block">
                    <p className="text-yellow-400 text-sm">
                      🔒 Private Group • Join Code: <code className="bg-gray-900 px-2 py-1 rounded">{group.join_code}</code>
                    </p>
                  </div>
                )}

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div>
                    <div className="text-2xl font-bold text-white">{group.current_members}</div>
                    <div className="text-sm text-gray-400">Members</div>
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-green-500">{group.total_points}</div>
                    <div className="text-sm text-gray-400">Total Points</div>
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-yellow-500">#{group.global_rank}</div>
                    <div className="text-sm text-gray-400">Global Rank</div>
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-purple-500">{group.total_problems_solved}</div>
                    <div className="text-sm text-gray-400">Problems Solved</div>
                  </div>
                </div>
              </div>
            </div>

            <div>
              {!isMember ? (
                <Button onClick={handleJoin} variant="success" size="large" loading={joining}>
                  Join Group
                </Button>
              ) : (
                <button
                  onClick={handleLeave}
                  className="flex items-center gap-2 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition"
                >
                  <FiLogOut />
                  Leave Group
                </button>
              )}
            </div>
          </div>

          {/* Join Code Input */}
          {showJoinCode && (
            <div className="mt-4 bg-gray-900 rounded-lg p-4">
              <label className="block text-sm text-gray-400 mb-2">Enter Join Code</label>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={joinCode}
                  onChange={(e) => setJoinCode(e.target.value.toUpperCase())}
                  placeholder="XXXXXX"
                  className="flex-1 px-4 py-2 bg-gray-800 border border-gray-700 rounded text-white"
                  maxLength={6}
                />
                <Button onClick={handleJoin} loading={joining}>
                  Join
                </Button>
              </div>
            </div>
          )}
        </div>

        {/* Members List */}
        <div className="bg-gray-800 rounded-lg border border-gray-700 p-6">
          <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <FiUsers className="text-green-500" />
            Members ({members.length})
          </h2>

          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="border-b border-gray-700">
                <tr>
                  <th className="px-4 py-3 text-left text-sm text-gray-400">Rank</th>
                  <th className="px-4 py-3 text-left text-sm text-gray-400">Member</th>
                  <th className="px-4 py-3 text-left text-sm text-gray-400">Role</th>
                  <th className="px-4 py-3 text-left text-sm text-gray-400">Contribution</th>
                  <th className="px-4 py-3 text-left text-sm text-gray-400">Problems</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-700">
                {members.map((member, index) => (
                  <tr key={member.id} className="hover:bg-gray-700 transition">
                    <td className="px-4 py-3 text-gray-400">#{index + 1}</td>
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-2">
                        <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center text-white text-sm font-semibold">
                          {member.user.username?.charAt(0).toUpperCase()}
                        </div>
                        <span className="text-white">{member.user.username}</span>
                      </div>
                    </td>
                    <td className="px-4 py-3">
                      <span
                        className={`px-2 py-1 rounded text-xs ${
                          member.role === 'ADMIN'
                            ? 'bg-purple-600 text-white'
                            : 'bg-gray-700 text-gray-300'
                        }`}
                      >
                        {member.role}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-green-500 font-semibold">
                      {member.points_contributed} pts
                    </td>
                    <td className="px-4 py-3 text-gray-400">{member.problems_solved}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  )
}

export default GroupDetailPage