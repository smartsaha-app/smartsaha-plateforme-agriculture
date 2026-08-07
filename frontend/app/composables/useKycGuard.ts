import { ref, computed } from 'vue'
import { useAuthStore } from '~/stores/auth'

// Singleton partagé entre tous les composants
const kycModalOpen = ref(false)

export const useKycGuard = () => {
  const authStore = useAuthStore()
  const kycStatus = computed(() => authStore.kycStatus)

  function requireKyc(): boolean {
    console.log('kycStatus:', JSON.stringify(kycStatus.value))
    if (kycStatus.value === 'APPROVED') {
      kycModalOpen.value = false
      return true
    }

    kycModalOpen.value = true
    return false
  }

  function closeKycModal() {
    kycModalOpen.value = false
  }

  return { kycModalOpen, kycStatus, requireKyc, closeKycModal }
}
