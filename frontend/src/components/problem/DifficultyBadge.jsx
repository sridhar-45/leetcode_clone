import { DIFFICULTY_COLORS, DIFFICULTY_BG } from '../../utils/constants'

const DifficultyBadge = ({ difficulty, showIcon = true }) => {
  const color = DIFFICULTY_COLORS[difficulty] || '#6b7280'
  const bgColor = DIFFICULTY_BG[difficulty] || 'rgba(107, 114, 128, 0.1)'

  return (
    <span
      className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
      style={{
        color: color,
        backgroundColor: bgColor,
      }}
    >
      {showIcon && <span className="mr-1">●</span>}
      {difficulty.charAt(0) + difficulty.slice(1).toLowerCase()}
    </span>
  )
}

export default DifficultyBadge