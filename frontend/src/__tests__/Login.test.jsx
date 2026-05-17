import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import Login from '../pages/Login'
import { AuthProvider } from '../auth/AuthContext.jsx'
import { fetchCurrentUser, loginRequest } from '../api/client'

vi.mock('../api/client', async () => {
  const actual = await vi.importActual('../api/client')
  return {
    ...actual,
    fetchCurrentUser: vi.fn(),
    loginRequest: vi.fn(),
  }
})

function renderLogin() {
  return render(
    <AuthProvider>
      <Login />
    </AuthProvider>,
  )
}

beforeEach(() => {
  window.localStorage.clear()
  vi.clearAllMocks()
})

describe('Login', () => {
  it('allows typing credentials', async () => {
    const user = userEvent.setup()
    renderLogin()

    const email = screen.getByLabelText(/email/i)
    const password = screen.getByLabelText(/password/i)

    await user.clear(email)
    await user.type(email, 'supervisor@example.com')
    await user.type(password, 'Password123!')

    expect(email).toHaveValue('supervisor@example.com')
    expect(password).toHaveValue('Password123!')
  })

  it('persists token and user after successful login', async () => {
    const user = userEvent.setup()
    loginRequest.mockResolvedValue({ access_token: 'new-token', token_type: 'bearer' })
    fetchCurrentUser.mockResolvedValue({
      email: 'admin@example.com',
      full_name: 'Admin User',
      role: 'ADMIN',
      driver_id: null,
    })
    renderLogin()

    await user.type(screen.getByLabelText(/password/i), 'Password123!')
    await user.click(screen.getByRole('button', { name: /ingresar/i }))

    await waitFor(() => expect(loginRequest).toHaveBeenCalled())
    expect(loginRequest).toHaveBeenCalledWith({
      email: 'admin@ailogix.local',
      password: 'Password123!',
    })
    expect(window.localStorage.getItem('ailogix_token')).toBe('new-token')
    expect(JSON.parse(window.localStorage.getItem('ailogix_user')).role).toBe('ADMIN')
  })

  it('shows API error message after failed login', async () => {
    const user = userEvent.setup()
    loginRequest.mockRejectedValue({ response: { data: { detail: 'Invalid email or password.' } } })
    renderLogin()

    await user.type(screen.getByLabelText(/password/i), 'bad-password')
    await user.click(screen.getByRole('button', { name: /ingresar/i }))

    expect(await screen.findByText('Invalid email or password.')).toBeInTheDocument()
  })
})
