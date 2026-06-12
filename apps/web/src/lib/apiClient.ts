import axios, { type AxiosRequestConfig } from 'axios'

export interface ApiResponse<T> {
  data: T | null
  error: { message: string; details?: unknown } | null
  meta: Record<string, unknown>
}

const instance = axios.create({
  baseURL: '/api',
  withCredentials: true,
  headers: { 'Content-Type': 'application/json' },
})

async function request<T>(config: AxiosRequestConfig): Promise<T> {
  const res = await instance.request<ApiResponse<T>>(config)
  const body = res.data
  if (body.error) {
    const msg = body.error.message ?? 'Unknown error'
    throw Object.assign(new Error(msg), { details: body.error.details, status: res.status })
  }
  return body.data as T
}

export const apiClient = {
  get: <T>(url: string, config?: AxiosRequestConfig) =>
    request<T>({ ...config, method: 'GET', url }),
  post: <T>(url: string, data?: unknown, config?: AxiosRequestConfig) =>
    request<T>({ ...config, method: 'POST', url, data }),
  put: <T>(url: string, data?: unknown, config?: AxiosRequestConfig) =>
    request<T>({ ...config, method: 'PUT', url, data }),
  patch: <T>(url: string, data?: unknown, config?: AxiosRequestConfig) =>
    request<T>({ ...config, method: 'PATCH', url, data }),
  delete: <T>(url: string, config?: AxiosRequestConfig) =>
    request<T>({ ...config, method: 'DELETE', url }),
}
