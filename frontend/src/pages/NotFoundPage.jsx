// """
// ═══════════════════════════════════════════════════════════════
// FILE 34: pages/NotFoundPage.jsx
// Location: frontend/src/pages/NotFoundPage.jsx
// 404 PAGE - Page not found
// ═══════════════════════════════════════════════════════════════
// """

import { Link } from 'react-router-dom'
import { FiHome } from 'react-icons/fi'

const NotFoundPage = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900 px-4">
      <div className="text-center">
        <div className="mb-8">
          <h1 className="text-9xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-purple-500">
            404
          </h1>
        </div>
        
        <h2 className="text-3xl font-bold text-white mb-4">
          Page Not Found
        </h2>
        
        <p className="text-gray-400 mb-8 max-w-md mx-auto">
          The page you're looking for doesn't exist or has been moved.
        </p>

        <Link
          to="/"
          className="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition"
        >
          <FiHome />
          Back to Home
        </Link>
      </div>
    </div>
  )
}

export default NotFoundPage

