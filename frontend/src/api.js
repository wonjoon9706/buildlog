const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api'

export class ApiError extends Error {
  constructor(message, status) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  })

  const data = await response.json().catch(() => null)

  if (!response.ok) {
    const message =
      typeof data?.detail === 'string'
        ? data.detail
        : '요청을 처리하지 못했습니다. 잠시 후 다시 시도해주세요.'
    throw new ApiError(message, response.status)
  }

  return data
}

export function registerAccount(email, password) {
  return request('/auth/register', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  })
}

export function loginAccount(email, password) {
  return request('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  })
}

export function logoutAccount() {
  return request('/auth/logout', { method: 'POST' })
}

export function getCurrentUser() {
  return request('/auth/me')
}
