/**
 * app/stores/auth.ts
 */
import { defineStore } from 'pinia'
import { useStorage } from '@vueuse/core'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const loggedInCookie = useCookie('is_logged_in', { maxAge: 60 * 60 * 24 * 7 })
  const uuidCookie     = useCookie('user_uuid',    { maxAge: 60 * 60 * 24 * 7 })
  const spacesCookie   = useCookie<any>('user_spaces', { maxAge: 60 * 60 * 24 * 7 })

  const serverStore = useStorage('serverStore', {
    username:  null as string | null,
    groupInfo: null as any,
  })
  
  const isInitialized = ref(false)

  const uuid            = computed(() => uuidCookie.value)
  const username        = computed(() => serverStore.value.username)
  
  const isAuthenticated = computed(() => {
    return !!loggedInCookie.value
  })
  const groupInfo       = computed(() => serverStore.value.groupInfo)
  const isGroupMember   = computed(() => !!serverStore.value.groupInfo)
  const spaces          = computed(() => spacesCookie.value)

  const setUserData = (data: {
    uuid?:      string
    username?:  string
    groupInfo?: any
    spaces?:    any
  }) => {
    loggedInCookie.value = 'true'
    if (data.uuid)  uuidCookie.value     = data.uuid
    if (data.spaces) spacesCookie.value  = data.spaces
    serverStore.value = { ...serverStore.value, ...data }
  }

  const setInitialized = (value: boolean) => {
    isInitialized.value = value
  }

  const getWorkspacePath = () => {
    if (!spacesCookie.value) return '/farmer/dashboard'
    
    // Priorité aux espaces spécialisés
    if (spacesCookie.value.superviseur) return '/admin'
    if (spacesCookie.value.organisation) return '/organization/dashboard'
    if (spacesCookie.value.agriculture) return '/farmer/dashboard'
    
    return '/farmer/dashboard'
  }

  const clearUserData = async () => {
    if (loggedInCookie.value) {
      try {
        const config = useRuntimeConfig()
        const baseUrl = config.public.apiBase || 'http://127.0.0.1:8000'
        await $fetch('/api/logout/', {
          baseURL: baseUrl,
          method: 'POST',
          credentials: 'include'
        })
      } catch (e) {
        console.error('Logout failed on backend:', e)
      }
    }

    loggedInCookie.value = null
    uuidCookie.value     = null
    spacesCookie.value   = null
    serverStore.value = { username: null, groupInfo: null }
    if (process.client) {
      localStorage.removeItem('serverStore') // nettoyage explicite
    }
  }

  return {
    uuid,
    username,
    isAuthenticated,
    groupInfo,
    isGroupMember,
    spaces,
    setUserData,
    clearUserData,
    isInitialized,
    setInitialized,
    getWorkspacePath,
  }
})