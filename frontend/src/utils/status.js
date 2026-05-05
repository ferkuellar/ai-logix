export const STATUS_LABELS = {
  DELIVERED: 'Surtido',
  PARTIAL: 'Parcial',
  PENDING: 'Pendiente',
  FAILED: 'Fallido',
  CANCELLED: 'Cancelado',
}

export const STATUS_COLORS = {
  DELIVERED: '#16a34a',
  PARTIAL: '#f59e0b',
  PENDING: '#f59e0b',
  FAILED: '#dc2626',
  CANCELLED: '#dc2626',
}

export const STATUS_BADGE_CLASSES = {
  DELIVERED: 'bg-green-50 text-green-700 ring-green-600/20',
  PARTIAL: 'bg-amber-50 text-amber-700 ring-amber-600/20',
  PENDING: 'bg-amber-50 text-amber-700 ring-amber-600/20',
  FAILED: 'bg-red-50 text-red-700 ring-red-600/20',
  CANCELLED: 'bg-red-50 text-red-700 ring-red-600/20',
}

export function normalizeStatus(status) {
  return String(status || 'PENDING').toUpperCase()
}

export function getStatusLabel(status) {
  const normalized = normalizeStatus(status)
  return STATUS_LABELS[normalized] || normalized
}

export function getStatusColor(status) {
  return STATUS_COLORS[normalizeStatus(status)] || '#64748b'
}

export function getStatusBadgeClass(status) {
  return STATUS_BADGE_CLASSES[normalizeStatus(status)] || 'bg-slate-50 text-slate-700 ring-slate-600/20'
}

export function hasValidCoordinates(orderState) {
  return Number.isFinite(Number(orderState.last_latitude)) && Number.isFinite(Number(orderState.last_longitude))
}

export function buildKpis(orderStates) {
  const total = orderStates.length
  const delivered = orderStates.filter((item) => normalizeStatus(item.current_status) === 'DELIVERED').length
  const pending = orderStates.filter((item) => ['PENDING', 'PARTIAL'].includes(normalizeStatus(item.current_status))).length
  const unattended = orderStates.filter((item) => ['FAILED', 'CANCELLED'].includes(normalizeStatus(item.current_status))).length

  return { total, delivered, pending, unattended }
}
