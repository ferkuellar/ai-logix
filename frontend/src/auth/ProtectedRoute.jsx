import Login from '../pages/Login'
import { useAuth } from './useAuth'

export default function ProtectedRoute({ children }) {
  const { isAuthenticated } = useAuth()
  return isAuthenticated ? children : <Login />
}
