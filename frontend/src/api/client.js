import axios from 'axios'

const fallbackBaseUrl = 'http://localhost:8000/api'
const apiBaseUrl = (import.meta.env.VITE_API_BASE_URL || fallbackBaseUrl).replace(/\/$/, '')
const publicBaseUrl = apiBaseUrl.replace(/\/api$/, '')

export const apiClient = axios.create({
  baseURL: apiBaseUrl,
  timeout: 10000,
})

export async function fetchOrderStates() {
  const response = await apiClient.get('/order-states')
  return Array.isArray(response.data) ? response.data : []
}

export async function uploadEvidence(formData) {
  const response = await apiClient.post('/evidence/upload', formData)
  return response.data
}

export async function processOcr(eventId) {
  const response = await apiClient.post(`/ocr/process/${eventId}`)
  return response.data
}

export async function fetchOcrResult(eventId) {
  const response = await apiClient.get(`/ocr/result/${eventId}`)
  return response.data
}

export async function confirmOcrResult(eventId, payload) {
  const response = await apiClient.post(`/ocr/confirm/${eventId}`, payload)
  return response.data
}

export function buildPublicUrl(path) {
  if (!path) return ''
  if (/^https?:\/\//i.test(path)) return path
  return `${publicBaseUrl}${path.startsWith('/') ? path : `/${path}`}`
}
