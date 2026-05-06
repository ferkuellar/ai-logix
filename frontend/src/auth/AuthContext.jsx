import { useCallback, useEffect, useMemo, useState } from 'react'
import { fetchCurrentUser, loginRequest } from '../api/client'
import { AuthContext } from './authContext'

function readStoredAuth() {
  const token = window.localStorage.getItem('ailogix_token') || ''
  const userRaw = window.localStorage.getItem('ailogix_user')

  if (!userRaw) {
    return { token, user: null }
  }

  try {
    return { token, user: JSON.parse(userRaw) }
  } catch {
    return { token, user: null }
  }
}

export function AuthProvider({ children }) {
  const initialAuth = readStoredAuth()
  const [token, setToken] = useState(initialAuth.token)
  const [user, setUser] = useState(initialAuth.user)

  const persistSession = useCallback((nextToken, nextUser) => {
    window.localStorage.setItem('ailogix_token', nextToken)
    window.localStorage.setItem('ailogix_user', JSON.stringify(nextUser))
    setToken(nextToken)
    setUser(nextUser)
  }, [])

  const logout = useCallback(() => {
    window.localStorage.removeItem('ailogix_token')
    window.localStorage.removeItem('ailogix_user')
    setToken('')
    setUser(null)
  }, [])

  const login = useCallback(async (credentials) => {
    const tokenResponse = await loginRequest(credentials)
    window.localStorage.setItem('ailogix_token', tokenResponse.access_token)
    const currentUser = await fetchCurrentUser()
    persistSession(tokenResponse.access_token, currentUser)
    return currentUser
  }, [persistSession])

  const hasRole = useCallback((roles) => {
    const allowed = Array.isArray(roles) ? roles : [roles]
    return Boolean(user?.role && allowed.includes(user.role))
  }, [user])

  useEffect(() => {
    function handleUnauthorized() {
      logout()
    }

    window.addEventListener('ailogix:unauthorized', handleUnauthorized)
    return () => window.removeEventListener('ailogix:unauthorized', handleUnauthorized)
  }, [logout])

  const value = useMemo(() => ({
    token,
    user,
    login,
    logout,
    hasRole,
    isAuthenticated: Boolean(token && user),
  }), [hasRole, login, logout, token, user])

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
