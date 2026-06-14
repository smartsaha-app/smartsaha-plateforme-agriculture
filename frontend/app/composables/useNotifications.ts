import { useState } from '#app'
import { useApi } from '~/composables/useApi'

export interface Notification {
  uuid: string
  notification_type: string
  title: string
  body: string
  is_read: boolean
  data: Record<string, any> | null
  created_at: string
}

export function useNotifications() {
  const notifications    = useState<Notification[]>('notifications', () => [])
  const unreadNotifCount = useState<number>('unreadNotifCount', () => 0)
  const loadingNotifs    = useState<boolean>('loadingNotifs', () => false)

  const { apiFetch } = useApi()

  async function fetchNotifications() {
    loadingNotifs.value = true
    try {
      const data = await apiFetch<Notification[]>('/api/notifications/')
      notifications.value    = data ?? []
      unreadNotifCount.value = notifications.value.filter(n => !n.is_read).length
    } catch (_) {
      // silently ignore — badge stays at last known value
    } finally {
      loadingNotifs.value = false
    }
  }

  async function markAsRead(uuid: string) {
    try {
      await apiFetch(`/api/notifications/${uuid}/mark_as_read/`, { method: 'POST' })
      const notif = notifications.value.find(n => n.uuid === uuid)
      if (notif) notif.is_read = true
      unreadNotifCount.value = notifications.value.filter(n => !n.is_read).length
    } catch (_) {}
  }

  async function markAllAsRead() {
    try {
      await apiFetch('/api/notifications/mark_all_as_read/', { method: 'POST' })
      notifications.value.forEach(n => { n.is_read = true })
      unreadNotifCount.value = 0
    } catch (_) {}
  }

  return {
    notifications,
    unreadNotifCount,
    loadingNotifs,
    fetchNotifications,
    markAsRead,
    markAllAsRead,
  }
}
