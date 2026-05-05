import { useEffect, useMemo, useState } from 'react'
import { buildPublicUrl, uploadEvidence } from '../api/client'
import { STATUS_LABELS } from '../utils/status'

const initialValues = {
  order_number: '',
  status: '',
  latitude: '',
  longitude: '',
  observations: '',
}

const allowedTypes = ['image/jpeg', 'image/png', 'image/webp']

export default function EvidenceUploadForm({ onUploadComplete }) {
  const [values, setValues] = useState(initialValues)
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [result, setResult] = useState(null)

  const publicPhotoUrl = useMemo(() => buildPublicUrl(result?.photo_url), [result])
  const previewUrl = useMemo(() => (file ? URL.createObjectURL(file) : ''), [file])

  useEffect(() => {
    return () => {
      if (previewUrl) URL.revokeObjectURL(previewUrl)
    }
  }, [previewUrl])

  function handleChange(event) {
    const { name, value } = event.target
    setValues((current) => ({ ...current, [name]: value }))
  }

  function handleFileChange(event) {
    const selectedFile = event.target.files?.[0] || null
    setResult(null)
    setError('')

    if (!selectedFile) {
      setFile(null)
      return
    }

    if (!allowedTypes.includes(selectedFile.type)) {
      setFile(null)
      setError('Selecciona una imagen JPG, PNG o WEBP.')
      return
    }

    setFile(selectedFile)
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setError('')
    setResult(null)

    if (!values.order_number.trim()) {
      setError('Captura el numero de pedido.')
      return
    }

    if (!file) {
      setError('Selecciona una imagen de evidencia.')
      return
    }

    const formData = new FormData()
    formData.append('order_number', values.order_number.trim())
    formData.append('file', file)

    if (values.status) formData.append('status', values.status)
    if (values.latitude) formData.append('latitude', values.latitude)
    if (values.longitude) formData.append('longitude', values.longitude)
    if (values.observations.trim()) formData.append('observations', values.observations.trim())

    try {
      setLoading(true)
      const uploadResult = await uploadEvidence(formData)
      setResult(uploadResult)
      setValues(initialValues)
      setFile(null)
      onUploadComplete?.(uploadResult)
    } catch (requestError) {
      setError(requestError.response?.data?.detail || requestError.message || 'No se pudo subir la evidencia.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="grid gap-5 lg:grid-cols-[minmax(0,1fr)_360px]">
      <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
        <div className="grid gap-4 sm:grid-cols-2">
          <label className="flex flex-col gap-1 text-sm font-medium text-slate-700">
            Numero de pedido
            <input
              className="rounded-lg border border-slate-300 px-3 py-2 text-sm font-normal outline-none ring-0 focus:border-slate-500"
              name="order_number"
              value={values.order_number}
              onChange={handleChange}
              placeholder="OX-1001"
              required
            />
          </label>

          <label className="flex flex-col gap-1 text-sm font-medium text-slate-700">
            Estado
            <select
              className="rounded-lg border border-slate-300 px-3 py-2 text-sm font-normal outline-none focus:border-slate-500"
              name="status"
              value={values.status}
              onChange={handleChange}
            >
              <option value="">Sin cambio de estado</option>
              {Object.entries(STATUS_LABELS).map(([value, label]) => (
                <option key={value} value={value}>{label}</option>
              ))}
            </select>
          </label>

          <label className="flex flex-col gap-1 text-sm font-medium text-slate-700">
            Latitud
            <input
              className="rounded-lg border border-slate-300 px-3 py-2 text-sm font-normal outline-none focus:border-slate-500"
              name="latitude"
              value={values.latitude}
              onChange={handleChange}
              placeholder="25.6866"
              type="number"
              step="any"
            />
          </label>

          <label className="flex flex-col gap-1 text-sm font-medium text-slate-700">
            Longitud
            <input
              className="rounded-lg border border-slate-300 px-3 py-2 text-sm font-normal outline-none focus:border-slate-500"
              name="longitude"
              value={values.longitude}
              onChange={handleChange}
              placeholder="-100.3161"
              type="number"
              step="any"
            />
          </label>

          <label className="flex flex-col gap-1 text-sm font-medium text-slate-700 sm:col-span-2">
            Observaciones
            <textarea
              className="min-h-24 rounded-lg border border-slate-300 px-3 py-2 text-sm font-normal outline-none focus:border-slate-500"
              name="observations"
              value={values.observations}
              onChange={handleChange}
              placeholder="Evidencia de surtido, entrega parcial, anaquel, ticket o fachada."
            />
          </label>

          <label className="flex flex-col gap-1 text-sm font-medium text-slate-700 sm:col-span-2">
            Imagen
            <input
              accept="image/jpeg,image/png,image/webp"
              className="rounded-lg border border-dashed border-slate-300 bg-slate-50 px-3 py-3 text-sm font-normal"
              type="file"
              onChange={handleFileChange}
              required
            />
          </label>
        </div>

        {error && (
          <div className="mt-4 rounded-lg border border-red-200 bg-red-50 p-3 text-sm font-medium text-red-700">
            {error}
          </div>
        )}

        {result && (
          <div className="mt-4 rounded-lg border border-green-200 bg-green-50 p-3 text-sm text-green-800">
            <p className="font-semibold">Evidencia guardada correctamente.</p>
            <a className="mt-1 inline-flex font-medium underline" href={publicPhotoUrl} target="_blank" rel="noreferrer">
              {publicPhotoUrl}
            </a>
          </div>
        )}

        <div className="mt-5 flex justify-end">
          <button
            className="rounded-lg bg-ink px-4 py-2 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:bg-slate-400"
            disabled={loading}
            type="submit"
          >
            {loading ? 'Subiendo evidencia...' : 'Subir evidencia'}
          </button>
        </div>
      </section>

      <aside className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
        <h2 className="text-base font-semibold text-ink">Preview</h2>
        <div className="mt-3 flex aspect-[4/3] items-center justify-center overflow-hidden rounded-lg border border-slate-200 bg-slate-50">
          {previewUrl ? (
            <img className="h-full w-full object-cover" src={previewUrl} alt="Preview de evidencia" />
          ) : (
            <p className="px-6 text-center text-sm text-muted">Selecciona una imagen para verla antes de subirla.</p>
          )}
        </div>
        <p className="mt-3 text-xs text-muted">Formatos permitidos: JPG, PNG o WEBP. Tamano maximo: 10 MB.</p>
      </aside>
    </form>
  )
}
