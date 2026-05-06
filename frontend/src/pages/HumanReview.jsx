import { useEffect, useState } from 'react'
import { confirmHumanReview, fetchPendingReviews, fetchReviewDetail, rejectHumanReview } from '../api/client'
import ReviewDetail from '../components/ReviewDetail'
import ReviewQueue from '../components/ReviewQueue'

export default function HumanReview({ onReviewComplete }) {
  const [items, setItems] = useState([])
  const [selectedEventId, setSelectedEventId] = useState('')
  const [detail, setDetail] = useState(null)
  const [queueLoading, setQueueLoading] = useState(true)
  const [detailLoading, setDetailLoading] = useState(false)
  const [queueError, setQueueError] = useState('')
  const [detailError, setDetailError] = useState('')
  const [submitting, setSubmitting] = useState('')
  const [message, setMessage] = useState('')

  async function refreshQueue(preferredEventId = '') {
    try {
      setQueueLoading(true)
      setQueueError('')
      const data = await fetchPendingReviews({ limit: 50 })
      setItems(data)

      const nextSelected = preferredEventId && data.some((item) => item.event_id === preferredEventId)
        ? preferredEventId
        : data[0]?.event_id || ''
      setSelectedEventId(nextSelected)
      return nextSelected
    } catch (requestError) {
      setQueueError(requestError.response?.data?.detail || requestError.message || 'No se pudo cargar la cola.')
      return ''
    } finally {
      setQueueLoading(false)
    }
  }

  async function refreshDetail(eventId) {
    if (!eventId) {
      setDetail(null)
      return
    }

    try {
      setDetailLoading(true)
      setDetailError('')
      const data = await fetchReviewDetail(eventId)
      setDetail(data)
    } catch (requestError) {
      setDetailError(requestError.response?.data?.detail || requestError.message || 'No se pudo cargar el detalle.')
    } finally {
      setDetailLoading(false)
    }
  }

  useEffect(() => {
    let active = true

    async function loadInitialQueue() {
      try {
        setQueueLoading(true)
        setQueueError('')
        const data = await fetchPendingReviews({ limit: 50 })

        if (!active) return

        setItems(data)
        setSelectedEventId(data[0]?.event_id || '')
      } catch (requestError) {
        if (active) {
          setQueueError(requestError.response?.data?.detail || requestError.message || 'No se pudo cargar la cola.')
        }
      } finally {
        if (active) {
          setQueueLoading(false)
        }
      }
    }

    loadInitialQueue()

    return () => {
      active = false
    }
  }, [])

  useEffect(() => {
    let active = true

    async function loadSelectedDetail() {
      if (!selectedEventId) {
        setDetail(null)
        return
      }

      try {
        setDetailLoading(true)
        setDetailError('')
        const data = await fetchReviewDetail(selectedEventId)

        if (active) {
          setDetail(data)
        }
      } catch (requestError) {
        if (active) {
          setDetailError(requestError.response?.data?.detail || requestError.message || 'No se pudo cargar el detalle.')
        }
      } finally {
        if (active) {
          setDetailLoading(false)
        }
      }
    }

    loadSelectedDetail()

    return () => {
      active = false
    }
  }, [selectedEventId])

  async function handleConfirm(payload) {
    try {
      setSubmitting('confirm')
      setMessage('')
      await confirmHumanReview(selectedEventId, payload)
      setMessage('Revision confirmada y estado operativo actualizado.')
      const nextSelected = await refreshQueue('')
      await refreshDetail(nextSelected)
      onReviewComplete?.()
    } catch (requestError) {
      setDetailError(requestError.response?.data?.detail || requestError.message || 'No se pudo confirmar la revision.')
    } finally {
      setSubmitting('')
    }
  }

  async function handleReject(payload) {
    try {
      setSubmitting('reject')
      setMessage('')
      await rejectHumanReview(selectedEventId, payload)
      setMessage('OCR rechazado. El pedido no fue marcado como entregado.')
      const nextSelected = await refreshQueue('')
      await refreshDetail(nextSelected)
      onReviewComplete?.()
    } catch (requestError) {
      setDetailError(requestError.response?.data?.detail || requestError.message || 'No se pudo rechazar la revision.')
    } finally {
      setSubmitting('')
    }
  }

  return (
    <main className="mx-auto flex w-full max-w-7xl flex-1 flex-col gap-5 px-4 py-5 sm:px-6 lg:px-8">
      <div className="flex flex-col gap-2">
        <p className="text-sm font-medium uppercase text-slate-500">Fase 5</p>
        <h1 className="text-2xl font-semibold tracking-normal text-ink sm:text-3xl">Revision humana de OCR</h1>
        <p className="max-w-3xl text-sm text-muted">
          Valida o corrige los datos sugeridos por OCR antes de convertirlos en informacion operativa confiable.
        </p>
      </div>

      <div className="grid gap-5 lg:grid-cols-[minmax(280px,0.38fr)_minmax(0,0.62fr)]">
        <ReviewQueue
          error={queueError}
          items={items}
          loading={queueLoading}
          onSelect={(eventId) => {
            setMessage('')
            setSelectedEventId(eventId)
          }}
          selectedEventId={selectedEventId}
        />
        <ReviewDetail
          detail={detail}
          error={detailError}
          loading={detailLoading}
          message={message}
          onConfirm={handleConfirm}
          onReject={handleReject}
          submitting={submitting}
        />
      </div>
    </main>
  )
}
