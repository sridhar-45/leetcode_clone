// """
// ═══════════════════════════════════════════════════════════════
// FILE 33: pages/ProblemDetailPage.jsx
// Location: frontend/src/pages/ProblemDetailPage.jsx
// PROBLEM DETAIL PAGE - Split view with description and code editor
// This is THE MOST IMPORTANT page!
// ═══════════════════════════════════════════════════════════════
// """

import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { problemsAPI } from '../services/problemsAPI'
import { submissionsAPI } from '../services/submissionsAPI'
import { useAuth } from '../context/AuthContext'
import CodeEditor from '../components/editor/CodeEditor'
import TestCasePanel from '../components/editor/TestCasePanel'
import ResultPanel from '../components/editor/ResultPanel'
import DifficultyBadge from '../components/problem/DifficultyBadge'
import TopicTag from '../components/problem/TopicTag'
import LoadingSpinner from '../components/common/LoadingSpinner'
import toast from 'react-hot-toast'
import { FiArrowLeft, FiBookOpen, FiCode } from 'react-icons/fi'

const ProblemDetailPage = () => {
  const { slug } = useParams()
  const navigate = useNavigate()
  const { isAuthenticated, user, updateUser } = useAuth()

  // Problem data
  const [problem, setProblem] = useState(null)
  const [loading, setLoading] = useState(true)

  // Editor state
  const [code, setCode] = useState('')
  const [language, setLanguage] = useState('python')
  const [activeTab, setActiveTab] = useState('description')
  const [activeTestCase, setActiveTestCase] = useState(0)

  // Submission state
  const [submitting, setSubmitting] = useState(false)
  const [result, setResult] = useState(null)
  const [showResult, setShowResult] = useState(false)

  useEffect(() => {
    fetchProblem()
  }, [slug])

  useEffect(() => {
    // Update code when language changes
    if (problem) {
      const templates = {
        python: problem.template_python,
        javascript: problem.template_javascript,
        java: problem.template_java,
      }
      setCode(templates[language] || problem.template_python || '')
    }
  }, [language, problem])

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyPress = (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault()
        handleSubmit()
      } else if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
        e.preventDefault()
        handleRun()
      }
    }

    window.addEventListener('keydown', handleKeyPress)
    return () => window.removeEventListener('keydown', handleKeyPress)
  }, [code, language])

  const fetchProblem = async () => {
    try {
      setLoading(true)
      const data = await problemsAPI.getProblemDetail(slug)
      setProblem(data)
      setCode(data.template_python || '')
    } catch (error) {
      console.error('Error fetching problem:', error)
      toast.error('Failed to load problem')
    } finally {
      setLoading(false)
    }
  }

  const handleRun = async () => {
    if (!isAuthenticated) {
      toast.error('Please login to run code')
      return
    }

    try {
      setSubmitting(true)
      setShowResult(false)

      const data = await submissionsAPI.runCode(slug, code, language)
      setResult(data)
      setShowResult(true)

      toast.success('Code executed successfully')
    } catch (error) {
      console.error('Error running code:', error)
      toast.error('Failed to run code')
    } finally {
      setSubmitting(false)
    }
  }

  const handleSubmit = async () => {
    if (!isAuthenticated) {
      toast.error('Please login to submit code')
      navigate('/login')
      return
    }

    try {
      setSubmitting(true)
      setShowResult(false)

      const data = await submissionsAPI.submitCode(slug, code, language)
      setResult(data)
      setShowResult(true)

      if (data.status === 'ACCEPTED') {
        toast.success(`Accepted! +${data.points_earned} points 🎉`, {
          duration: 5000,
        })

        // Update user stats in context
        if (user) {
          const updatedUser = {
            ...user,
            problems_solved: user.problems_solved + (data.is_first_accepted ? 1 : 0),
            total_points: user.total_points + data.points_earned,
          }
          updateUser(updatedUser)
        }
      } else {
        toast.error(`${data.status.replace(/_/g, ' ')}`)
      }
    } catch (error) {
      console.error('Error submitting code:', error)
      toast.error('Failed to submit code')
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) {
    return <LoadingSpinner text="Loading problem..." />
  }

  if (!problem) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <h2 className="text-2xl text-white mb-4">Problem not found</h2>
          <button
            onClick={() => navigate('/problems')}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg"
          >
            Back to Problems
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="h-screen flex flex-col bg-gray-900">
      {/* Header */}
      <div className="flex items-center justify-between px-6 py-3 bg-gray-800 border-b border-gray-700">
        <div className="flex items-center gap-4">
          <button
            onClick={() => navigate('/problems')}
            className="text-gray-400 hover:text-white transition"
          >
            <FiArrowLeft className="text-xl" />
          </button>

          <div className="flex items-center gap-3">
            <h1 className="text-xl font-bold text-white">
              {problem.id}. {problem.title}
            </h1>
            <DifficultyBadge difficulty={problem.difficulty} />
          </div>
        </div>

        <div className="flex items-center gap-2">
          {problem.topics?.slice(0, 3).map((topic) => (
            <TopicTag key={topic.slug} topic={topic.name} />
          ))}
        </div>
      </div>

      {/* Main Content - Split View */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Panel - Problem Description */}
        <div className="w-1/2 flex flex-col border-r border-gray-700">
          {/* Tabs */}
          <div className="flex gap-2 px-4 py-3 bg-gray-800 border-b border-gray-700">
            <button
              onClick={() => setActiveTab('description')}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition ${
                activeTab === 'description'
                  ? 'bg-gray-700 text-white'
                  : 'text-gray-400 hover:text-white hover:bg-gray-700'
              }`}
            >
              <FiBookOpen />
              Description
            </button>
            <button
              onClick={() => setActiveTab('testcases')}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition ${
                activeTab === 'testcases'
                  ? 'bg-gray-700 text-white'
                  : 'text-gray-400 hover:text-white hover:bg-gray-700'
              }`}
            >
              <FiCode />
              Test Cases
            </button>
          </div>

          {/* Content */}
          <div className="flex-1 overflow-y-auto">
            {activeTab === 'description' ? (
              <div className="p-6 prose prose-invert max-w-none">
                {/* Description */}
                <div className="mb-6">
                  <div
                    className="text-gray-300 whitespace-pre-wrap"
                    dangerouslySetInnerHTML={{ __html: problem.description.replace(/\n/g, '<br />') }}
                  />
                </div>

                {/* Examples */}
                {problem.examples && (
                  <div className="mb-6">
                    <h3 className="text-lg font-semibold text-white mb-3">Examples</h3>
                    <div
                      className="text-gray-300 whitespace-pre-wrap bg-gray-800 rounded-lg p-4 font-mono text-sm"
                      dangerouslySetInnerHTML={{ __html: problem.examples.replace(/\n/g, '<br />') }}
                    />
                  </div>
                )}

                {/* Constraints */}
                {problem.constraints && (
                  <div className="mb-6">
                    <h3 className="text-lg font-semibold text-white mb-3">Constraints</h3>
                    <div
                      className="text-gray-300 whitespace-pre-wrap bg-gray-800 rounded-lg p-4 font-mono text-sm"
                      dangerouslySetInnerHTML={{ __html: problem.constraints.replace(/\n/g, '<br />') }}
                    />
                  </div>
                )}

                {/* Stats */}
                <div className="grid grid-cols-2 gap-4 mt-6">
                  <div className="bg-gray-800 rounded-lg p-4">
                    <div className="text-sm text-gray-400">Acceptance Rate</div>
                    <div className="text-2xl font-bold text-green-500">
                      {problem.acceptance_rate.toFixed(1)}%
                    </div>
                  </div>
                  <div className="bg-gray-800 rounded-lg p-4">
                    <div className="text-sm text-gray-400">Total Submissions</div>
                    <div className="text-2xl font-bold text-blue-500">
                      {problem.total_submissions}
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <TestCasePanel
                testCases={problem.test_cases}
                activeTestCase={activeTestCase}
                setActiveTestCase={setActiveTestCase}
              />
            )}
          </div>
        </div>

        {/* Right Panel - Code Editor */}
        <div className="w-1/2 flex flex-col">
          {/* Code Editor */}
          <div className={showResult ? 'h-1/2 border-b border-gray-700' : 'h-full'}>
            <CodeEditor
              code={code}
              onChange={setCode}
              language={language}
              onLanguageChange={setLanguage}
              onRun={handleRun}
              onSubmit={handleSubmit}
              loading={submitting}
              problemTemplate={problem[`template_${language}`]}
            />
          </div>

          {/* Results Panel */}
          {showResult && (
            <div className="h-1/2">
              <ResultPanel result={result} />
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default ProblemDetailPage