import { Link, useLocation } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import { FiCode, FiUser, FiLogOut, FiTrophy, FiUsers } from 'react-icons/fi'
import { useState } from 'react'

const Navbar = () => {
  const { user, isAuthenticated, logout } = useAuth()
  const location = useLocation()
  const [showUserMenu, setShowUserMenu] = useState(false)

  const isActive = (path) => {
    return location.pathname === path || location.pathname.startsWith(path + '/')
  }

  const navLinks = [
    { path: '/problems', label: 'Problems', icon: FiCode },
    { path: '/contests', label: 'Contests', icon: FiTrophy },
    { path: '/groups', label: 'Groups', icon: FiUsers },
    { path: '/leaderboard', label: 'Leaderboard', icon: FiTrophy },
  ]

  return (
    <nav className="bg-gray-900 border-b border-gray-800 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <FiCode className="text-blue-500 text-2xl" />
            <span className="text-xl font-bold text-white">CodeForge</span>
          </Link>

          {/* Nav Links */}
          <div className="hidden md:flex items-center space-x-1">
            {navLinks.map((link) => {
              const Icon = link.icon
              return (
                <Link
                  key={link.path}
                  to={link.path}
                  className={`
                    flex items-center space-x-1 px-4 py-2 rounded-lg text-sm font-medium transition
                    ${isActive(link.path)
                      ? 'bg-gray-800 text-white'
                      : 'text-gray-300 hover:bg-gray-800 hover:text-white'
                    }
                  `}
                >
                  <Icon className="text-lg" />
                  <span>{link.label}</span>
                </Link>
              )
            })}
          </div>

          {/* User Menu */}
          <div className="flex items-center space-x-4">
            {isAuthenticated ? (
              <div className="relative">
                <button
                  onClick={() => setShowUserMenu(!showUserMenu)}
                  className="flex items-center space-x-2 px-3 py-2 rounded-lg hover:bg-gray-800 transition"
                >
                  <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center text-white font-semibold">
                    {user?.username?.charAt(0).toUpperCase()}
                  </div>
                  <span className="text-white font-medium hidden sm:block">{user?.username}</span>
                  <span className="text-gray-400 text-xs hidden sm:block">{user?.total_points} pts</span>
                </button>

                {/* Dropdown Menu */}
                {showUserMenu && (
                  <>
                    <div
                      className="fixed inset-0 z-10"
                      onClick={() => setShowUserMenu(false)}
                    ></div>
                    <div className="absolute right-0 mt-2 w-56 bg-gray-800 rounded-lg shadow-lg border border-gray-700 py-1 z-20">
                      <div className="px-4 py-3 border-b border-gray-700">
                        <p className="text-sm text-white font-semibold">{user?.username}</p>
                        <p className="text-xs text-gray-400">{user?.email}</p>
                        <div className="mt-2 flex items-center space-x-2 text-xs">
                          <span className="text-green-500">● {user?.current_streak} day streak</span>
                          <span className="text-gray-500">|</span>
                          <span className="text-blue-500">{user?.problems_solved} solved</span>
                        </div>
                      </div>

                      <Link
                        to="/profile"
                        onClick={() => setShowUserMenu(false)}
                        className="flex items-center space-x-2 px-4 py-2 text-gray-300 hover:bg-gray-700 transition"
                      >
                        <FiUser />
                        <span>My Profile</span>
                      </Link>

                      <Link
                        to="/submissions"
                        onClick={() => setShowUserMenu(false)}
                        className="flex items-center space-x-2 px-4 py-2 text-gray-300 hover:bg-gray-700 transition"
                      >
                        <FiCode />
                        <span>My Submissions</span>
                      </Link>

                      <button
                        onClick={() => {
                          setShowUserMenu(false)
                          logout()
                        }}
                        className="w-full flex items-center space-x-2 px-4 py-2 text-red-400 hover:bg-gray-700 transition"
                      >
                        <FiLogOut />
                        <span>Logout</span>
                      </button>
                    </div>
                  </>
                )}
              </div>
            ) : (
              <div className="flex items-center space-x-2">
                <Link
                  to="/login"
                  className="px-4 py-2 text-gray-300 hover:text-white transition"
                >
                  Sign In
                </Link>
                <Link
                  to="/register"
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition"
                >
                  Sign Up
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Mobile Nav */}
      <div className="md:hidden border-t border-gray-800">
        <div className="flex justify-around py-2">
          {navLinks.map((link) => {
            const Icon = link.icon
            return (
              <Link
                key={link.path}
                to={link.path}
                className={`
                  flex flex-col items-center px-3 py-1 text-xs
                  ${isActive(link.path) ? 'text-blue-500' : 'text-gray-400'}
                `}
              >
                <Icon className="text-xl mb-1" />
                <span>{link.label}</span>
              </Link>
            )
          })}
        </div>
      </div>
    </nav>
  )
}

export default Navbar
