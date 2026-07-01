<template>
  <Teleport to="body">
    <Transition name="kyc-modal">
      <div v-if="kycModalOpen"
        class="fixed inset-0 z-[300] flex items-center justify-center p-6 backdrop-blur-sm bg-black/30"
        @click.self="closeKycModal">

        <div class="bg-white w-full max-w-md rounded-2xl shadow-2xl border border-gray-100 overflow-hidden">

          <!-- Bande colorée selon statut -->
          <div class="h-1.5 w-full" :class="stripColor"></div>

          <!-- Corps -->
          <div class="p-8 space-y-6">

            <!-- Icône + Titre -->
            <div class="flex items-start gap-4">
              <div :class="['w-14 h-14 rounded-2xl flex items-center justify-center flex-shrink-0', iconBg]">
                <i :class="['text-2xl', iconClass]"></i>
              </div>
              <div>
                <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest mb-0.5">
                  {{ t('kyc.sidebarLink') }}
                </p>
                <h3 class="text-lg font-black text-[#112830] leading-tight">
                  {{ t('kyc.guardTitle') }}
                </h3>
                <p class="text-xs font-bold mt-0.5" :class="subtitleColor">{{ subtitle }}</p>
              </div>
            </div>

            <!-- Description -->
            <p class="text-sm text-gray-500 leading-relaxed bg-gray-50 rounded-xl p-4 border border-gray-100">
              {{ description }}
            </p>

            <!-- Actions -->
            <div class="flex gap-3">
              <button @click="closeKycModal"
                class="flex-1 py-3 rounded-xl border border-gray-100 text-gray-500 font-bold text-sm hover:bg-gray-50 transition-colors">
                {{ t('kyc.guardClose') }}
              </button>
              <button @click="goToKyc"
                :class="['flex-[2] py-3 rounded-xl font-bold text-sm text-white flex items-center justify-center gap-2 transition-all', ctaClass]">
                <i class="bx bx-id-card text-base"></i>
                {{ t('kyc.guardCta') }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useKycGuard } from '~/composables/useKycGuard'

const { t } = useI18n()
const router = useRouter()
const route  = useRoute()
const { kycModalOpen, kycStatus, closeKycModal } = useKycGuard()

const kycPath = computed(() => {
  const p = route.path
  if (p.startsWith('/seller'))       return '/seller/kyc'
  if (p.startsWith('/organization')) return '/organization/kyc'
  return '/farmer/kyc'
})

const subtitle = computed(() => {
  if (kycStatus.value === 'PENDING')  return t('kyc.guardSubtitlePending')
  if (kycStatus.value === 'REJECTED') return t('kyc.guardSubtitleRejected')
  return t('kyc.guardSubtitleNone')
})

const description = computed(() => {
  if (kycStatus.value === 'PENDING')  return t('kyc.guardDescPending')
  if (kycStatus.value === 'REJECTED') return t('kyc.guardDescRejected')
  return t('kyc.guardDescNone')
})

const iconBg = computed(() => {
  if (kycStatus.value === 'PENDING')  return 'bg-amber-50'
  if (kycStatus.value === 'REJECTED') return 'bg-rose-50'
  return 'bg-blue-50'
})

const iconClass = computed(() => {
  if (kycStatus.value === 'PENDING')  return 'bx bx-time-five text-amber-500'
  if (kycStatus.value === 'REJECTED') return 'bx bx-shield-x text-rose-500'
  return 'bx bx-shield-quarter text-blue-500'
})

const subtitleColor = computed(() => {
  if (kycStatus.value === 'PENDING')  return 'text-amber-500'
  if (kycStatus.value === 'REJECTED') return 'text-rose-500'
  return 'text-blue-500'
})

const stripColor = computed(() => {
  if (kycStatus.value === 'PENDING')  return 'bg-amber-400'
  if (kycStatus.value === 'REJECTED') return 'bg-rose-500'
  return 'bg-blue-500'
})

const ctaClass = computed(() => {
  if (kycStatus.value === 'REJECTED') return 'bg-rose-500 hover:bg-rose-600'
  return 'bg-[#112830] hover:bg-[#10b481]'
})

function goToKyc() {
  closeKycModal()
  router.push(kycPath.value)
}
</script>

<style scoped>
.kyc-modal-enter-active, .kyc-modal-leave-active { transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1); }
.kyc-modal-enter-from, .kyc-modal-leave-to       { opacity: 0; transform: scale(0.92); }
</style>
