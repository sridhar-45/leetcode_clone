import { createContext, useState, useContext, useEffect } from 'react'
import { authAPI } from '../services/authAPI'
import { useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'

const AuthContext = createContext()

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  // Check if user is logged in on mount
  useEffect(() => {
    const initAuth = async () => {
      const token = localStorage.getItem('access_token')
      const savedUser = localStorage.getItem('user')

      if (token && savedUser) {
        try {
          setUser(JSON.parse(savedUser))
          setIsAuthenticated(true)
          
          // Fetch fresh profile data
          const profile = await authAPI.getProfile()
          setUser(profile)
          localStorage.setItem('user', JSON.stringify(profile))
        } catch (error) {
          console.error('Auth init failed:', error)
          logout()
        }
      }
      
      setLoading(false)
    }

    initAuth()
  }, [])

  // Login function
  const login = async (credentials) => {
    try {
      const data = await authAPI.login(credentials)
      
      // Save tokens and user
      localStorage.setItem('access_token', data.tokens.access)
      localStorage.setItem('refresh_token', data.tokens.refresh)
      localStorage.setItem('user', JSON.stringify(data.user))
      
      setUser(data.user)
      setIsAuthenticated(true)
      
      toast.success('Welcome back! 👋')
      navigate('/problems')
      
      return { success: true }
    } catch (error) {
      const message = error.response?.data?.error || 'Login failed'
      toast.error(message)
      return { success: false, error: message }
    }
  }

  // Register function
  const register = async (userData) => {
    try {
      const data = await authAPI.register(userData)
      
      // Save tokens and user
      localStorage.setItem('access_token', data.tokens.access)
      localStorage.setItem('refresh_token', data.tokens.refresh)
      localStorage.setItem('user', JSON.stringify(data.user))
      
      setUser(data.user)
      setIsAuthenticated(true)
      
      toast.success('Account created successfully! 🎉')
      navigate('/problems')
      
      return { success: true }
    } catch (error) {
      const message = error.response?.data?.error || 'Registration failed'
      toast.error(message)
      return { success: false, error: message }
    }
  }

  // Logout function
  const logout = async () => {
    try {
      const refreshToken = localStorage.getItem('refresh_token')
      if (refreshToken) {
        await authAPI.logout(refreshToken)
      }
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      // Clear local data
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
      
      setUser(null)
      setIsAuthenticated(false)
      
      toast.success('Logged out successfully')
      navigate('/login')
    }
  }

  // Update user data
  const updateUser = (userData) => {
    setUser(userData)
    localStorage.setItem('user', JSON.stringify(userData))
  }

  const value = {
    user,
    isAuthenticated,
    loading,
    login,
    register,
    logout,
    updateUser,
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}
