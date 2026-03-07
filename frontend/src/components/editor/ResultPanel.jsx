import { FiCheck, FiX, FiClock, FiDatabase } from 'react-icons/fi'
import { STATUS_COLORS } from '../../utils/constants'
import { formatRuntime, formatMemory, safeJSONParse } from '../../utils/helpers'

const ResultPanel = ({ result }) => {
  if (!result) {
    return (
      <div className="flex items-center justify-center h-full text-gray-400">
        <p>Run your code to see results here</p>
      </div>
    )
  }

  const isAccepted = result.status === 'ACCEPTED'
  const statusColor = STATUS_COLORS[result.status] || '#6b7280'
  const testResults = safeJSONParse(result.test_results, [])

  return (
    <div className="bg-gray-900 h-full flex flex-col overflow-hidden">
      {/* Status Header */}
      <div className={`px-6 py-4 border-b border-gray-700`}>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            {isAccepted ? (
              <FiCheck className="text-3xl text-green-500" />
            ) : (
              <FiX className="text-3xl text-red-500" />
            )}
            <div>
              <h3
                className="text-xl font-bold"
                style={{ color: statusColor }}
              >
                {result.status.replace(/_/g, ' ')}
              </h3>
              <p className="text-sm text-gray-400">
                {result.test_cases_passed || 0} / {result.test_cases_total || 0} test cases passed
              </p>
            </div>
          </div>

          {isAccepted && result.points_earned > 0 && (
            <div className="text-right">
              <div className="text-2xl font-bold text-yellow-500">
                +{result.points_earned}
              </div>
              <div className="text-xs text-gray-400">Points Earned</div>
            </div>
          )}
        </div>
      </div>

      {/* Runtime & Memory */}
      {(result.runtime || result.memory) && (
        <div className="grid grid-cols-2 gap-4 px-6 py-4 border-b border-gray-700">
          {result.runtime !== null && (
            <div className="flex items-center gap-2">
              <FiClock className="text-gray-400" />
              <div>
                <div className="text-sm text-gray-400">Runtime</div>
                <div className="text-white font-medium">
                  {formatRuntime(result.runtime)}
                </div>
              </div>
            </div>
          )}

          {result.memory !== null && (
            <div className="flex items-center gap-2">
              <FiDatabase className="text-gray-400" />
              <div>
                <div className="text-sm text-gray-400">Memory</div>
                <div className="text-white font-medium">
                  {formatMemory(result.memory)}
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Error Message */}
      {result.error_message && (
        <div className="px-6 py-4 border-b border-gray-700">
          <div className="text-sm text-gray-400 mb-2">Error</div>
          <div className="bg-red-900/20 border border-red-900 rounded p-3 text-red-400 text-sm font-mono">
            {result.error_message}
          </div>
        </div>
      )}

      {/* Test Results */}
      {testResults.length > 0 && (
        <div className="flex-1 overflow-y-auto px-6 py-4">
          <div className="text-sm text-gray-400 mb-3">Test Results</div>
          <div className="space-y-3">
            {testResults.map((test, index) => (
              <div
                key={index}
                className={`rounded-lg border p-3 ${
                  test.passed
                    ? 'bg-green-900/10 border-green-900'
                    : 'bg-red-900/10 border-red-900'
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    {test.passed ? (
                      <FiCheck className="text-green-500" />
                    ) : (
                      <FiX className="text-red-500" />
                    )}
                    <span className="font-medium text-white">
                      Test Case {test.test_num || index + 1}
                    </span>
                  </div>
                  {test.runtime_ms && (
                    <span className="text-xs text-gray-400">
                      {test.runtime_ms}ms
                    </span>
                  )}
                </div>

                <div className="space-y-2 text-sm">
                  <div>
                    <span className="text-gray-400">Input: </span>
                    <code className="text-gray-300">{test.input}</code>
                  </div>
                  <div>
                    <span className="text-gray-400">Expected: </span>
                    <code className="text-gray-300">{test.expected}</code>
                  </div>
                  {!test.passed && test.actual && (
                    <div>
                      <span className="text-gray-400">Your Output: </span>
                      <code className="text-red-400">{test.actual}</code>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default ResultPanel