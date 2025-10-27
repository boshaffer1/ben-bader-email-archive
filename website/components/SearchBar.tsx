interface SearchBarProps {
  value: string
  onChange: (value: string) => void
  placeholder?: string
}

export default function SearchBar({ value, onChange, placeholder = 'Search...' }: SearchBarProps) {
  return (
    <div className="relative max-w-3xl mx-auto">
      <div className="relative">
        <svg className="absolute left-6 top-1/2 -translate-y-1/2 w-6 h-6 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <input
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder={placeholder}
          className="w-full pl-16 pr-16 py-5 text-lg rounded-2xl border-2 border-slate-200 dark:border-slate-700 bg-white/60 dark:bg-slate-800/40 backdrop-blur-sm focus:border-blue-500 dark:focus:border-blue-500 focus:outline-none transition-all shadow-lg focus:shadow-xl placeholder:text-slate-400"
        />
        {value && (
          <button
            onClick={() => onChange('')}
            className="absolute right-6 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 transition-colors p-1"
          >
            ✕
          </button>
        )}
      </div>
    </div>
  )
}
