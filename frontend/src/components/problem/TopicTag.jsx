const TopicTag = ({ topic, onClick }) => {
  return (
    <span
      onClick={onClick}
      className={`
        inline-flex items-center px-2.5 py-0.5 rounded text-xs font-medium
        bg-gray-700 text-gray-300 border border-gray-600
        ${onClick ? 'cursor-pointer hover:bg-gray-600 transition' : ''}
      `}
    >
      {topic}
    </span>
  )
}

export default TopicTag