import { useMemo, useState } from 'react'
import { confirmOcrResult, fetchOcrResult, processOcr } from '../api/client'
import { STATUS_LABELS } from '../utils/status'

const emptyForm = {
  order_number: '',
  store_code: '',
  store_name: '',
  barcode: '',
  products: '',
  status: '',
  observations: '',
}

function toProductsText(products) {
  if (!Array.isArray(products) || products.length === 0) return ''
  return products.map((product) => `${product.name || ''}|${product.quantity || ''}`).join('\n')
}

function parseProducts(value) {
  return value
    .split('\n')
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line) => {
      const [name, quantity] = line.split('|').map((item) => item.trim())
      const parsedQuantity = Number(quantity)
      return {
        name,
        quantity: Number.isFinite(parsedQuantity) ? parsedQuantity : null,
      }
    })
}

export default function OcrResultPanel({ eventId, onConfirmed }) {
  const [status, setStatus] = useState(eventId ? 'not_processed' : 'idle')
  const [error, setError] = useState('')
  const [result, setResult] = useState(null)
  const [form, setForm] = useState(emptyForm)

  const extracted = result?.ai_extracted_json || {}
  const statusLabel = useMemo(() => {
    if (status === 'idle') return 'Sin evidencia'
    if (status === 'not_processed') return 'No procesado'
    if (status === 'processing') return 'Procesando'
    if (status === 'processed') return 'Procesado'
    if (status === 'confirmed') return 'Confirmado'
    return 'Error'
  }, [status])

  function hydrateForm(data) {
    const payload = data?.ai_extracted_json || {}
    setForm({
      order_number: payload.order_number || data?.order_number || '',
      store_code: payload.store_code || '',
      store_name: payload.store_name || '',
      barcode: payload.barcode || '',
      products: toProductsText(payload.products),
      status: payload.status_suggestion || '',
      observations: payload.observations || '',
    })
    setStatus(payload.confirmed ? 'confirmed' : 'processed')
  }

  async function handleProcess() {
    if (!eventId) return

    try {
      setStatus('processing')
      setError('')
      const data = await processOcr(eventId)
      setResult(data)
      hydrateForm(data)
    } catch (requestError) {
      setStatus('error')
      setError(requestError.response?.data?.detail || requestError.message || 'No se pudo procesar OCR.')
    }
  }

  async function handleRefresh() {
    if (!eventId) return

    try {
      setError('')
      const data = await fetchOcrResult(eventId)
      setResult(data)
      hydrateForm(data)
    } catch (requestError) {
      setStatus('error')
      setError(requestError.response?.data?.detail || requestError.message || 'No se pudo consultar OCR.')
    }
  }

  function handleChange(event) {
    const { name, value } = event.target
    setForm((current) => ({ ...current, [name]: value }))
  }

  async function handleConfirm(event) {
    event.preventDefault()

    try {
      setError('')
      const data = await confirmOcrResult(eventId, {
        order_number: form.order_number,
        store_code: form.store_code,
        store_name: form.store_name,
        barcode: form.barcode,
        products: parseProducts(form.products),
        status: form.status,
        observations: form.observations,
      })
      setResult((current) => ({ ...current, ...data }))
      setStatus('confirmed')
      onConfirmed?.(data)
    } catch (requestError) {
      setStatus('error')
      setError(requestError.response?.data?.detail || requestError.message || 'No se pudo confirmar OCR.')
    }
  }

  return (
    <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 className="text-base font-semibold text-ink">OCR / IA</h2>
          <p className="text-sm text-muted">Estado: {statusLabel}</p>
        </div>
        <div className="flex flex-wrap gap-2">
          <button
            className="rounded-lg bg-ink px-3 py-2 text-sm font-semibold text-white disabled:bg-slate-400"
            disabled={!eventId || status === 'processing'}
            onClick={handleProcess}
            type="button"
          >
            Procesar OCR
          </button>
          <button
            className="rounded-lg bg-slate-100 px-3 py-2 text-sm font-semibold text-slate-700 disabled:text-slate-400"
            disabled={!eventId}
            onClick={handleRefresh}
            type="button"
          >
            Consultar resultado
          </button>
        </div>
      </div>

      {error && (
        <div className="mt-4 rounded-lg border border-red-200 bg-red-50 p-3 text-sm font-medium text-red-700">
          {error}
        </div>
      )}

      {!eventId && (
        <div className="mt-4 rounded-lg border border-dashed border-slate-300 bg-slate-50 p-4 text-sm text-muted">
          Sube una evidencia para habilitar OCR.
        </div>
      )}

      {result && (
        <div className="mt-4 grid gap-4 lg:grid-cols-2">
          <div className="space-y-3">
            <div>
              <p className="text-sm font-semibold text-ink">Texto OCR</p>
              <pre className="mt-2 max-h-64 overflow-auto rounded-lg bg-slate-950 p-3 text-xs text-slate-100">{result.ocr_text || extracted.raw_text || 'Sin texto OCR.'}</pre>
            </div>
            <div>
              <p className="text-sm font-semibold text-ink">JSON extraido</p>
              <pre className="mt-2 max-h-64 overflow-auto rounded-lg bg-slate-50 p-3 text-xs text-slate-700">{JSON.stringify(extracted, null, 2)}</pre>
            </div>
          </div>

          <form onSubmit={handleConfirm} className="grid gap-3">
            <label className="flex flex-col gap-1 text-sm font-medium text-slate-700">
              Pedido detectado
              <input className="rounded-lg border border-slate-300 px-3 py-2 text-sm font-normal" name="order_number" value={form.order_number} onChange={handleChange} />
            </label>
            <label className="flex flex-col gap-1 text-sm font-medium text-slate-700">
              Codigo de tienda
              <input className="rounded-lg border border-slate-300 px-3 py-2 text-sm font-normal" name="store_code" value={form.store_code} onChange={handleChange} />
            </label>
            <label className="flex flex-col gap-1 text-sm font-medium text-slate-700">
              Tienda
              <input className="rounded-lg border border-slate-300 px-3 py-2 text-sm font-normal" name="store_name" value={form.store_name} onChange={handleChange} />
            </label>
            <label className="flex flex-col gap-1 text-sm font-medium text-slate-700">
              Codigo de barras
              <input className="rounded-lg border border-slate-300 px-3 py-2 text-sm font-normal" name="barcode" value={form.barcode} onChange={handleChange} />
            </label>
            <label className="flex flex-col gap-1 text-sm font-medium text-slate-700">
              Sugerencia de estado
              <select className="rounded-lg border border-slate-300 px-3 py-2 text-sm font-normal" name="status" value={form.status} onChange={handleChange}>
                <option value="">Sin estado</option>
                {Object.entries(STATUS_LABELS).map(([value, label]) => (
                  <option key={value} value={value}>{label}</option>
                ))}
              </select>
            </label>
            <label className="flex flex-col gap-1 text-sm font-medium text-slate-700">
              Productos
              <textarea className="min-h-20 rounded-lg border border-slate-300 px-3 py-2 text-sm font-normal" name="products" value={form.products} onChange={handleChange} placeholder="Producto demo|2" />
            </label>
            <label className="flex flex-col gap-1 text-sm font-medium text-slate-700">
              Observaciones
              <textarea className="min-h-20 rounded-lg border border-slate-300 px-3 py-2 text-sm font-normal" name="observations" value={form.observations} onChange={handleChange} />
            </label>
            <div className="flex items-center justify-between gap-3">
              <p className="text-sm text-muted">Confidence: {Number(extracted.confidence || 0).toFixed(2)}</p>
              <button className="rounded-lg bg-green-700 px-4 py-2 text-sm font-semibold text-white" type="submit">
                Confirmar OCR
              </button>
            </div>
          </form>
        </div>
      )}
    </section>
  )
}
