import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import useAuth from '../useAuth'

export default function DashboardPage() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [errorMessage, setErrorMessage] = useState('')
  const [isLoggingOut, setIsLoggingOut] = useState(false)

  async function handleLogout() {
    setErrorMessage('')
    setIsLoggingOut(true)
    try {
      await logout()
      navigate('/login', { replace: true })
    } catch (error) {
      setErrorMessage(error.message)
    } finally {
      setIsLoggingOut(false)
    }
  }

  return (
    <main className="dashboard-page">
      <header className="dashboard-header">
        <span className="brand">BuildLog</span>
        <button className="secondary-button" disabled={isLoggingOut} onClick={handleLogout}>
          {isLoggingOut ? '로그아웃 중...' : '로그아웃'}
        </button>
      </header>

      <section className="dashboard-card">
        <p className="eyebrow">로그인 완료</p>
        <h1>안녕하세요.</h1>
        <p className="dashboard-email">{user.email}</p>
        <p className="dashboard-description">
          회원 가입과 로그인 기능이 준비되었습니다. 다음 Phase에서 공통 메뉴와 기록 화면을
          연결합니다.
        </p>
        {errorMessage && (
          <p className="form-message form-message--error" role="alert">
            {errorMessage}
          </p>
        )}
      </section>
    </main>
  )
}
