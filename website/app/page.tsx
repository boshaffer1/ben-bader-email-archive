'use client'

import { useState, useEffect } from 'react'
import EmailList from '@/components/EmailList'
import TopicFilter from '@/components/TopicFilter'
import SearchBar from '@/components/SearchBar'
import NameInputModal from '@/components/NameInputModal'

interface Email {
  id: string
  subject: string
  from: string
  date: string
  snippet: string
  body: string
  timestamp?: string
}

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

export default function Home() {
  const [emails, setEmails] = useState<Email[]>([])
  const [topics, setTopics] = useState<Record<string, Topic>>({})
  const [selectedTopic, setSelectedTopic] = useState<string | null>(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [loading, setLoading] = useState(true)
  const [userName, setUserName] = useState('friend')
  const [sortOrder, setSortOrder] = useState<'newest' | 'oldest'>('newest')
  const [selectedYear, setSelectedYear] = useState<number | null>(null)
  const [favorites, setFavorites] = useState<Set<string>>(new Set())
  const [showFavoritesOnly, setShowFavoritesOnly] = useState(false)
  const [randomEmail, setRandomEmail] = useState<Email | null>(null)

  useEffect(() => {
    async function loadData() {
      try {
        const emailsRes = await fetch('/data/raw_emails.json')

        if (emailsRes.ok) {
          const emailData = await emailsRes.json()
          setEmails(emailData)
        }

        try {
          const topicsRes = await fetch('/data/topics.json')
          if (topicsRes.ok) {
            const topicData = await topicsRes.json()
            setTopics(topicData)
          }
        } catch {
          console.log('Topics not generated yet')
        }
      } catch (error) {
        console.error('Error loading data:', error)
      } finally {
        setLoading(false)
      }
    }

    loadData()
  }, [])

  // Load favorites from localStorage
  useEffect(() => {
    const savedFavorites = localStorage.getItem('emailFavorites')
    if (savedFavorites) {
      setFavorites(new Set(JSON.parse(savedFavorites)))
    }
  }, [])

  // Save favorites to localStorage
  useEffect(() => {
    localStorage.setItem('emailFavorites', JSON.stringify(Array.from(favorites)))
  }, [favorites])

  const toggleFavorite = (emailId: string) => {
    setFavorites(prev => {
      const newFavorites = new Set(prev)
      if (newFavorites.has(emailId)) {
        newFavorites.delete(emailId)
      } else {
        newFavorites.add(emailId)
      }
      return newFavorites
    })
  }

  const getRandomEmail = () => {
    if (filteredEmails.length > 0) {
      const randomIndex = Math.floor(Math.random() * filteredEmails.length)
      setRandomEmail(filteredEmails[randomIndex])
    }
  }

  const years = Array.from(new Set(emails.map(email => {
    const timestamp = parseInt(email.timestamp || '0')
    return new Date(timestamp).getFullYear()
  }))).sort((a, b) => b - a)

  const filteredEmails = emails
    .filter(email => {
      const matchesSearch = searchQuery === '' ||
        email.subject.toLowerCase().includes(searchQuery.toLowerCase()) ||
        email.body.toLowerCase().includes(searchQuery.toLowerCase())

      const matchesTopic = !selectedTopic ||
        topics[selectedTopic]?.emails.some(e => e.id === email.id)

      const matchesYear = !selectedYear ||
        new Date(parseInt(email.timestamp || '0')).getFullYear() === selectedYear

      const matchesFavorites = !showFavoritesOnly || favorites.has(email.id)

      return matchesSearch && matchesTopic && matchesYear && matchesFavorites
    })
    .sort((a, b) => {
      const timeA = parseInt(a.timestamp || '0')
      const timeB = parseInt(b.timestamp || '0')
      return sortOrder === 'newest' ? timeB - timeA : timeA - timeB
    })

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Loading emails...</div>
      </div>
    )
  }

  return (
    <main className="min-h-screen py-16 px-6 max-w-7xl mx-auto">
      <header className="mb-20 text-center">
        {/* Hero Section */}
        <div className="mb-12">
          <div className="relative inline-block mb-8">
            <div className="absolute inset-0 bg-gradient-to-br from-blue-500/20 to-cyan-500/20 rounded-full blur-2xl"></div>
            <img
              src="/ben-bader.jpg"
              alt="Ben Bader"
              className="relative w-56 h-56 rounded-full mx-auto object-cover shadow-2xl border-4 border-white/80 dark:border-white/10"
            />
          </div>

          <h1 className="text-6xl md:text-7xl font-bold mb-6 bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 dark:from-white dark:via-blue-200 dark:to-white bg-clip-text text-transparent leading-tight">
            Ben Bader<br/>Email Archive
          </h1>

          <p className="text-2xl text-slate-600 dark:text-slate-400 mb-4 font-light">
            {emails.length} emails • September 2021 – October 2025
          </p>
        </div>

        {/* Tribute Section */}
        <div className="max-w-4xl mx-auto space-y-8 mb-16">
          <div className="bg-white/60 dark:bg-slate-800/40 backdrop-blur-xl rounded-3xl p-12 shadow-2xl border border-slate-200/50 dark:border-slate-700/50">
            <div className="space-y-6 text-lg leading-relaxed">
              <p className="text-slate-700 dark:text-slate-300">
                If you knew Ben, you knew how amazing of a writer he was. He had a way with words that could inspire, motivate, and move you to action. He was a copywriter after all—one of the best.
              </p>

              <p className="text-slate-700 dark:text-slate-300">
                This archive was created to ensure Ben's legacy continues to inspire. His words deserve to be shared, remembered, and celebrated by all who knew him and those who wish they had.
              </p>

              <p className="text-slate-700 dark:text-slate-300">
                While we may have lost Ben, <span className="font-semibold text-blue-600 dark:text-blue-400">these emails will live on forever</span>.
              </p>

              <div className="pt-6 border-t border-slate-200 dark:border-slate-700">
                <p className="text-slate-600 dark:text-slate-400 text-base mb-4">
                  This archive contains emails from <strong className="text-slate-900 dark:text-slate-100">September 17, 2021</strong> through his final email on <strong className="text-slate-900 dark:text-slate-100">October 23, 2025</strong>.
                </p>
                <p className="text-slate-600 dark:text-slate-400 text-sm">
                  If you'd like to contribute to this archive, please DM me or reach out at{' '}
                  <a
                    href="mailto:bo@momentummarketinglab.com"
                    className="text-blue-600 dark:text-blue-400 hover:underline font-medium"
                  >
                    bo@momentummarketinglab.com
                  </a>
                </p>
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="mb-8 space-y-4">
        <SearchBar
          value={searchQuery}
          onChange={setSearchQuery}
          placeholder="Search emails..."
        />

        {/* Sort and Actions Bar */}
        <div className="flex flex-wrap items-center gap-3">
          <span className="text-sm font-medium text-slate-700 dark:text-slate-300">Sort:</span>
          <div className="flex gap-2">
            <button
              onClick={() => setSortOrder('newest')}
              className={`px-4 py-2 rounded-xl text-sm font-medium transition-all ${
                sortOrder === 'newest'
                  ? 'bg-gradient-to-r from-blue-600 to-cyan-600 text-white shadow-lg'
                  : 'bg-white/60 dark:bg-slate-800/40 text-slate-700 dark:text-slate-300 hover:bg-white dark:hover:bg-slate-800 border border-slate-200 dark:border-slate-700'
              }`}
            >
              Newest
            </button>
            <button
              onClick={() => setSortOrder('oldest')}
              className={`px-4 py-2 rounded-xl text-sm font-medium transition-all ${
                sortOrder === 'oldest'
                  ? 'bg-gradient-to-r from-blue-600 to-cyan-600 text-white shadow-lg'
                  : 'bg-white/60 dark:bg-slate-800/40 text-slate-700 dark:text-slate-300 hover:bg-white dark:hover:bg-slate-800 border border-slate-200 dark:border-slate-700'
              }`}
            >
              Oldest
            </button>
          </div>

          <div className="h-6 w-px bg-slate-300 dark:bg-slate-700"></div>

          {/* Random Email Button */}
          <button
            onClick={getRandomEmail}
            className="px-4 py-2 rounded-xl text-sm font-medium transition-all bg-white/60 dark:bg-slate-800/40 text-slate-700 dark:text-slate-300 hover:bg-gradient-to-r hover:from-purple-600 hover:to-pink-600 hover:text-white border border-slate-200 dark:border-slate-700"
          >
            📧 Read a random email
          </button>

          {/* Favorites Toggle */}
          <button
            onClick={() => setShowFavoritesOnly(!showFavoritesOnly)}
            className={`px-4 py-2 rounded-xl text-sm font-medium transition-all ${
              showFavoritesOnly
                ? 'bg-gradient-to-r from-red-500 to-pink-500 text-white shadow-lg'
                : 'bg-white/60 dark:bg-slate-800/40 text-slate-700 dark:text-slate-300 hover:bg-white dark:hover:bg-slate-800 border border-slate-200 dark:border-slate-700'
            }`}
          >
            ❤️ {showFavoritesOnly ? `Favorites (${favorites.size})` : 'Show Favorites'}
          </button>
        </div>

        {/* Year Filter */}
        {years.length > 0 && (
          <div className="flex flex-wrap items-center gap-3">
            <span className="text-sm font-medium text-slate-700 dark:text-slate-300">Year:</span>
            <div className="flex flex-wrap gap-2">
              <button
                onClick={() => setSelectedYear(null)}
                className={`px-4 py-2 rounded-xl text-sm font-medium transition-all ${
                  selectedYear === null
                    ? 'bg-gradient-to-r from-blue-600 to-cyan-600 text-white shadow-lg'
                    : 'bg-white/60 dark:bg-slate-800/40 text-slate-700 dark:text-slate-300 hover:bg-white dark:hover:bg-slate-800 border border-slate-200 dark:border-slate-700'
                }`}
              >
                All Years
              </button>
              {years.map(year => (
                <button
                  key={year}
                  onClick={() => setSelectedYear(year)}
                  className={`px-4 py-2 rounded-xl text-sm font-medium transition-all ${
                    selectedYear === year
                      ? 'bg-gradient-to-r from-blue-600 to-cyan-600 text-white shadow-lg'
                      : 'bg-white/60 dark:bg-slate-800/40 text-slate-700 dark:text-slate-300 hover:bg-white dark:hover:bg-slate-800 border border-slate-200 dark:border-slate-700'
                  }`}
                >
                  {year}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        {Object.keys(topics).length > 0 && (
          <aside className="lg:col-span-1">
            <TopicFilter
              topics={topics}
              selectedTopic={selectedTopic}
              onSelectTopic={setSelectedTopic}
            />
          </aside>
        )}

        <div className={Object.keys(topics).length > 0 ? 'lg:col-span-3' : 'lg:col-span-4'}>
          <EmailList
            emails={filteredEmails}
            userName={userName}
            favorites={favorites}
            onToggleFavorite={toggleFavorite}
            randomEmail={randomEmail}
            onCloseRandom={() => setRandomEmail(null)}
          />
        </div>
      </div>

      <NameInputModal onNameSet={setUserName} />
    </main>
  )
}
