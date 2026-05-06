import Unauthorized from '../pages/Unauthorized'
import { useAuth } from './useAuth'

export default function RoleRoute({ roles, children }) {
  const { hasRole } = useAuth()
  return hasRole(roles) ? children : <Unauthorized />
}
