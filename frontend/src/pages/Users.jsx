import { useEffect, useState } from 'react'
import { createUser, fetchUsers } from '../api/client'

const roles = ['ADMIN', 'SUPERVISOR', 'DRIVER']

export default function Users() {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')
  const [form, setForm] = useState({
    email: '',
    full_name: '',
    password: '',
    role: 'DRIVER',
  })

  async function loadUsers() {
    try {
      setLoading(true)
      setError('')
      setUsers(await fetchUsers())
    } catch (requestError) {
      setError(requestError.response?.data?.detail || requestError.message || 'No se pudo cargar usuarios.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    let active = true

    async function load() {
      try {
        setLoading(true)
        setError('')
        const data = await fetchUsers()
        if (active) {
          setUsers(data)
        }
      } catch (requestError) {
        if (active) {
          setError(requestError.response?.data?.detail || requestError.message || 'No se pudo cargar usuarios.')
        }
      } finally {
        if (active) {
          setLoading(false)
        }
      }
    }

    load()
    return () => {
      active = false
    }
  }, [])

  function updateField(event) {
    const { name, value } = event.target
    setForm((current) => ({ ...current, [name]: value }))
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setSubmitting(true)
    setError('')
    setMessage('')

    try {
      await createUser(form)
      setMessage('Usuario creado correctamente.')
      setForm({ email: '', full_name: '', password: '', role: 'DRIVER' })
      await loadUsers()
    } catch (requestError) {
      setError(requestError.response?.data?.detail || requestError.message || 'No se pudo crear usuario.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <main className="mx-auto flex w-full max-w-7xl flex-1 flex-col gap-5 px-4 py-5 sm:px-6 lg:px-8">
      <div>
        <p className="text-sm font-medium uppercase text-slate-500">ADMIN</p>
        <h1 className="text-2xl font-semibold text-ink sm:text-3xl">Usuarios</h1>
      </div>

      <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
        <h2 className="mb-4 text-base font-semibold text-ink">Crear usuario</h2>
        <form className="grid gap-4 md:grid-cols-2" onSubmit={handleSubmit}>
          <input className="rounded-lg border border-slate-300 px-3 py-2 text-sm" name="email" onChange={updateField} placeholder="email" type="email" value={form.email} />
          <input className="rounded-lg border border-slate-300 px-3 py-2 text-sm" name="full_name" onChange={updateField} placeholder="nombre" value={form.full_name} />
          <input className="rounded-lg border border-slate-300 px-3 py-2 text-sm" name="password" onChange={updateField} placeholder="password" type="password" value={form.password} />
          <select className="rounded-lg border border-slate-300 px-3 py-2 text-sm" name="role" onChange={updateField} value={form.role}>
            {roles.map((role) => <option key={role} value={role}>{role}</option>)}
          </select>
          <button className="rounded-lg bg-ink px-4 py-2 text-sm font-semibold text-white disabled:opacity-60 md:w-fit" disabled={submitting} type="submit">
            {submitting ? 'Creando...' : 'Crear usuario'}
          </button>
        </form>
      </section>

      {message && <p className="rounded-lg bg-emerald-50 p-3 text-sm font-medium text-emerald-700">{message}</p>}
      {error && <p className="rounded-lg bg-red-50 p-3 text-sm font-medium text-red-700">{error}</p>}

      <section className="overflow-hidden rounded-lg border border-slate-200 bg-white shadow-sm">
        {loading ? (
          <p className="p-5 text-sm text-muted">Cargando usuarios...</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-slate-200 text-sm">
              <thead className="bg-slate-50 text-left text-xs font-semibold uppercase text-slate-500">
                <tr>
                  <th className="px-4 py-3">Email</th>
                  <th className="px-4 py-3">Nombre</th>
                  <th className="px-4 py-3">Rol</th>
                  <th className="px-4 py-3">Activo</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {users.map((user) => (
                  <tr key={user.id}>
                    <td className="px-4 py-3 font-medium text-ink">{user.email}</td>
                    <td className="px-4 py-3 text-muted">{user.full_name}</td>
                    <td className="px-4 py-3 text-muted">{user.role}</td>
                    <td className="px-4 py-3 text-muted">{user.is_active ? 'Si' : 'No'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </main>
  )
}
