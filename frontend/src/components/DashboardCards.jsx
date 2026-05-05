import { buildKpis } from '../utils/status'

const cardConfig = [
  { key: 'total', label: 'Total de pedidos', tone: 'border-slate-200' },
  { key: 'delivered', label: 'Surtidos', tone: 'border-green-200' },
  { key: 'pending', label: 'Pendientes', tone: 'border-amber-200' },
  { key: 'unattended', label: 'No atendidos', tone: 'border-red-200' },
]

export default function DashboardCards({ orderStates }) {
  const kpis = buildKpis(orderStates)

  return (
    <section className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
      {cardConfig.map((card) => (
        <article key={card.key} className={`rounded-lg border ${card.tone} bg-panel p-4 shadow-sm`}>
          <p className="text-sm font-medium text-muted">{card.label}</p>
          <p className="mt-3 text-3xl font-semibold tracking-normal text-ink">{kpis[card.key]}</p>
        </article>
      ))}
    </section>
  )
}
