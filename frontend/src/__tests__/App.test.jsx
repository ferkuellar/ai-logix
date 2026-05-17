import { render, screen, waitFor } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import App from '../App'
import { AuthProvider } from '../auth/AuthContext.jsx'
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

function renderApp() {
  return render(
    <AuthProvider>
      <App />
    </AuthProvider>,
  )
}

beforeEach(() => {
  window.localStorage.clear()
  window.history.pushState({}, '', '/')
  vi.clearAllMocks()
})

describe('App', () => {
  it('renders the login form without an authenticated session', () => {
    renderApp()

    expect(screen.getByRole('heading', { name: /ingresar a ai logix/i })).toBeInTheDocument()
  })

  it('renders the authenticated dashboard shell and loads order states', async () => {
    window.localStorage.setItem('ailogix_token', 'test-token')
    window.localStorage.setItem(
      'ailogix_user',
      JSON.stringify({ email: 'admin@example.com', full_name: 'Admin User', role: 'ADMIN' }),
    )
    fetchOrderStates.mockResolvedValue([
      {
        id: 'state-1',
        order_number: 'ORD-1',
        current_status: 'DELIVERED',
        last_latitude: 25.6866,
        last_longitude: -100.3161,
        last_update_at: '2026-05-17T12:00:00Z',
      },
    ])

    renderApp()

    expect(screen.getByText('Panel operativo')).toBeInTheDocument()
    await waitFor(() => expect(fetchOrderStates).toHaveBeenCalledTimes(1))
    expect((await screen.findAllByText('ORD-1')).length).toBeGreaterThan(0)
  })

  it('clears session and shows login when unauthorized event is dispatched', async () => {
    window.localStorage.setItem('ailogix_token', 'test-token')
    window.localStorage.setItem(
      'ailogix_user',
      JSON.stringify({ email: 'admin@example.com', full_name: 'Admin User', role: 'ADMIN' }),
    )
    fetchOrderStates.mockResolvedValue([])

    renderApp()
    window.dispatchEvent(new Event('ailogix:unauthorized'))

    await waitFor(() => expect(window.localStorage.getItem('ailogix_token')).toBeNull())
    expect(screen.getByRole('heading', { name: /ingresar a ai logix/i })).toBeInTheDocument()
  })
})
