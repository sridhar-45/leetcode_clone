import { useAuth } from '../../context/AuthContext'
import { FiCode, FiZap, FiTrendingUp } from "react-icons/fi";
import { FaTrophy } from "react-icons/fa";


const ProfilePage = () => {
  const { user } = useAuth()

  if (!user) return null

  const stats = [
    { label: 'Total Points', value: user.total_points, icon: FaTrophy, color: 'text-yellow-500' },
    { label: 'Problems Solved', value: user.problems_solved, icon: FiCode, color: 'text-blue-500' },
    { label: 'Current Streak', value: `${user.current_streak} days`, icon: FiZap, color: 'text-green-500' },
    { label: 'Global Rank', value: `#${user.global_ranking || 'Unranked'}`, icon: FiTrendingUp, color: 'text-purple-500' },
  ]

  const difficultyStats = [
    { label: 'Easy', count: user.easy_solved, color: 'bg-green-500' },
    { label: 'Medium', count: user.medium_solved, color: 'bg-yellow-500' },
    { label: 'Hard', count: user.hard_solved, color: 'bg-red-500' },
  ]

  return (
    <div className="min-h-screen bg-gray-900 py-8">
      <div className="max-w-6xl mx-auto px-4">
        {/* Profile Header */}
        <div className="bg-gray-800 rounded-lg border border-gray-700 p-8 mb-6">
          <div className="flex items-start gap-6">
            <div className="w-24 h-24 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center text-white text-4xl font-bold">
              {user.username.charAt(0).toUpperCase()}
            </div>

            <div className="flex-1">
              <h1 className="text-3xl font-bold text-white mb-2">{user.username}</h1>
              <p className="text-gray-400 mb-4">{user.email}</p>

              {user.bio && (
                <p className="text-gray-300 mb-4">{user.bio}</p>
              )}

              <div className="flex items-center gap-4 text-sm text-gray-400">
                {user.location && (
                  <span>📍 {user.location}</span>
                )}
                {user.website && (
                  <a href={user.website} target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:underline">
                    🔗 {user.website}
                  </a>
                )}
                {user.github_username && (
                  <a href={`https://github.com/${user.github_username}`} target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:underline">
                    GitHub: @{user.github_username}
                  </a>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          {stats.map((stat, index) => {
            const Icon = stat.icon
            return (
              <div key={index} className="bg-gray-800 rounded-lg border border-gray-700 p-6">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-gray-400 text-sm">{stat.label}</span>
                  <Icon className={`${stat.color} text-2xl`} />
                </div>
                <div className="text-3xl font-bold text-white">{stat.value}</div>
              </div>
            )
          })}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Problem Breakdown */}
          <div className="bg-gray-800 rounded-lg border border-gray-700 p-6">
            <h2 className="text-xl font-bold text-white mb-6">Problem Breakdown</h2>

            <div className="space-y-4">
              {difficultyStats.map((stat, index) => (
                <div key={index}>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-gray-400">{stat.label}</span>
                    <span className="text-white font-semibold">{stat.count}</span>
                  </div>
                  <div className="h-2 bg-gray-700 rounded-full overflow-hidden">
                    <div
                      className={`h-full ${stat.color}`}
                      style={{
                        width: `${user.problems_solved > 0 ? (stat.count / user.problems_solved) * 100 : 0}%`,
                      }}
                    />
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-6 pt-6 border-t border-gray-700">
              <div className="flex items-center justify-between">
                <span className="text-gray-400">Acceptance Rate</span>
                <span className="text-green-500 font-bold text-xl">
                  {user.acceptance_rate?.toFixed(1) || 0}%
                </span>
              </div>
            </div>
          </div>

          {/* Streak Info */}
          <div className="bg-gray-800 rounded-lg border border-gray-700 p-6">
            <h2 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
              <FiZap className="text-yellow-500" />
              Streak
            </h2>

            <div className="space-y-6">
              <div>
                <div className="text-5xl font-bold text-center mb-2">
                  <span className="text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 to-orange-500">
                    {user.current_streak}
                  </span>
                </div>
                <div className="text-center text-gray-400">Current Streak (days)</div>
              </div>

              <div className="flex items-center justify-around pt-6 border-t border-gray-700">
                <div className="text-center">
                  <div className="text-2xl font-bold text-white">{user.longest_streak}</div>
                  <div className="text-sm text-gray-400">Longest Streak</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-white">{user.contests_participated || 0}</div>
                  <div className="text-sm text-gray-400">Contests</div>
                </div>
              </div>

              {user.is_on_streak ? (
                <div className="bg-green-900/20 border border-green-700 rounded-lg p-4 text-center">
                  <span className="text-green-400 text-sm">
                    🔥 You're on a streak! Keep it going!
                  </span>
                </div>
              ) : (
                <div className="bg-gray-900 rounded-lg p-4 text-center">
                  <span className="text-gray-400 text-sm">
                    Solve a problem today to start your streak!
                  </span>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ProfilePage