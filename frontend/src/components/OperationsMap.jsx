import { CircleMarker, MapContainer, Popup, TileLayer } from 'react-leaflet'
import { getStatusColor, getStatusLabel, hasValidCoordinates } from '../utils/status'

const defaultCenter = [25.6866, -100.3161]

export default function OperationsMap({ orderStates }) {
  const points = orderStates.filter(hasValidCoordinates)
  const center = points.length > 0 ? [Number(points[0].last_latitude), Number(points[0].last_longitude)] : defaultCenter

  return (
    <section className="overflow-hidden rounded-lg border border-slate-200 bg-white shadow-sm">
      <div className="flex flex-col gap-1 border-b border-slate-200 px-4 py-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 className="text-base font-semibold text-ink">Mapa operativo</h2>
          <p className="text-sm text-muted">{points.length} pedidos con coordenadas</p>
        </div>
        <div className="flex flex-wrap gap-2 text-xs text-slate-600">
          <span className="inline-flex items-center gap-1"><span className="h-2.5 w-2.5 rounded-full bg-green-600" /> Surtido</span>
          <span className="inline-flex items-center gap-1"><span className="h-2.5 w-2.5 rounded-full bg-amber-500" /> Pendiente</span>
          <span className="inline-flex items-center gap-1"><span className="h-2.5 w-2.5 rounded-full bg-red-600" /> No atendido</span>
        </div>
      </div>

      {points.length === 0 ? (
        <div className="flex h-[340px] items-center justify-center bg-slate-50 px-6 text-center text-sm text-muted md:h-[460px]">
          No hay pedidos con coordenadas para mostrar en el mapa.
        </div>
      ) : (
        <MapContainer center={center} zoom={12} scrollWheelZoom className="h-[340px] w-full md:h-[460px]">
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          {points.map((item) => {
            const color = getStatusColor(item.current_status)

            return (
              <CircleMarker
                key={item.id || item.order_number}
                center={[Number(item.last_latitude), Number(item.last_longitude)]}
                radius={9}
                pathOptions={{ color, fillColor: color, fillOpacity: 0.78, weight: 2 }}
              >
                <Popup>
                  <div className="space-y-1 text-sm">
                    <p className="font-semibold text-slate-900">{item.order_number}</p>
                    <p>Estado: {getStatusLabel(item.current_status)}</p>
                    <p>Lat: {Number(item.last_latitude).toFixed(6)}</p>
                    <p>Lng: {Number(item.last_longitude).toFixed(6)}</p>
                  </div>
                </Popup>
              </CircleMarker>
            )
          })}
        </MapContainer>
      )}
    </section>
  )
}
