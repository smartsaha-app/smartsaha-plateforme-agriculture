/**
 * apps/composables/useApi.ts
 */
import { useAuthStore } from '~/stores/auth'

export const useApi = () => {
  const config    = useRuntimeConfig()
  const authStore = useAuthStore()  // ← direct, plus besoin de useAuth

  // Relay cookies via useRequestHeaders pending SSR mapping
  const headers = process.server ? useRequestHeaders(['cookie']) : {}

  const apiFetch = async (path: string, opts: any = {}) => {
    const baseUrl = config.public.apiBase || 'http://127.0.0.1:8000'

    const response = await $fetch<any>(path, {
      baseURL: baseUrl,
      credentials: 'include',
      headers: {
        ...headers,
        ...opts.headers,
      },
      ...opts,
      async onResponseError({ response }: { response: any }) {
        if (response.status === 401) {
          authStore.clearUserData()
          await navigateTo('/login')
        }
      }
    })

    // Si on reçoit un objet de pagination { count, results, ... }
    // On peut renvoyer soit les résultats direct (compatibilité), soit l'objet complet.
    return response
  }

  return { apiFetch }
}