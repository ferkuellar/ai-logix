import { useState } from 'react'

const statusOptions = ['PENDING', 'DELIVERED', 'PARTIAL', 'FAILED', 'CANCELLED']

function productsToText(products) {
  if (!Array.isArray(products) || products.length === 0) return '[]'
  return JSON.stringify(products, null, 2)
}

export default function HumanConfirmForm({ detail, submitting, onConfirm }) {
  const extracted = detail?.ai_extracted_json || {}
  const confirmedData = extracted.confirmed_data || {}
  const [form, setForm] = useState(() => ({
    order_number: confirmedData.order_number || extracted.order_number || detail?.order_number || '',
    store_code: confirmedData.store_code || extracted.store_code || '',
    store_name: confirmedData.store_name || extracted.store_name || '',
    barcode: confirmedData.barcode || extracted.barcode || '',
    products: productsToText(confirmedData.products || extracted.products),
    status: confirmedData.status || extracted.status_suggestion || detail?.status || 'DELIVERED',
    latitude: confirmedData.latitude ?? detail?.latitude ?? '',
    longitude: confirmedData.longitude ?? detail?.longitude ?? '',
    observations: confirmedData.observations || extracted.observations || detail?.observations || '',
  }))
  const [error, setError] = useState('')

  function updateField(event) {
    const { name, value } = event.target
    setForm((current) => ({ ...current, [name]: value }))
  }

  function handleSubmit(event) {
    event.preventDefault()
    setError('')

    let products
    try {
      products = JSON.parse(form.products || '[]')
      if (!Array.isArray(products)) {
        throw new Error('products debe ser una lista JSON.')
      }
    } catch (parseError) {
      setError(parseError.message || 'Products debe ser JSON valido.')
      return
    }

    if (!form.order_number.trim()) {
      setError('order_number es requerido para confirmar.')
      return
    }

    onConfirm({
      order_number: form.order_number.trim(),
      store_code: form.store_code.trim() || null,
      store_name: form.store_name.trim() || null,
      barcode: form.barcode.trim() || null,
      products,
      status: form.status,
      latitude: form.latitude === '' ? null : Number(form.latitude),
      longitude: form.longitude === '' ? null : Number(form.longitude),
      observations: form.observations.trim() || null,
    })
  }

  return (
    <form className="space-y-4" onSubmit={handleSubmit}>
      <div className="grid gap-4 md:grid-cols-2">
        <label className="space-y-1 text-sm font-medium text-slate-700">
          Pedido
          <input className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm" name="order_number" onChange={updateField} value={form.order_number} />
        </label>
        <label className="space-y-1 text-sm font-medium text-slate-700">
          Estado
          <select className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm" name="status" onChange={updateField} value={form.status}>
            {statusOptions.map((status) => (
              <option key={status} value={status}>{status}</option>
            ))}
          </select>
        </label>
        <label className="space-y-1 text-sm font-medium text-slate-700">
          Codigo tienda
          <input className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm" name="store_code" onChange={updateField} value={form.store_code} />
        </label>
        <label className="space-y-1 text-sm font-medium text-slate-700">
          Tienda
          <input className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm" name="store_name" onChange={updateField} value={form.store_name} />
        </label>
        <label className="space-y-1 text-sm font-medium text-slate-700">
          Codigo de barras
          <input className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm" name="barcode" onChange={updateField} value={form.barcode} />
        </label>
        <div className="grid gap-4 sm:grid-cols-2">
          <label className="space-y-1 text-sm font-medium text-slate-700">
            Latitud
            <input className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm" name="latitude" onChange={updateField} type="number" value={form.latitude} />
          </label>
          <label className="space-y-1 text-sm font-medium text-slate-700">
            Longitud
            <input className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm" name="longitude" onChange={updateField} type="number" value={form.longitude} />
          </label>
        </div>
      </div>
      <label className="block space-y-1 text-sm font-medium text-slate-700">
        Productos JSON
        <textarea className="min-h-28 w-full rounded-lg border border-slate-300 px-3 py-2 font-mono text-xs" name="products" onChange={updateField} value={form.products} />
      </label>
      <label className="block space-y-1 text-sm font-medium text-slate-700">
        Observaciones
        <textarea className="min-h-20 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm" name="observations" onChange={updateField} value={form.observations} />
      </label>
      {error && <p className="rounded-lg bg-red-50 p-3 text-sm font-medium text-red-700">{error}</p>}
      <button className="rounded-lg bg-emerald-600 px-4 py-2 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-60" disabled={submitting} type="submit">
        {submitting ? 'Confirmando...' : 'Confirmar datos'}
      </button>
    </form>
  )
}
