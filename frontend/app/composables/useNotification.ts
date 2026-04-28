/**
 * apps/composables/useNotification.ts
 * ------------------------------------
 * Système de notification unifié pour l'application.
 */
import { ref } from 'vue'

export type NotificationType = 'success' | 'error' | 'warning' | 'info'

interface Notification {
  message: string
  type: NotificationType
  id: number
}

const notifications = ref<Notification[]>([])
let nextId = 0

export const useNotification = () => {
  const show = (message: string, type: NotificationType = 'info', timeout = 5000) => {
    const id = nextId++
    notifications.value.push({ id, message, type })
    
    // Auto-suppression après le timeout
    setTimeout(() => {
      remove(id)
    }, timeout)
  }

  const showSuccess = (message: string) => show(message, 'success')
  const showError = (message: string) => show(message, 'error')
  const showWarning = (message: string) => show(message, 'warning')
  const showInfo = (message: string) => show(message, 'info')

  const remove = (id: number) => {
    notifications.value = notifications.value.filter(n => n.id !== id)
  }

  return {
    notifications,
    showSuccess,
    showError,
    showWarning,
    showInfo,
    remove
  }
}
