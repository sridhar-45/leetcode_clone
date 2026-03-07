import { useState } from 'react'
import Editor from '@monaco-editor/react'
import { LANGUAGES, MONACO_THEMES, FONT_SIZES } from '../../utils/constants'
import { FiPlay, FiSend, FiSettings, FiRotateCcw } from 'react-icons/fi'
import Button from '../common/Button'

const CodeEditor = ({
  code,
  onChange,
  language,
  onLanguageChange,
  onRun,
  onSubmit,
  loading,
  problemTemplate,
}) => {
  const [fontSize, setFontSize] = useState(14)
  const [theme, setTheme] = useState('vs-dark')
  const [showSettings, setShowSettings] = useState(false)

  const handleEditorChange = (value) => {
    onChange(value || '')
  }

  const handleReset = () => {
    if (window.confirm('Are you sure you want to reset your code?')) {
      onChange(problemTemplate || '')
    }
  }

  return (
    <div className="flex flex-col h-full bg-gray-900">
      {/* Editor Header */}
      <div className="flex items-center justify-between px-4 py-3 bg-gray-800 border-b border-gray-700">
        <div className="flex items-center gap-3">
          {/* Language Selector */}
          <select
            value={language}
            onChange={(e) => onLanguageChange(e.target.value)}
            className="px-3 py-1.5 bg-gray-900 border border-gray-700 rounded text-white text-sm focus:outline-none focus:border-blue-500"
          >
            {LANGUAGES.map((lang) => (
              <option key={lang.value} value={lang.value}>
                {lang.label}
              </option>
            ))}
          </select>

          {/* Font Size */}
          <select
            value={fontSize}
            onChange={(e) => setFontSize(Number(e.target.value))}
            className="px-3 py-1.5 bg-gray-900 border border-gray-700 rounded text-white text-sm focus:outline-none focus:border-blue-500"
          >
            {FONT_SIZES.map((size) => (
              <option key={size} value={size}>
                {size}px
              </option>
            ))}
          </select>

          {/* Theme Selector */}
          <div className="relative">
            <button
              onClick={() => setShowSettings(!showSettings)}
              className="px-3 py-1.5 bg-gray-900 border border-gray-700 rounded text-white text-sm hover:bg-gray-800 transition flex items-center gap-2"
            >
              <FiSettings />
              Theme
            </button>

            {showSettings && (
              <>
                <div
                  className="fixed inset-0 z-10"
                  onClick={() => setShowSettings(false)}
                ></div>
                <div className="absolute top-full left-0 mt-1 bg-gray-800 border border-gray-700 rounded-lg shadow-lg z-20 min-w-[150px]">
                  {Object.entries(MONACO_THEMES).map(([value, label]) => (
                    <button
                      key={value}
                      onClick={() => {
                        setTheme(value)
                        setShowSettings(false)
                      }}
                      className={`w-full text-left px-4 py-2 text-sm hover:bg-gray-700 transition ${
                        theme === value ? 'text-blue-400' : 'text-white'
                      }`}
                    >
                      {label}
                    </button>
                  ))}
                </div>
              </>
            )}
          </div>

          {/* Reset Button */}
          <button
            onClick={handleReset}
            className="px-3 py-1.5 bg-gray-900 border border-gray-700 rounded text-white text-sm hover:bg-gray-800 transition flex items-center gap-2"
            title="Reset to template"
          >
            <FiRotateCcw />
            Reset
          </button>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center gap-2">
          <Button
            onClick={onRun}
            variant="secondary"
            size="small"
            loading={loading}
            className="flex items-center gap-2"
          >
            <FiPlay />
            Run Code
          </Button>

          <Button
            onClick={onSubmit}
            variant="success"
            size="small"
            loading={loading}
            className="flex items-center gap-2"
          >
            <FiSend />
            Submit
          </Button>
        </div>
      </div>

      {/* Monaco Editor */}
      <div className="flex-1 overflow-hidden">
        <Editor
          height="100%"
          language={language}
          value={code}
          onChange={handleEditorChange}
          theme={theme}
          options={{
            fontSize: fontSize,
            minimap: { enabled: fontSize > 16 },
            scrollBeyondLastLine: false,
            wordWrap: 'on',
            automaticLayout: true,
            tabSize: 4,
            insertSpaces: true,
            formatOnPaste: true,
            formatOnType: true,
            suggestOnTriggerCharacters: true,
            quickSuggestions: true,
            lineNumbers: 'on',
            renderWhitespace: 'selection',
            bracketPairColorization: {
              enabled: true,
            },
          }}
        />
      </div>

      {/* Keyboard Shortcuts Hint */}
      <div className="px-4 py-2 bg-gray-800 border-t border-gray-700 text-xs text-gray-400 flex items-center justify-between">
        <div className="flex gap-4">
          <span>
            <kbd className="px-2 py-1 bg-gray-900 rounded">Ctrl</kbd> +{' '}
            <kbd className="px-2 py-1 bg-gray-900 rounded">Enter</kbd> to Submit
          </span>
          <span>
            <kbd className="px-2 py-1 bg-gray-900 rounded">Ctrl</kbd> +{' '}
            <kbd className="px-2 py-1 bg-gray-900 rounded">R</kbd> to Run
          </span>
        </div>
        <span>Font: {fontSize}px | Theme: {MONACO_THEMES[theme]}</span>
      </div>
    </div>
  )
}

export default CodeEditor
