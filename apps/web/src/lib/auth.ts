import { apiClient } from './apiClient'

export interface AuthUser {
  id: string
  email: string
  firstName: string
  lastName: string
  role: string
  requires2FA?: boolean
}

export const authApi = {
  login: (email: string, password: string, totpCode?: string) =>
    apiClient.post<AuthUser>('/auth/login', { email, password, totpCode }),

  register: (data: { email: string; password: string; firstName: string; lastName: string }) =>
    apiClient.post<AuthUser>('/auth/register', data),

  logout: () => apiClient.post<{ message: string }>('/auth/logout'),

  session: () => apiClient.get<AuthUser>('/auth/session'),

  setup2FA: () => apiClient.post<{ secret: string; otpauthUrl: string; qrCodeUrl: string }>('/auth/2fa/setup'),

  verify2FA: (code: string) => apiClient.post<{ enabled: boolean }>('/auth/2fa/verify', { code }),

  requestPasswordReset: (email: string) =>
    apiClient.post<{ message: string }>('/auth/password-reset/request', { email }),

  confirmPasswordReset: (token: string, newPassword: string) =>
    apiClient.post<{ message: string }>('/auth/password-reset/confirm', { token, newPassword }),
}
