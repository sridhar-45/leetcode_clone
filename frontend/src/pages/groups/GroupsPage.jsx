import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { groupsAPI } from '../../services/groupsAPI'
import { useAuth } from '../../context/AuthContext'
import LoadingSpinner from '../../components/common/LoadingSpinner'
import { FiUsers, FiPlus, FiTrendingUp } from 'react-icons/fi'

const GroupsPage = () => {
  const { isAuthenticated } = useAuth()
  const [groups, setGroups] = useState([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('all')

  useEffect(() => {
    fetchGroups()
  }, [filter])

  const fetchGroups = async () => {
    try {
      setLoading(true)
      const params = filter === 'public' ? { visibility: 'public' } : {}
      const data = await groupsAPI.getGroups(params)
      setGroups(data || [])
    } catch (error) {
      console.error('Error fetching groups:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <LoadingSpinner text="Loading groups..." />

  return (
    <div className="min-h-screen bg-gray-900 py-8">
      <div className="max-w-7xl mx-auto px-4">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-4xl font-bold text-white mb-2">Groups</h1>
            <p className="text-gray-400">Join groups and compete together</p>
          </div>

          {isAuthenticated && (
            <Link
              to="/groups/create"
              className="flex items-center gap-2 px-6 py-3 bg-green-600 hover:bg-green-700 text-white rounded-lg transition"
            >
              <FiPlus />
              Create Group
            </Link>
          )}
        </div>

        {/* Filters */}
        <div className="flex gap-2 mb-6">
          {['all', 'public'].map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                filter === f
                  ? 'bg-green-600 text-white'
                  : 'bg-gray-800 text-gray-400 hover:text-white'
              }`}
            >
              {f.charAt(0).toUpperCase() + f.slice(1)}
            </button>
          ))}
        </div>

        {/* Groups Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {groups.map((group) => (
            <Link
              key={group.id}
              to={`/groups/${group.slug}`}
              className="bg-gray-800 rounded-lg border border-gray-700 hover:border-green-500 transition overflow-hidden"
            >
              <div className="p-6">
                <div className="flex items-start justify-between mb-4">
                  <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-emerald-500 rounded-lg flex items-center justify-center">
                    <FiUsers className="text-white text-2xl" />
                  </div>
                  {!group.is_public && (
                    <span className="px-2 py-1 bg-yellow-600 text-white text-xs rounded-full">
                      Private
                    </span>
                  )}
                </div>

                <h3 className="text-xl font-bold text-white mb-2">{group.name}</h3>
                <p className="text-gray-400 text-sm mb-4 line-clamp-2">
                  {group.description || 'No description'}
                </p>

                <div className="space-y-2 text-sm">
                  <div className="flex items-center justify-between">
                    <span className="text-gray-400">Members</span>
                    <span className="text-white font-medium">
                      {group.current_members} / {group.max_members}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-gray-400">Total Points</span>
                    <span className="text-green-500 font-bold">{group.total_points}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-gray-400">Rank</span>
                    <span className="text-yellow-500 font-medium">#{group.global_rank}</span>
                  </div>
                </div>
              </div>
            </Link>
          ))}
        </div>

        {groups.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-400 text-lg">No groups found</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default GroupsPage