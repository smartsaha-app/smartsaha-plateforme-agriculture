/**
 * app/types/models.ts
 * --------------------
 * Interfaces TypeScript pour les modèles de données.
 */

export interface User {
  uuid: string
  username: string
  email: string
  first_name?: string
  last_name?: string
  avatar?: string
}

export interface Parcel {
  uuid: string
  parcel_name: string
  owner: string
  points: { lat: number; lng: number }[]
  area?: number
  created_at: string
  updated_at: string
}

export interface Crop {
  uuid: string
  name: string
  variety?: string
  description?: string
}

export interface Task {
  uuid: string
  title: string
  description?: string
  status: 'pending' | 'in_progress' | 'completed'
  priority: 'low' | 'medium' | 'high'
  due_date?: string
  parcel?: string
}

export interface YieldRecord {
  uuid: string
  parcel: string
  crop: string
  yield_amount: number
  date: string
}
