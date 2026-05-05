import { useEffect, useState } from 'react'
import { fetchOrderStates } from '../api/client'
import DashboardCards from '../components/DashboardCards'
import OperationsMap from '../components/OperationsMap'
import OrderStatesTable from '../components/OrderStatesTable'

export default function Dashboard({ refreshKey = 0 }) {
  const [orderStates, setOrderStates] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let active = true

    async function loadOrderStates() {
      try {
        setLoading(true)
        setError('')
        const data = await fetchOrderStates()

        if (active) {
          setOrderStates(data)
        }
      } catch (requestError) {
        if (active) {
          setError(requestError.response?.data?.detail || requestError.message || 'No se pudo cargar la operacion.')
        }
      } finally {
        if (active) {
          setLoading(false)
        }
      }
    }

    loadOrderStates()

    return () => {
      active = false
    }
  }, [refreshKey])

  return (
    <main className="mx-auto flex w-full max-w-7xl flex-1 flex-col gap-5 px-4 py-5 sm:px-6 lg:px-8">
      <div className="flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-sm font-medium uppercase text-slate-500">AI Logix</p>
          <h1 className="text-2xl font-semibold tracking-normal text-ink sm:text-3xl">Operacion de entregas OXXO</h1>
        </div>
        <p className="text-sm text-muted">Lectura en vivo desde /api/order-states</p>
      </div>

      {loading && (
        <div className="rounded-lg border border-slate-200 bg-white p-6 text-sm text-muted shadow-sm">
          Cargando estado operativo...
        </div>
      )}

      {!loading && error && (
        <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm font-medium text-red-700">
          {error}
        </div>
      )}

      {!loading && !error && (
        <>
          <DashboardCards orderStates={orderStates} />
          <OperationsMap orderStates={orderStates} />
          <section className="space-y-3">
            <div>
              <h2 className="text-base font-semibold text-ink">Pedidos recibidos</h2>
              <p className="text-sm text-muted">Tabla base para auditoria operativa.</p>
            </div>
            <OrderStatesTable orderStates={orderStates} />
          </section>
        </>
      )}
    </main>
  )
}
