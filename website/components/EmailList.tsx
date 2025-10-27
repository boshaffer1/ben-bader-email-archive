'use client'

import { useState, useMemo } from 'react'

interface Email {
  id: string
  subject: string
  from: string
  date: string
  snippet: string
  body: string
  timestamp?: string
}

function decodeHtmlEntities(text: string): string {
  const textarea = document.createElement('textarea')
  textarea.innerHTML = text
  return textarea.value
}

function formatEmailBody(body: string, userName: string = 'friend'): string {
  let formatted = decodeHtmlEntities(body)

  // Replace name placeholders with user's name
  formatted = formatted.replace(/\bAdam\b/g, userName)
  formatted = formatted.replace(/\bBo\b/g, userName)
  formatted = formatted.replace(/\bB\b/g, userName)
  formatted = formatted.replace(/first_name/g, userName)

  // Make URLs clickable with nice styling - extract domain name for display
  formatted = formatted.replace(
    /(https?:\/\/([^\s/]+)[^\s]*)/g,
    (match, url, domain) => {
      // Clean up domain (remove www. prefix if exists)
      const cleanDomain = domain.replace(/^www\./, '')
      return `<a href="${url}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1 text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 underline decoration-blue-400/30 hover:decoration-blue-600 transition-colors"><svg class="w-4 h-4 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>${cleanDomain}</a>`
    }
  )

  // Clean up excessive whitespace
  formatted = formatted.replace(/\n{3,}/g, '\n\n')

  return formatted
}

export default function EmailList({ emails, userName = 'friend' }: { emails: Email[], userName?: string }) {
  const [selectedEmail, setSelectedEmail] = useState<Email | null>(null)

  const formattedBody = useMemo(() => {
    if (!selectedEmail) return ''
    return formatEmailBody(selectedEmail.body, userName)
  }, [selectedEmail, userName])

  if (emails.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        No emails found matching your criteria
      </div>
    )
  }

  return (
    <div>
      <div className="space-y-6">
        {emails.map(email => (
          <div
            key={email.id}
            className="group bg-white/60 dark:bg-slate-800/40 backdrop-blur-sm border border-slate-200/50 dark:border-slate-700/50 rounded-2xl p-8 hover:shadow-2xl hover:border-blue-200 dark:hover:border-blue-800 transition-all duration-300 cursor-pointer"
            onClick={() => setSelectedEmail(email)}
          >
            <h3 className="text-2xl font-semibold mb-3 text-slate-900 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
              {decodeHtmlEntities(email.subject)}
            </h3>
            <div className="text-sm font-medium text-blue-600 dark:text-blue-400 mb-4">
              {new Date(parseInt(email.timestamp || '0')).toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
              })}
            </div>
            <p className="text-slate-600 dark:text-slate-400 line-clamp-2 leading-relaxed">
              {decodeHtmlEntities(email.snippet)}
            </p>
          </div>
        ))}
      </div>

      {selectedEmail && (
        <div
          className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 z-50 animate-in fade-in duration-200"
          onClick={() => setSelectedEmail(null)}
        >
          <div
            className="bg-white dark:bg-slate-900 rounded-3xl max-w-4xl w-full max-h-[90vh] overflow-y-auto p-12 shadow-2xl border border-slate-200 dark:border-slate-800 animate-in zoom-in-95 duration-300"
            onClick={e => e.stopPropagation()}
          >
            <div className="flex justify-between items-start mb-8">
              <div>
                <h2 className="text-4xl font-bold mb-4 text-slate-900 dark:text-white leading-tight">
                  {decodeHtmlEntities(selectedEmail.subject)}
                </h2>
                <div className="space-y-1 text-slate-600 dark:text-slate-400">
                  <div className="font-medium">{selectedEmail.from}</div>
                  <div className="text-sm">
                    {new Date(parseInt(selectedEmail.timestamp || '0')).toLocaleDateString('en-US', {
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric',
                      hour: 'numeric',
                      minute: 'numeric'
                    })}
                  </div>
                </div>
              </div>
              <button
                onClick={() => setSelectedEmail(null)}
                className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 text-3xl transition-colors p-2 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-full"
              >
                ×
              </button>
            </div>
            <div className="prose prose-lg dark:prose-invert max-w-none prose-headings:text-slate-900 dark:prose-headings:text-white prose-p:text-slate-700 dark:prose-p:text-slate-300 prose-a:text-blue-600 dark:prose-a:text-blue-400">
              <div
                dangerouslySetInnerHTML={{ __html: formattedBody }}
                className="whitespace-pre-wrap leading-relaxed"
                style={{
                  fontSize: '1.0625rem',
                  lineHeight: '1.8'
                }}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
