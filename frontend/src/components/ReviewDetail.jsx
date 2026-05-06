import { buildPublicUrl } from '../api/client'
import HumanConfirmForm from './HumanConfirmForm'
import HumanRejectForm from './HumanRejectForm'

const statusLabels = {
  OCR_PENDING: 'Pendiente',
  OCR_PROCESSED: 'Procesado por OCR',
  HUMAN_REVIEW_REQUIRED: 'Requiere revision',
  HUMAN_CONFIRMED: 'Confirmado',
  HUMAN_REJECTED: 'Rechazado',
}

export default function ReviewDetail({ detail, loading, error, submitting, message, onConfirm, onReject }) {
  if (!detail && !loading && !error) {
    return (
      <section className="rounded-lg border border-slate-200 bg-white p-5 text-sm text-muted shadow-sm">
        Selecciona una evidencia para revisar.
      </section>
    )
  }

  if (loading) {
    return (
      <section className="rounded-lg border border-slate-200 bg-white p-5 text-sm text-muted shadow-sm">
        Cargando detalle de revision...
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

  const extracted = detail.ai_extracted_json || {}
  const photoUrl = buildPublicUrl(detail.photo_url)

  return (
    <section className="space-y-5">
      {message && (
        <div className="rounded-lg border border-emerald-200 bg-emerald-50 p-4 text-sm font-medium text-emerald-700">
          {message}
        </div>
      )}

      <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
        <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
          <div>
            <h2 className="text-lg font-semibold text-ink">Detalle de evidencia</h2>
            <p className="break-all text-xs text-muted">{detail.event_id}</p>
          </div>
          <span className="w-fit rounded-full bg-amber-100 px-2.5 py-1 text-xs font-semibold text-amber-800">
            {statusLabels[detail.review_status] || detail.review_status}
          </span>
        </div>

        <div className="mt-5 grid gap-5 lg:grid-cols-[minmax(0,0.9fr)_minmax(0,1.1fr)]">
          <div className="space-y-4">
            {photoUrl ? (
              <img alt="Evidencia de entrega" className="max-h-[420px] w-full rounded-lg border border-slate-200 object-contain" src={photoUrl} />
            ) : (
              <div className="rounded-lg border border-slate-200 bg-slate-50 p-6 text-sm text-muted">Sin foto asociada.</div>
            )}
            <div>
              <h3 className="text-sm font-semibold text-ink">Texto OCR</h3>
              <pre className="mt-2 max-h-56 overflow-auto rounded-lg bg-slate-950 p-3 text-xs text-slate-100">{detail.ocr_text || 'Sin texto OCR.'}</pre>
            </div>
          </div>

          <div className="space-y-4">
            <div>
              <h3 className="text-sm font-semibold text-ink">JSON extraido</h3>
              <pre className="mt-2 max-h-80 overflow-auto rounded-lg bg-slate-950 p-3 text-xs text-slate-100">{JSON.stringify(extracted, null, 2)}</pre>
            </div>
            <HumanConfirmForm key={detail.event_id} detail={detail} onConfirm={onConfirm} submitting={submitting === 'confirm'} />
            <div className="border-t border-slate-200 pt-4">
              <HumanRejectForm onReject={onReject} submitting={submitting === 'reject'} />
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
