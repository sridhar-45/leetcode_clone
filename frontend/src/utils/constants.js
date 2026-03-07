export const DIFFICULTY_COLORS = {
  EASY: '#10b981',    // Green
  MEDIUM: '#f59e0b',  // Orange
  HARD: '#ef4444',    // Red
}

export const DIFFICULTY_BG = {
  EASY: 'rgba(16, 185, 129, 0.1)',
  MEDIUM: 'rgba(245, 158, 11, 0.1)',
  HARD: 'rgba(239, 68, 68, 0.1)',
}

export const STATUS_COLORS = {
  ACCEPTED: '#10b981',
  WRONG_ANSWER: '#ef4444',
  TIME_LIMIT_EXCEEDED: '#f59e0b',
  RUNTIME_ERROR: '#ef4444',
  COMPILE_ERROR: '#ef4444',
  PENDING: '#6b7280',
  RUNNING: '#3b82f6',
}

export const LANGUAGES = [
  { value: 'python', label: 'Python 3', extension: 'py' },
  { value: 'javascript', label: 'JavaScript', extension: 'js' },
  { value: 'java', label: 'Java', extension: 'java' },
]

export const DEFAULT_CODE_TEMPLATES = {
  python: `class Solution:
    def solve(self):
        # Write your code here
        pass`,
  javascript: `/**
 * @return {number}
 */
var solve = function() {
    // Write your code here
};`,
  java: `class Solution {
    public void solve() {
        // Write your code here
    }
}`,
}

export const MONACO_THEMES = {
  'vs-dark': 'Dark',
  'vs-light': 'Light',
  'hc-black': 'High Contrast',
}

export const FONT_SIZES = [10, 12, 14, 16, 18, 20, 22, 24]

