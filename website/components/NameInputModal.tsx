'use client'

import { useState, useEffect } from 'react'

interface NameInputModalProps {
  onNameSet: (name: string) => void
}

export default function NameInputModal({ onNameSet }: NameInputModalProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [name, setName] = useState('')

  useEffect(() => {
    const savedName = localStorage.getItem('userName')
    if (!savedName) {
      setIsOpen(true)
    } else {
      onNameSet(savedName)
    }
  }, [onNameSet])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (name.trim()) {
      localStorage.setItem('userName', name.trim())
      onNameSet(name.trim())
      setIsOpen(false)
    }
  }

  const handleSkip = () => {
    localStorage.setItem('userName', 'friend')
    onNameSet('friend')
    setIsOpen(false)
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 z-50 animate-in fade-in duration-300">
      <div className="bg-white dark:bg-slate-900 rounded-3xl max-w-md w-full p-10 shadow-2xl border border-slate-200 dark:border-slate-800 animate-in zoom-in-95 duration-300">
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold mb-3 text-slate-900 dark:text-white">
            Welcome
          </h2>
          <p className="text-slate-600 dark:text-slate-400 leading-relaxed">
            Ben's emails were personal and spoke directly to each reader. Enter your name to experience them the way he intended.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="name" className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
              Your first name
            </label>
            <input
              type="text"
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Enter your name..."
              className="w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-white placeholder-slate-400 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
              autoFocus
            />
          </div>

          <div className="flex gap-3">
            <button
              type="button"
              onClick={handleSkip}
              className="flex-1 px-6 py-3 rounded-xl border border-slate-300 dark:border-slate-600 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 transition-all font-medium"
            >
              Skip
            </button>
            <button
              type="submit"
              className="flex-1 px-6 py-3 rounded-xl bg-gradient-to-r from-blue-600 to-cyan-600 text-white hover:from-blue-700 hover:to-cyan-700 transition-all font-medium shadow-lg hover:shadow-xl"
            >
              Continue
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
