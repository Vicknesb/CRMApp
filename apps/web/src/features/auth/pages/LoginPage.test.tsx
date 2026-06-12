import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { LoginPage } from './LoginPage'
import { AuthProvider } from '../hooks/useAuth'
import * as authLib from '../../../lib/auth'

vi.mock('../../../lib/auth', () => ({
  authApi: {
    session: vi.fn().mockRejectedValue(new Error('no session')),
    login: vi.fn(),
    logout: vi.fn(),
  },
}))

function renderLoginPage() {
  return render(
    <MemoryRouter>
      <AuthProvider>
        <LoginPage />
      </AuthProvider>
    </MemoryRouter>,
  )
}

describe('LoginPage', () => {
  it('renders email and password fields', async () => {
    renderLoginPage()
    expect(screen.getByPlaceholderText('you@ideas2it.com')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('••••••••')).toBeInTheDocument()
  })

  it('shows validation error for invalid email', async () => {
    renderLoginPage()
    fireEvent.click(screen.getByRole('button', { name: /sign in/i }))
    await waitFor(() => {
      expect(screen.getByText('Invalid email')).toBeInTheDocument()
    })
  })

  it('shows 2FA prompt when requires2FA is true', async () => {
    vi.mocked(authLib.authApi.login).mockResolvedValueOnce({
      id: '1', email: 'a@b.com', firstName: 'A', lastName: 'B',
      role: 'SALES_REP', requires2FA: true,
    })
    renderLoginPage()
    fireEvent.change(screen.getByPlaceholderText('you@ideas2it.com'), { target: { value: 'a@b.com' } })
    fireEvent.change(screen.getByPlaceholderText('••••••••'), { target: { value: 'Password1' } })
    fireEvent.click(screen.getByRole('button', { name: /sign in/i }))
    await waitFor(() => {
      expect(screen.getByPlaceholderText('000000')).toBeInTheDocument()
    })
  })
})
