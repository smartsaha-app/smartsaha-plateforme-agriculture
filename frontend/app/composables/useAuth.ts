/**
 * apps/composables/useAuth.ts
 */
import { useAuthStore } from '~/stores/auth'

export const useAuth = () => {
  const authStore = useAuthStore()
  const localePath = useLocalePath()

  const token = computed(() => authStore.token)
  const uuid  = computed(() => authStore.uuid)
  const isAuthenticated = computed(() => authStore.isAuthenticated)

  const logout = () => {
    authStore.clearUserData()      // nettoie localStorage + store
    navigateTo(localePath('/login'))  // navigateTo au lieu de router.push
  }

  return {
    token,
    uuid,
    isAuthenticated,
    logout
  }
}