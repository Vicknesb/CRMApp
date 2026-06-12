import { render, screen } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { describe, it, expect, vi } from 'vitest'
import { ProtectedRoute } from './ProtectedRoute'
import * as useAuthModule from '../hooks/useAuth'

vi.mock('../hooks/useAuth', async (importOriginal) => {
  const orig = await importOriginal<typeof useAuthModule>()
  return { ...orig, useAuth: vi.fn() }
})

describe('ProtectedRoute', () => {
  it('redirects to /login when not authenticated', () => {
    vi.mocked(useAuthModule.useAuth).mockReturnValue({
      user: null, isLoading: false,
      login: vi.fn(), logout: vi.fn(), refresh: vi.fn(),
    })
    render(
      <MemoryRouter initialEntries={['/dashboard']}>
        <Routes>
          <Route element={<ProtectedRoute />}>
            <Route path="/dashboard" element={<div>Protected</div>} />
          </Route>
          <Route path="/login" element={<div>Login Page</div>} />
        </Routes>
      </MemoryRouter>,
    )
    expect(screen.getByText('Login Page')).toBeInTheDocument()
    expect(screen.queryByText('Protected')).not.toBeInTheDocument()
  })

  it('renders children when authenticated', () => {
    vi.mocked(useAuthModule.useAuth).mockReturnValue({
      user: { id: '1', email: 'a@b.com', firstName: 'A', lastName: 'B', role: 'ADMIN' },
      isLoading: false,
      login: vi.fn(), logout: vi.fn(), refresh: vi.fn(),
    })
    render(
      <MemoryRouter initialEntries={['/dashboard']}>
        <Routes>
          <Route element={<ProtectedRoute />}>
            <Route path="/dashboard" element={<div>Protected</div>} />
          </Route>
        </Routes>
      </MemoryRouter>,
    )
    expect(screen.getByText('Protected')).toBeInTheDocument()
  })
})
