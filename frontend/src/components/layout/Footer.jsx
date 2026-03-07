import { FiGithub, FiTwitter, FiLinkedin } from 'react-icons/fi'

const Footer = () => {
  return (
    <footer className="bg-gray-900 border-t border-gray-800 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* About */}
          <div>
            <h3 className="text-white font-semibold mb-4">CodeForge</h3>
            <p className="text-gray-400 text-sm">
              Master coding skills through practice. Compete in contests, join groups, and climb the leaderboard.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-white font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li><a href="/problems" className="text-gray-400 hover:text-white text-sm transition">Problems</a></li>
              <li><a href="/contests" className="text-gray-400 hover:text-white text-sm transition">Contests</a></li>
              <li><a href="/groups" className="text-gray-400 hover:text-white text-sm transition">Groups</a></li>
              <li><a href="/leaderboard" className="text-gray-400 hover:text-white text-sm transition">Leaderboard</a></li>
            </ul>
          </div>

          {/* Support */}
          <div>
            <h3 className="text-white font-semibold mb-4">Support</h3>
            <ul className="space-y-2">
              <li><a href="#" className="text-gray-400 hover:text-white text-sm transition">Help Center</a></li>
              <li><a href="#" className="text-gray-400 hover:text-white text-sm transition">Contact Us</a></li>
              <li><a href="#" className="text-gray-400 hover:text-white text-sm transition">FAQ</a></li>
              <li><a href="#" className="text-gray-400 hover:text-white text-sm transition">Report Bug</a></li>
            </ul>
          </div>

          {/* Social */}
          <div>
            <h3 className="text-white font-semibold mb-4">Connect</h3>
            <div className="flex space-x-4">
              <a href="#" className="text-gray-400 hover:text-white transition">
                <FiGithub className="text-2xl" />
              </a>
              <a href="#" className="text-gray-400 hover:text-white transition">
                <FiTwitter className="text-2xl" />
              </a>
              <a href="#" className="text-gray-400 hover:text-white transition">
                <FiLinkedin className="text-2xl" />
              </a>
            </div>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-gray-800 text-center">
          <p className="text-gray-400 text-sm">
            © 2026 CodeForge. Built with ❤️ for coders.
          </p>
        </div>
      </div>
    </footer>
  )
}

export default Footer