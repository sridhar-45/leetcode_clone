import { format, formatDistanceToNow } from 'date-fns'

// Format date to readable string
export const formatDate = (dateString) => {
  if (!dateString) return 'Never'
  const date = new Date(dateString)
  return format(date, 'MMM dd, yyyy')
}

// Format date to relative time (2 hours ago)
export const formatRelativeTime = (dateString) => {
  if (!dateString) return 'Never'
  const date = new Date(dateString)
  return formatDistanceToNow(date, { addSuffix: true })
}

// Format runtime
export const formatRuntime = (ms) => {
  if (ms === null || ms === undefined) return 'N/A'
  return `${ms} ms`
}

// Format memory
export const formatMemory = (mb) => {
  if (mb === null || mb === undefined) return 'N/A'
  return `${mb.toFixed(1)} MB`
}

// Format percentage
export const formatPercentage = (value) => {
  if (value === null || value === undefined) return '0%'
  return `${value.toFixed(1)}%`
}

// Truncate text
export const truncate = (text, maxLength) => {
  if (!text) return ''
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}

// Get difficulty badge color
export const getDifficultyColor = (difficulty) => {
  const colors = {
    EASY: 'text-green-500',
    MEDIUM: 'text-yellow-500',
    HARD: 'text-red-500',
  }
  return colors[difficulty] || 'text-gray-500'
}

// Get status color
export const getStatusColor = (status) => {
  const colors = {
    ACCEPTED: 'text-green-500',
    WRONG_ANSWER: 'text-red-500',
    TIME_LIMIT_EXCEEDED: 'text-yellow-500',
    RUNTIME_ERROR: 'text-red-500',
    COMPILE_ERROR: 'text-red-500',
    PENDING: 'text-gray-500',
    RUNNING: 'text-blue-500',
  }
  return colors[status] || 'text-gray-500'
}

// Calculate time remaining
export const getTimeRemaining = (endTime) => {
  const now = new Date()
  const end = new Date(endTime)
  const diff = end - now

  if (diff <= 0) return 'Ended'

  const hours = Math.floor(diff / (1000 * 60 * 60))
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
  const seconds = Math.floor((diff % (1000 * 60)) / 1000)

  if (hours > 0) return `${hours}h ${minutes}m`
  if (minutes > 0) return `${minutes}m ${seconds}s`
  return `${seconds}s`
}

// Parse JSON safely
export const safeJSONParse = (jsonString, defaultValue = null) => {
  try {
    return JSON.parse(jsonString)
  } catch (error) {
    return defaultValue
  }
}

// Debounce function
export const debounce = (func, wait) => {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}
