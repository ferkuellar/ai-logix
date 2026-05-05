import { getStatusBadgeClass, getStatusLabel } from '../utils/status'

function formatDate(value) {
  if (!value) return 'Sin fecha'

  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value

  return new Intl.DateTimeFormat('es-MX', {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(date)
}

function formatCoordinate(value) {
  const parsed = Number(value)
  return Number.isFinite(parsed) ? parsed.toFixed(6) : 'Sin dato'
}

export default function OrderStatesTable({ orderStates }) {
  if (orderStates.length === 0) {
    return (
      <div className="rounded-lg border border-dashed border-slate-300 bg-white p-6 text-center text-sm text-muted">
        No hay registros de pedidos todavia.
      </div>
    )
  }

  return (
    <div className="overflow-hidden rounded-lg border border-slate-200 bg-white shadow-sm">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-slate-200 text-left text-sm">
          <thead className="bg-slate-50 text-xs font-semibold uppercase text-slate-500">
            <tr>
              <th className="px-4 py-3">Pedido</th>
              <th className="px-4 py-3">Estado</th>
              <th className="px-4 py-3">Latitud</th>
              <th className="px-4 py-3">Longitud</th>
              <th className="px-4 py-3">Ultima actualizacion</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {orderStates.map((item) => (
              <tr key={item.id || item.order_number} className="hover:bg-slate-50">
                <td className="whitespace-nowrap px-4 py-3 font-medium text-ink">{item.order_number}</td>
                <td className="whitespace-nowrap px-4 py-3">
                  <span className={`inline-flex rounded-full px-2.5 py-1 text-xs font-semibold ring-1 ring-inset ${getStatusBadgeClass(item.current_status)}`}>
                    {getStatusLabel(item.current_status)}
                  </span>
                </td>
                <td className="whitespace-nowrap px-4 py-3 text-slate-600">{formatCoordinate(item.last_latitude)}</td>
                <td className="whitespace-nowrap px-4 py-3 text-slate-600">{formatCoordinate(item.last_longitude)}</td>
                <td className="whitespace-nowrap px-4 py-3 text-slate-600">{formatDate(item.last_update_at)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
