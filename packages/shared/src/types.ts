export interface ApiResponse<T> {
  data: T | null
  error: { message: string; details?: unknown } | null
  meta: Record<string, unknown>
}
