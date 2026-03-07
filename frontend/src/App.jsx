import { Routes, Route } from 'react-router-dom'
import Navbar from './components/layout/Navbar'
import Footer from './components/layout/Footer'
import ProtectedRoute from './components/common/ProtectedRoute'

// Pages
import HomePage from './pages/HomePage'
import LoginPage from './pages/auth/LoginPage'
import RegisterPage from './pages/auth/RegisterPage'
import ProblemsPage from './pages/ProblemsPage'
import ProblemDetailPage from './pages/ProblemDetailPage'
import ContestsPage from './pages/contests/ContestsPage'
import ContestDetailPage from './pages/contests/ContestDetailPage'
import CreateContestPage from './pages/contests/CreateContestPage'
import GroupsPage from './pages/groups/GroupsPage'
import GroupDetailPage from './pages/groups/GroupDetailPage'
import CreateGroupPage from './pages/groups/CreateGroupPage'
import ProfilePage from './pages/profile/ProfilePage'
import SubmissionsPage from './pages/profile/SubmissionsPage'
import LeaderboardPage from './pages/LeaderboardPage'
import NotFoundPage from './pages/NotFoundPage'

function App() {
  return (
    <div className="app">
      <Navbar />
      
      <main className="main-content">
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/problems" element={<ProblemsPage />} />
          <Route path="/problems/:slug" element={<ProblemDetailPage />} />
          <Route path="/contests" element={<ContestsPage />} />
          <Route path="/contests/:slug" element={<ContestDetailPage />} />
          <Route path="/groups" element={<GroupsPage />} />
          <Route path="/groups/:slug" element={<GroupDetailPage />} />
          <Route path="/leaderboard" element={<LeaderboardPage />} />
          
          {/* Protected Routes (require login) */}
          <Route path="/profile" element={
            <ProtectedRoute>
              <ProfilePage />
            </ProtectedRoute>
          } />
          <Route path="/submissions" element={
            <ProtectedRoute>
              <SubmissionsPage />
            </ProtectedRoute>
          } />
          <Route path="/contests/create" element={
            <ProtectedRoute>
              <CreateContestPage />
            </ProtectedRoute>
          } />
          <Route path="/groups/create" element={
            <ProtectedRoute>
              <CreateGroupPage />
            </ProtectedRoute>
          } />
          
          {/* 404 Page */}
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </main>
      
      <Footer />
    </div>
  )
}

export default App