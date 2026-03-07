// Save to localStorage
export const saveToStorage = (key, value) => {
  try {
    const serialized = JSON.stringify(value)
    localStorage.setItem(key, serialized)
  } catch (error) {
    console.error('Error saving to localStorage:', error)
  }
}

// Get from localStorage
export const getFromStorage = (key, defaultValue = null) => {
  try {
    const item = localStorage.getItem(key)
    return item ? JSON.parse(item) : defaultValue
  } catch (error) {
    console.error('Error reading from localStorage:', error)
    return defaultValue
  }
}

// Remove from localStorage
export const removeFromStorage = (key) => {
  try {
    localStorage.removeItem(key)
  } catch (error) {
    console.error('Error removing from localStorage:', error)
  }
}

// Clear all localStorage
export const clearStorage = () => {
  try {
    localStorage.clear()
  } catch (error) {
    console.error('Error clearing localStorage:', error)
  }
}

// Save editor preferences
export const saveEditorPrefs = (prefs) => {
  saveToStorage('editorPrefs', prefs)
}

// Get editor preferences
export const getEditorPrefs = () => {
  return getFromStorage('editorPrefs', {
    fontSize: 14,
    theme: 'vs-dark',
    language: 'python',
  })
}