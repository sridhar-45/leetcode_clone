import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { FiCode, FiUsers, FiTrendingUp, FiZap, FiAward } from "react-icons/fi";
  import { FaTrophy } from "react-icons/fa";
const HomePage = () => {
  const { isAuthenticated } = useAuth()

  const features = [
    {
      icon: FiCode,
      title: '500+ Problems',
      description: 'Practice with curated coding problems from easy to hard',
      color: 'from-blue-500 to-cyan-500',
    },
    {
      icon: FaTrophy,
      title: 'Weekly Contests',
      description: 'Compete with others and climb the leaderboard',
      color: 'from-purple-500 to-pink-500',
    },
    {
      icon: FiUsers,
      title: 'Group Battles',
      description: 'Form teams and compete together',
      color: 'from-green-500 to-emerald-500',
    },
    {
      icon: FiTrendingUp,
      title: 'Track Progress',
      description: 'Monitor your improvement with detailed statistics',
      color: 'from-orange-500 to-red-500',
    },
    {
      icon: FiZap,
      title: 'Real-time Execution',
      description: 'Run and test your code instantly',
      color: 'from-yellow-500 to-orange-500',
    },
    {
      icon: FiAward,
      title: 'Daily Streaks',
      description: 'Build consistency with daily challenges',
      color: 'from-indigo-500 to-purple-500',
    },
  ]

  const stats = [
    { value: '10K+', label: 'Active Users' },
    { value: '500+', label: 'Problems' },
    { value: '100+', label: 'Contests' },
    { value: '50K+', label: 'Submissions' },
  ]

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 py-20 px-4">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-purple-500 transform rotate-45 scale-150"></div>
        </div>
        
        <div className="max-w-6xl mx-auto text-center relative z-10">
          <h1 className="text-5xl md:text-7xl font-bold text-white mb-6">
            Master Coding
            <span className="block bg-gradient-to-r from-blue-500 to-purple-500 text-transparent bg-clip-text">
              One Problem at a Time
            </span>
          </h1>
          
          <p className="text-xl md:text-2xl text-gray-300 mb-12 max-w-3xl mx-auto">
            Join thousands of developers improving their skills through practice,
            contests, and community challenges
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            {isAuthenticated ? (
              <Link
                to="/problems"
                className="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white rounded-lg text-lg font-semibold transition-all transform hover:scale-105 shadow-lg"
              >
                Start Solving
              </Link>
            ) : (
              <>
                <Link
                  to="/register"
                  className="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white rounded-lg text-lg font-semibold transition-all transform hover:scale-105 shadow-lg"
                >
                  Get Started Free
                </Link>
                <Link
                  to="/problems"
                  className="px-8 py-4 bg-gray-800 hover:bg-gray-700 text-white rounded-lg text-lg font-semibold transition-all border-2 border-gray-700"
                >
                  Browse Problems
                </Link>
              </>
            )}
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mt-16">
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <div className="text-3xl md:text-4xl font-bold text-white mb-2">
                  {stat.value}
                </div>
                <div className="text-gray-400">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 bg-gray-900">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-white mb-4">
              Everything You Need to Succeed
            </h2>
            <p className="text-xl text-gray-400">
              Comprehensive platform for coding interview preparation
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon
              return (
                <div
                  key={index}
                  className="bg-gray-800 rounded-xl p-6 border border-gray-700 hover:border-gray-600 transition-all hover:transform hover:scale-105"
                >
                  <div className={`w-12 h-12 rounded-lg bg-gradient-to-r ${feature.color} flex items-center justify-center mb-4`}>
                    <Icon className="text-white text-2xl" />
                  </div>
                  <h3 className="text-xl font-semibold text-white mb-2">
                    {feature.title}
                  </h3>
                  <p className="text-gray-400">
                    {feature.description}
                  </p>
                </div>
              )
            })}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 bg-gradient-to-r from-blue-600 to-purple-600">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-white mb-6">
            Ready to Level Up Your Skills?
          </h2>
          <p className="text-xl text-blue-100 mb-8">
            Join our community and start your coding journey today
          </p>
          {!isAuthenticated && (
            <Link
              to="/register"
              className="inline-block px-8 py-4 bg-white text-blue-600 rounded-lg text-lg font-semibold hover:bg-gray-100 transition-all transform hover:scale-105 shadow-lg"
            >
              Create Free Account
            </Link>
          )}
        </div>
      </section>
    </div>
  )
}

export default HomePage
