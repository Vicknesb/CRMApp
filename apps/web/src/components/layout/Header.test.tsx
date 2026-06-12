import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { describe, it, expect } from 'vitest'
import { Header } from './Header'

describe('Header', () => {
  it('renders bell and avatar links', () => {
    render(
      <MemoryRouter>
        <Header title="Test" />
      </MemoryRouter>,
    )
    expect(screen.getByLabelText('Notifications')).toBeInTheDocument()
    expect(screen.getByLabelText('Profile')).toBeInTheDocument()
  })

  it('renders title when provided', () => {
    render(
      <MemoryRouter>
        <Header title="Dashboard" />
      </MemoryRouter>,
    )
    expect(screen.getByText('Dashboard')).toBeInTheDocument()
  })
})
