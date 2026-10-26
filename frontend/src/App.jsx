import { Navigate, Route, Routes } from 'react-router-dom'
import './App.css'
import { AuthProvider } from './AuthContext'
import ProtectedRoute from './ProtectedRoute'
import AuthPage from './pages/AuthPage'
import DashboardPage from './pages/DashboardPage'

function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route element={<ProtectedRoute />}>
          <Route path="/" element={<DashboardPage />} />
        </Route>
        <Route path="/login" element={<AuthPage mode="login" />} />
        <Route path="/signup" element={<AuthPage mode="register" />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </AuthProvider>
  )
}

export default App
