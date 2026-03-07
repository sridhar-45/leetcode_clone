const TestCasePanel = ({ testCases, activeTestCase, setActiveTestCase }) => {
  if (!testCases || testCases.length === 0) {
    return (
      <div className="p-4 text-gray-400 text-center">
        No test cases available
      </div>
    )
  }

  return (
    <div className="bg-gray-900 h-full flex flex-col">
      {/* Test Case Tabs */}
      <div className="flex gap-2 px-4 py-3 border-b border-gray-700 overflow-x-auto">
        {testCases.map((tc, index) => (
          <button
            key={index}
            onClick={() => setActiveTestCase(index)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition whitespace-nowrap ${
              activeTestCase === index
                ? 'bg-gray-700 text-white'
                : 'text-gray-400 hover:text-white hover:bg-gray-800'
            }`}
          >
            Case {index + 1}
          </button>
        ))}
      </div>

      {/* Test Case Content */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {testCases[activeTestCase] && (
          <>
            <div>
              <div className="text-sm font-medium text-gray-400 mb-2">Input</div>
              <div className="bg-gray-800 rounded p-3 font-mono text-sm text-white">
                {testCases[activeTestCase].input_data}
              </div>
            </div>

            <div>
              <div className="text-sm font-medium text-gray-400 mb-2">Expected Output</div>
              <div className="bg-gray-800 rounded p-3 font-mono text-sm text-white">
                {testCases[activeTestCase].expected_output}
              </div>
            </div>

            {testCases[activeTestCase].explanation && (
              <div>
                <div className="text-sm font-medium text-gray-400 mb-2">Explanation</div>
                <div className="text-gray-300 text-sm">
                  {testCases[activeTestCase].explanation}
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  )
}

export default TestCasePanel