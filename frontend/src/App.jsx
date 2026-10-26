import { useEffect, useState } from 'react'
import { Navigate, Route, Routes } from 'react-router-dom'
import './App.css'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api'

function SetupPage() {
  const [apiStatus, setApiStatus] = useState('checking')

  useEffect(() => {
    const controller = new AbortController()

    async function checkApi() {
      try {
        const response = await fetch(`${API_BASE_URL}/health`, {
          signal: controller.signal,
        })

        if (!response.ok) {
          throw new Error('API health check failed')
        }

        setApiStatus('connected')
      } catch (error) {
        if (error.name !== 'AbortError') {
          setApiStatus('disconnected')
        }
      }
    }

    checkApi()

    return () => controller.abort()
  }, [])

  const statusText = {
    checking: 'FastAPI 연결 확인 중',
    connected: 'FastAPI 연결됨',
    disconnected: 'FastAPI가 실행되지 않았습니다',
  }[apiStatus]

  return (
    <main className="setup-page">
      <section className="setup-card">
        <span className="eyebrow">BUILDLOG · PHASE 1</span>
        <h1>공부의 과정을 한곳에 기록하세요.</h1>
        <p className="description">
          React 화면이 준비되었습니다. 다음 단계에서 로그인과 학습 기록 기능을
          차례로 연결합니다.
        </p>

        <div className={`status status--${apiStatus}`} role="status">
          <span className="status__dot" aria-hidden="true" />
          <span>{statusText}</span>
        </div>

        <dl className="stack-list">
          <div>
            <dt>프론트엔드</dt>
            <dd>React + Vite</dd>
          </div>
          <div>
            <dt>백엔드</dt>
            <dd>FastAPI</dd>
          </div>
          <div>
            <dt>데이터</dt>
            <dd>Supabase · 테스트 SQLite3</dd>
          </div>
        </dl>
      </section>
    </main>
  )
}

function App() {
  return (
    <Routes>
      <Route path="/" element={<SetupPage />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

export default App
