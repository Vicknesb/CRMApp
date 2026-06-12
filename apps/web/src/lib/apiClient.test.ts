import { describe, it, expect, vi, beforeEach } from 'vitest'
import axios from 'axios'

vi.mock('axios', () => {
  const mockInstance = {
    request: vi.fn(),
    create: vi.fn(),
  }
  return {
    default: {
      create: vi.fn(() => mockInstance),
    },
    __mockInstance: mockInstance,
  }
})

describe('apiClient', () => {
  it('unwraps data from envelope', async () => {
    const { __mockInstance } = await import('axios') as any
    __mockInstance.request.mockResolvedValueOnce({
      data: { data: { id: 1 }, error: null, meta: {} },
      status: 200,
    })
    const { apiClient } = await import('./apiClient')
    const result = await apiClient.get('/test')
    expect(result).toEqual({ id: 1 })
  })

  it('throws normalized error when envelope has error', async () => {
    const { __mockInstance } = await import('axios') as any
    __mockInstance.request.mockResolvedValueOnce({
      data: { data: null, error: { message: 'Not found', details: null }, meta: {} },
      status: 404,
    })
    const { apiClient } = await import('./apiClient')
    await expect(apiClient.get('/test')).rejects.toThrow('Not found')
  })
})
