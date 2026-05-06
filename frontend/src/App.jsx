import { useEffect, useState } from 'react'
import ProtectedRoute from './auth/ProtectedRoute'
import RoleRoute from './auth/RoleRoute'
import { useAuth } from './auth/useAuth'
import Dashboard from './pages/Dashboard'
import Evidence from './pages/Evidence'
import HumanReview from './pages/HumanReview'
import Users from './pages/Users'

const routes = {
  dashboard: '/',
  evidence: '/evidence',
  review: '/review',
  users: '/users',
}

function App() {
  const { logout, user, hasRole } = useAuth()
  const [path, setPath] = useState(window.location.pathname)
  const [refreshKey, setRefreshKey] = useState(0)
  const [lastEvidenceEventId, setLastEvidenceEventId] = useState('')

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

  function handleUploadComplete(result) {
    if (result?.event_id) {
      setLastEvidenceEventId(result.event_id)
    }
    setRefreshKey((current) => current + 1)
  }

  const knownPaths = Object.values(routes)
  const currentPath = knownPaths.includes(path) ? path : routes.dashboard

  function renderRoute() {
    if (currentPath === routes.review) {
      return (
        <RoleRoute roles={['ADMIN', 'SUPERVISOR']}>
          <HumanReview onReviewComplete={() => setRefreshKey((current) => current + 1)} />
        </RoleRoute>
      )
    }

    if (currentPath === routes.evidence) {
      return (
        <RoleRoute roles={['ADMIN', 'SUPERVISOR', 'DRIVER']}>
          <Evidence lastEvidenceEventId={lastEvidenceEventId} onUploadComplete={handleUploadComplete} />
        </RoleRoute>
      )
    }

    if (currentPath === routes.users) {
      return (
        <RoleRoute roles={['ADMIN']}>
          <Users />
        </RoleRoute>
      )
    }

    return (
      <RoleRoute roles={['ADMIN', 'SUPERVISOR']}>
        <Dashboard refreshKey={refreshKey} />
      </RoleRoute>
    )
  }

  return (
    <ProtectedRoute>
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
          <nav className="flex flex-wrap items-center gap-2">
            {hasRole(['ADMIN', 'SUPERVISOR']) && (
              <button
                className={`rounded-lg px-3 py-2 text-sm font-semibold ${currentPath === routes.dashboard ? 'bg-ink text-white' : 'bg-slate-100 text-slate-700'}`}
                onClick={() => navigate(routes.dashboard)}
                type="button"
              >
                Dashboard
              </button>
            )}
            <button
              className={`rounded-lg px-3 py-2 text-sm font-semibold ${currentPath === routes.evidence ? 'bg-ink text-white' : 'bg-slate-100 text-slate-700'}`}
              onClick={() => navigate(routes.evidence)}
              type="button"
            >
              Evidencia
            </button>
            {hasRole(['ADMIN', 'SUPERVISOR']) && (
              <button
                className={`rounded-lg px-3 py-2 text-sm font-semibold ${currentPath === routes.review ? 'bg-ink text-white' : 'bg-slate-100 text-slate-700'}`}
                onClick={() => navigate(routes.review)}
                type="button"
              >
                Revision
              </button>
            )}
            {hasRole(['ADMIN']) && (
              <button
                className={`rounded-lg px-3 py-2 text-sm font-semibold ${currentPath === routes.users ? 'bg-ink text-white' : 'bg-slate-100 text-slate-700'}`}
                onClick={() => navigate(routes.users)}
                type="button"
              >
                Usuarios
              </button>
            )}
            <div className="ml-0 flex items-center gap-2 rounded-lg bg-slate-100 px-3 py-2 text-xs text-slate-700 sm:ml-2">
              <span>{user?.full_name || user?.email}</span>
              <span className="font-semibold">{user?.role}</span>
            </div>
            <button className="rounded-lg bg-slate-900 px-3 py-2 text-sm font-semibold text-white" onClick={logout} type="button">
              Salir
            </button>
          </nav>
        </div>
      </header>
      {renderRoute()}
    </div>
    </ProtectedRoute>
  )
}

export default App
