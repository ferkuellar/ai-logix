import { useState } from 'react'

export default function HumanRejectForm({ submitting, onReject }) {
  const [reason, setReason] = useState('')
  const [observations, setObservations] = useState('')
  const [error, setError] = useState('')

  function handleSubmit(event) {
    event.preventDefault()
    setError('')

    if (!reason.trim()) {
      setError('La razon de rechazo es obligatoria.')
      return
    }

    onReject({
      reason: reason.trim(),
      observations: observations.trim() || null,
    })
  }

  return (
    <form className="space-y-4" onSubmit={handleSubmit}>
      <label className="block space-y-1 text-sm font-medium text-slate-700">
        Razon de rechazo
        <input className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm" onChange={(event) => setReason(event.target.value)} value={reason} />
      </label>
      <label className="block space-y-1 text-sm font-medium text-slate-700">
        Observaciones
        <textarea className="min-h-20 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm" onChange={(event) => setObservations(event.target.value)} value={observations} />
      </label>
      {error && <p className="rounded-lg bg-red-50 p-3 text-sm font-medium text-red-700">{error}</p>}
      <button className="rounded-lg bg-red-600 px-4 py-2 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-60" disabled={submitting} type="submit">
        {submitting ? 'Rechazando...' : 'Rechazar OCR'}
      </button>
    </form>
  )
}
