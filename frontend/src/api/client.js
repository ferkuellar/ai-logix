import axios from 'axios'

const fallbackBaseUrl = 'http://localhost:8000/api'
const apiBaseUrl = (import.meta.env.VITE_API_BASE_URL || fallbackBaseUrl).replace(/\/$/, '')
const publicBaseUrl = apiBaseUrl.replace(/\/api$/, '')

export const apiClient = axios.create({
  baseURL: apiBaseUrl,
  timeout: 10000,
})

apiClient.interceptors.request.use((config) => {
  const token = window.localStorage.getItem('ailogix_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      window.dispatchEvent(new Event('ailogix:unauthorized'))
    }
    return Promise.reject(error)
  },
)

export async function loginRequest(credentials) {
  const response = await apiClient.post('/auth/login', credentials)
  return response.data
}

export async function fetchCurrentUser() {
  const response = await apiClient.get('/auth/me')
  return response.data
}

export async function fetchUsers() {
  const response = await apiClient.get('/users')
  return Array.isArray(response.data) ? response.data : []
}

export async function createUser(payload) {
  const response = await apiClient.post('/users', payload)
  return response.data
}

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

export async function fetchPendingReviews(params = {}) {
  const response = await apiClient.get('/review/pending', { params })
  return Array.isArray(response.data) ? response.data : []
}

export async function fetchReviewDetail(eventId) {
  const response = await apiClient.get(`/review/${eventId}`)
  return response.data
}

export async function confirmHumanReview(eventId, payload) {
  const response = await apiClient.post(`/review/${eventId}/confirm`, payload)
  return response.data
}

export async function rejectHumanReview(eventId, payload) {
  const response = await apiClient.post(`/review/${eventId}/reject`, payload)
  return response.data
}

export function buildPublicUrl(path) {
  if (!path) return ''
  if (/^https?:\/\//i.test(path)) return path
  return `${publicBaseUrl}${path.startsWith('/') ? path : `/${path}`}`
}
