const statusLabels = {
  OCR_PENDING: 'Pendiente',
  OCR_PROCESSED: 'Procesado por OCR',
  HUMAN_REVIEW_REQUIRED: 'Requiere revision',
  HUMAN_CONFIRMED: 'Confirmado',
  HUMAN_REJECTED: 'Rechazado',
}

export default function ReviewQueue({ items, selectedEventId, loading, error, onSelect }) {
  if (loading) {
    return (
      <section className="rounded-lg border border-slate-200 bg-white p-5 text-sm text-muted shadow-sm">
        Cargando cola de revision...
      </section>
    )
  }

  if (error) {
    return (
      <section className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm font-medium text-red-700">
        {error}
      </section>
    )
  }

  if (!items.length) {
    return (
      <section className="rounded-lg border border-slate-200 bg-white p-5 text-sm text-muted shadow-sm">
        No hay evidencias pendientes de revision humana.
      </section>
    )
  }

  return (
    <section className="space-y-3">
      <div>
        <h2 className="text-base font-semibold text-ink">Cola de revision</h2>
        <p className="text-sm text-muted">OCR tratado como sugerencia hasta confirmacion humana.</p>
      </div>
      <div className="grid gap-3">
        {items.map((item) => (
          <button
            className={`rounded-lg border p-4 text-left shadow-sm transition ${selectedEventId === item.event_id ? 'border-ink bg-slate-50' : 'border-slate-200 bg-white hover:border-slate-300'}`}
            key={item.event_id}
            onClick={() => onSelect(item.event_id)}
            type="button"
          >
            <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
              <div>
                <p className="text-sm font-semibold text-ink">{item.order_number || 'Sin pedido confirmado'}</p>
                <p className="break-all text-xs text-muted">{item.event_id}</p>
              </div>
              <span className="w-fit rounded-full bg-amber-100 px-2.5 py-1 text-xs font-semibold text-amber-800">
                {statusLabels[item.review_status] || item.review_status}
              </span>
            </div>
            <p className="mt-2 line-clamp-2 text-sm text-muted">{item.ocr_text || 'Sin texto OCR disponible.'}</p>
          </button>
        ))}
      </div>
    </section>
  )
}
