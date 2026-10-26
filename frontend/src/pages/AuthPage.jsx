import { useState } from 'react'
import { Link, Navigate, useNavigate } from 'react-router-dom'
import useAuth from '../useAuth'

export default function AuthPage({ mode }) {
  const isRegister = mode === 'register'
  const { user, isLoading, login, register } = useAuth()
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [errorMessage, setErrorMessage] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  if (!isLoading && user) {
    return <Navigate to="/" replace />
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setErrorMessage('')

    if (password.length < 8) {
      setErrorMessage('비밀번호는 8자 이상 입력해주세요.')
      return
    }

    setIsSubmitting(true)
    try {
      if (isRegister) {
        await register(email, password)
      } else {
        await login(email, password)
      }
      navigate('/', { replace: true })
    } catch (error) {
      setErrorMessage(error.message)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <main className="auth-page">
      <section className="auth-card">
        <Link className="brand" to="/">
          BuildLog
        </Link>
        <p className="eyebrow">{isRegister ? '처음 오셨나요?' : '다시 만나서 반가워요'}</p>
        <h1>{isRegister ? '회원 가입' : '로그인'}</h1>
        <p className="auth-description">
          {isRegister
            ? '계정을 만들고 공부 기록을 한곳에서 관리하세요.'
            : '가입한 계정으로 내 기록을 이어서 확인하세요.'}
        </p>

        <form className="auth-form" onSubmit={handleSubmit}>
          <label>
            이메일
            <input
              autoComplete="email"
              name="email"
              onChange={(event) => setEmail(event.target.value)}
              placeholder="name@example.com"
              required
              type="email"
              value={email}
            />
          </label>
          <label>
            비밀번호
            <input
              autoComplete={isRegister ? 'new-password' : 'current-password'}
              minLength={8}
              name="password"
              onChange={(event) => setPassword(event.target.value)}
              placeholder="8자 이상 입력"
              required
              type="password"
              value={password}
            />
          </label>

          {errorMessage && (
            <p className="form-message form-message--error" role="alert">
              {errorMessage}
            </p>
          )}

          <button className="primary-button" disabled={isSubmitting} type="submit">
            {isSubmitting ? '처리 중...' : isRegister ? '가입하기' : '로그인'}
          </button>
        </form>

        <p className="auth-switch">
          {isRegister ? '이미 계정이 있나요?' : '아직 계정이 없나요?'}{' '}
          <Link to={isRegister ? '/login' : '/signup'}>
            {isRegister ? '로그인' : '회원 가입'}
          </Link>
        </p>
      </section>
    </main>
  )
}
