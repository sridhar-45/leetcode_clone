// """
// ═══════════════════════════════════════════════════════════════
// FILE 35: pages/LeaderboardPage.jsx
// Location: frontend/src/pages/LeaderboardPage.jsx
// LEADERBOARD PAGE - Global rankings
// ═══════════════════════════════════════════════════════════════
// """

import { useState, useEffect } from 'react'
import { authAPI } from '../services/authAPI'
import { groupsAPI } from '../services/groupsAPI'
import LoadingSpinner from '../components/common/LoadingSpinner'
import ErrorMessage from '../components/common/ErrorMessage'
import { FiTrophy, FiUsers } from 'react-icons/fi'

const LeaderboardPage = () => {
  const [activeTab, setActiveTab] = useState('users')
  const [users, setUsers] = useState([])
  const [groups, setGroups] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (activeTab === 'users') {
      fetchUserLeaderboard()
    } else {
      fetchGroupLeaderboard()
    }
  }, [activeTab])

  const fetchUserLeaderboard = async () => {
    try {
      setLoading(true)
      const data = await authAPI.getLeaderboard(100)
      setUsers(data.users || [])
      setError(null)
    } catch (err) {
      setError('Failed to load leaderboard')
    } finally {
      setLoading(false)
    }
  }

  const fetchGroupLeaderboard = async () => {
    try {
      setLoading(true)
      const data = await groupsAPI.getGroupLeaderboard(100)
      setGroups(data.leaderboard || [])
      setError(null)
    } catch (err) {
      setError('Failed to load group leaderboard')
    } finally {
      setLoading(false)
    }
  }

  const getRankColor = (rank) => {
    if (rank === 1) return 'text-yellow-500'
    if (rank === 2) return 'text-gray-400'
    if (rank === 3) return 'text-orange-600'
    return 'text-gray-500'
  }

  const getRankIcon = (rank) => {
    if (rank <= 3) return '🏆'
    return '#' + rank
  }

  return (
    <div className="min-h-screen bg-gray-900 py-8">
      <div className="max-w-6xl mx-auto px-4">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">Leaderboard</h1>
          <p className="text-gray-400">Top performers across the platform</p>
        </div>

        {/* Tabs */}
        <div className="flex gap-2 mb-6">
          <button
            onClick={() => setActiveTab('users')}
            className={`flex items-center gap-2 px-6 py-3 rounded-lg font-medium transition ${
              activeTab === 'users'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-800 text-gray-400 hover:text-white'
            }`}
          >
            <FiTrophy />
            Users
          </button>
          <button
            onClick={() => setActiveTab('groups')}
            className={`flex items-center gap-2 px-6 py-3 rounded-lg font-medium transition ${
              activeTab === 'groups'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-800 text-gray-400 hover:text-white'
            }`}
          >
            <FiUsers />
            Groups
          </button>
        </div>

        {/* Content */}
        {loading ? (
          <LoadingSpinner text="Loading leaderboard..." />
        ) : error ? (
          <ErrorMessage
            message={error}
            onRetry={activeTab === 'users' ? fetchUserLeaderboard : fetchGroupLeaderboard}
          />
        ) : (
          <div className="bg-gray-800 rounded-lg border border-gray-700">
            {activeTab === 'users' ? (
              /* Users Leaderboard */
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-900 border-b border-gray-700">
                    <tr>
                      <th className="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase">
                        Rank
                      </th>
                      <th className="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase">
                        User
                      </th>
                      <th className="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase">
                        Solved
                      </th>
                      <th className="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase">
                        Points
                      </th>
                      <th className="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase">
                        Streak
                      </th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-700">
                    {users.map((user, index) => (
                      <tr key={user.id} className="hover:bg-gray-700 transition">
                        <td className="px-6 py-4">
                          <span className={`text-2xl font-bold ${getRankColor(index + 1)}`}>
                            {getRankIcon(index + 1)}
                          </span>
                        </td>
                        <td className="px-6 py-4">
                          <div className="flex items-center gap-3">
                            <div className="w-10 h-10 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center text-white font-semibold">
                              {user.username?.charAt(0).toUpperCase()}
                            </div>
                            <div>
                              <div className="text-white font-medium">{user.username}</div>
                              <div className="text-sm text-gray-400">
                                {user.first_name} {user.last_name}
                              </div>
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4">
                          <div className="text-white">{user.problems_solved}</div>
                          <div className="text-xs text-gray-400">
                            <span className="text-green-500">{user.easy_solved}E</span> /{' '}
                            <span className="text-yellow-500">{user.medium_solved}M</span> /{' '}
                            <span className="text-red-500">{user.hard_solved}H</span>
                          </div>
                        </td>
                        <td className="px-6 py-4">
                          <div className="text-xl font-bold text-blue-500">
                            {user.total_points}
                          </div>
                        </td>
                        <td className="px-6 py-4">
                          <div className="text-white">{user.current_streak} days</div>
                          <div className="text-xs text-gray-400">
                            Best: {user.longest_streak}
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              /* Groups Leaderboard */
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-900 border-b border-gray-700">
                    <tr>
                      <th className="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase">
                        Rank
                      </th>
                      <th className="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase">
                        Group
                      </th>
                      <th className="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase">
                        Members
                      </th>
                      <th className="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase">
                        Points
                      </th>
                      <th className="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase">
                        Avg Points
                      </th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-700">
                    {groups.map((group, index) => (
                      <tr key={group.id} className="hover:bg-gray-700 transition">
                        <td className="px-6 py-4">
                          <span className={`text-2xl font-bold ${getRankColor(index + 1)}`}>
                            {getRankIcon(index + 1)}
                          </span>
                        </td>
                        <td className="px-6 py-4">
                          <div className="flex items-center gap-3">
                            <div className="w-10 h-10 rounded-lg bg-gradient-to-r from-green-500 to-emerald-500 flex items-center justify-center">
                              <FiUsers className="text-white" />
                            </div>
                            <div>
                              <div className="text-white font-medium">{group.name}</div>
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4 text-white">
                          {group.current_members}
                        </td>
                        <td className="px-6 py-4">
                          <div className="text-xl font-bold text-green-500">
                            {group.total_points}
                          </div>
                        </td>
                        <td className="px-6 py-4 text-gray-400">
                          {Math.round(group.total_points / group.current_members)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default LeaderboardPage