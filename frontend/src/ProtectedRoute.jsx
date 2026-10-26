import { Navigate, Outlet } from 'react-router-dom'
import useAuth from './useAuth'

export default function ProtectedRoute() {
  const { user, isLoading } = useAuth()

  if (isLoading) {
    return <div className="loading-page">로그인 상태를 확인하고 있습니다.</div>
  }

  if (!user) {
    return <Navigate to="/login" replace />
  }

  return <Outlet />
}
