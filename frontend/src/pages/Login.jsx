import { useState } from 'react'
import { useAuth } from '../auth/useAuth'

export default function Login() {
  const { login } = useAuth()
  const [email, setEmail] = useState('admin@ailogix.local')
  const [password, setPassword] = useState('ChangeMe123!')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleSubmit(event) {
    event.preventDefault()
    setLoading(true)
    setError('')

    try {
      await login({ email, password })
    } catch (requestError) {
      setError(requestError.response?.data?.detail || requestError.message || 'No se pudo iniciar sesion.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-100 px-4 py-8">
      <section className="w-full max-w-md rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
        <div className="mb-6 space-y-2">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-ink text-sm font-bold text-white">AL</div>
          <h1 className="text-2xl font-semibold text-ink">Ingresar a AI Logix</h1>
          <p className="text-sm text-muted">Acceso operativo protegido por JWT.</p>
        </div>

        <form className="space-y-4" onSubmit={handleSubmit}>
          <label className="block space-y-1 text-sm font-medium text-slate-700">
            Email
            <input className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm" onChange={(event) => setEmail(event.target.value)} type="email" value={email} />
          </label>
          <label className="block space-y-1 text-sm font-medium text-slate-700">
            Password
            <input className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm" onChange={(event) => setPassword(event.target.value)} type="password" value={password} />
          </label>
          {error && <p className="rounded-lg bg-red-50 p-3 text-sm font-medium text-red-700">{error}</p>}
          <button className="w-full rounded-lg bg-ink px-4 py-2.5 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-60" disabled={loading} type="submit">
            {loading ? 'Ingresando...' : 'Ingresar'}
          </button>
        </form>
      </section>
    </main>
  )
}
