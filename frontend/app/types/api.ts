/**
 * app/types/api.ts
 * -----------------
 * Interfaces pour les réponses de l'API.
 */

export interface ApiResponse<T> {
  data: T
  message?: string
}

export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

export interface AuthResponse {
  token: string
  user_uuid: string
  username: string
}
