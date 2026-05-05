import { useEffect, useState } from 'react'
import Dashboard from './pages/Dashboard'
import Evidence from './pages/Evidence'

const routes = {
  dashboard: '/',
  evidence: '/evidence',
}

function App() {
  const [path, setPath] = useState(window.location.pathname)
  const [refreshKey, setRefreshKey] = useState(0)

  useEffect(() => {
    function handlePopState() {
      setPath(window.location.pathname)
    }

    window.addEventListener('popstate', handlePopState)
    return () => window.removeEventListener('popstate', handlePopState)
  }, [])

  function navigate(nextPath) {
    window.history.pushState({}, '', nextPath)
    setPath(nextPath)
  }

  function handleUploadComplete() {
    setRefreshKey((current) => current + 1)
  }

  const currentPath = path === routes.evidence ? routes.evidence : routes.dashboard

  return (
    <div className="min-h-screen bg-slate-100">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex min-h-16 w-full max-w-7xl flex-col gap-3 px-4 py-3 sm:flex-row sm:items-center sm:justify-between sm:px-6 lg:px-8">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-ink text-sm font-bold text-white">
              AL
            </div>
            <div>
              <p className="text-sm font-semibold text-ink">AI Logix</p>
              <p className="text-xs text-muted">Panel operativo</p>
            </div>
          </div>
          <nav className="flex gap-2">
            <button
              className={`rounded-lg px-3 py-2 text-sm font-semibold ${currentPath === routes.dashboard ? 'bg-ink text-white' : 'bg-slate-100 text-slate-700'}`}
              onClick={() => navigate(routes.dashboard)}
              type="button"
            >
              Dashboard
            </button>
            <button
              className={`rounded-lg px-3 py-2 text-sm font-semibold ${currentPath === routes.evidence ? 'bg-ink text-white' : 'bg-slate-100 text-slate-700'}`}
              onClick={() => navigate(routes.evidence)}
              type="button"
            >
              Evidencia
            </button>
          </nav>
        </div>
      </header>
      {currentPath === routes.evidence ? (
        <Evidence onUploadComplete={handleUploadComplete} />
      ) : (
        <Dashboard refreshKey={refreshKey} />
      )}
    </div>
  )
}

export default App
