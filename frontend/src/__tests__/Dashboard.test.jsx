import { render, screen } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import Dashboard from '../pages/Dashboard'
import { fetchOrderStates } from '../api/client'

vi.mock('../api/client', async () => {
  const actual = await vi.importActual('../api/client')
  return {
    ...actual,
    fetchOrderStates: vi.fn(),
  }
})

vi.mock('react-leaflet', () => ({
  CircleMarker: ({ children }) => <div data-testid="circle-marker">{children}</div>,
  MapContainer: ({ children }) => <div data-testid="map">{children}</div>,
  Popup: ({ children }) => <div>{children}</div>,
  TileLayer: () => <div data-testid="tile-layer" />,
}))

beforeEach(() => {
  vi.clearAllMocks()
})

describe('Dashboard', () => {
  it('renders order states returned by the API', async () => {
    fetchOrderStates.mockResolvedValue([
      {
        id: 'state-1',
        order_number: 'ORD-DASH-1',
        current_status: 'DELIVERED',
        last_latitude: 25.6866,
        last_longitude: -100.3161,
        last_update_at: '2026-05-17T12:00:00Z',
      },
    ])

    render(<Dashboard />)

    expect((await screen.findAllByText('ORD-DASH-1')).length).toBeGreaterThan(0)
    expect(screen.getByText('Pedidos recibidos')).toBeInTheDocument()
  })

  it('renders an error when order state API fails', async () => {
    fetchOrderStates.mockRejectedValue(new Error('API unavailable'))

    render(<Dashboard />)

    expect(await screen.findByText('API unavailable')).toBeInTheDocument()
  })
})
