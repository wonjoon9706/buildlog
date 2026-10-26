import { useEffect, useMemo, useState } from 'react'
import {
  ApiError,
  getCurrentUser,
  loginAccount,
  logoutAccount,
  registerAccount,
} from './api'
import AuthContext from './auth-context'

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    async function loadUser() {
      try {
        const currentUser = await getCurrentUser()
        setUser(currentUser)
      } catch (error) {
        if (!(error instanceof ApiError) || error.status !== 401) {
          console.error('사용자 정보를 불러오지 못했습니다.', error)
        }
        setUser(null)
      } finally {
        setIsLoading(false)
      }
    }

    loadUser()
  }, [])

  const value = useMemo(
    () => ({
      user,
      isLoading,
      async register(email, password) {
        const result = await registerAccount(email, password)
        setUser(result.user)
        return result
      },
      async login(email, password) {
        const result = await loginAccount(email, password)
        setUser(result.user)
        return result
      },
      async logout() {
        await logoutAccount()
        setUser(null)
      },
    }),
    [isLoading, user],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
