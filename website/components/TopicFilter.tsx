interface Topic {
  name: string
  email_count: number
  emails: Array<{
    id: string
    subject: string
    date: string
    snippet: string
  }>
}

interface TopicFilterProps {
  topics: Record<string, Topic>
  selectedTopic: string | null
  onSelectTopic: (topicId: string | null) => void
}

export default function TopicFilter({ topics, selectedTopic, onSelectTopic }: TopicFilterProps) {
  const topicEntries = Object.entries(topics)

  if (topicEntries.length === 0) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg p-6">
        <h2 className="text-xl font-bold mb-4">Topics</h2>
        <p className="text-gray-500 text-sm">No topics generated yet</p>
      </div>
    )
  }

  return (
    <div className="bg-white/60 dark:bg-slate-800/40 backdrop-blur-sm rounded-2xl p-6 sticky top-8 border border-slate-200/50 dark:border-slate-700/50">
      <h2 className="text-xl font-bold mb-6 text-slate-900 dark:text-white">Topics</h2>

      <button
        onClick={() => onSelectTopic(null)}
        className={`w-full text-left px-5 py-3 rounded-xl mb-3 transition-all font-medium ${
          selectedTopic === null
            ? 'bg-gradient-to-r from-blue-600 to-cyan-600 text-white shadow-lg'
            : 'hover:bg-slate-100 dark:hover:bg-slate-700/50 text-slate-700 dark:text-slate-300'
        }`}
      >
        All Emails
      </button>

      <div className="space-y-2">
        {topicEntries.map(([topicId, topic]) => (
          <button
            key={topicId}
            onClick={() => onSelectTopic(topicId)}
            className={`w-full text-left px-5 py-3 rounded-xl transition-all ${
              selectedTopic === topicId
                ? 'bg-gradient-to-r from-blue-600 to-cyan-600 text-white shadow-lg'
                : 'hover:bg-slate-100 dark:hover:bg-slate-700/50'
            }`}
          >
            <div className={`font-semibold ${selectedTopic === topicId ? 'text-white' : 'text-slate-900 dark:text-white'}`}>
              {topic.name}
            </div>
            <div className={`text-sm ${selectedTopic === topicId ? 'text-white/80' : 'text-slate-500 dark:text-slate-400'}`}>
              {topic.email_count} emails
            </div>
          </button>
        ))}
      </div>
    </div>
  )
}
