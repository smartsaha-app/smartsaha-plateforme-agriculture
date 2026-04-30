<template>
  <div class="flex items-center justify-center mt-12 px-4">
    <div class="w-full max-w-md bg-white rounded-3xl border border-gray-100 p-10 shadow-xl">
      <header class="mb-8 text-center">
        <div class="w-16 h-16 bg-[#f0fdf4] rounded-2xl flex items-center justify-center mx-auto mb-4">
          <i class="bx bx-lock-open text-3xl text-[#10b481]"></i>
        </div>
        <h1 class="text-2xl font-black text-[#112830]">{{ t('resetMdpTittle') }}</h1>
        <p class="mt-2 text-sm text-gray-500 font-medium">{{ t('resetText') }}</p>
      </header>

      <form @submit.prevent="onSubmit" class="space-y-6">
        <div>
          <label for="email" class="text-gray-700 text-xs font-bold uppercase tracking-wider mb-2 block">{{ t('email') }}</label>
          <div class="relative">
            <input
              id="email"
              v-model="email"
              :aria-invalid="!!errorMessage || !isEmailValid"
              type="email"
              placeholder="votre@email.com"
              class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-4 focus:ring-[#10b481]/5 focus:border-[#10b481] outline-none transition-all disabled:opacity-50"
              :disabled="loading || success"
              required
            />
          </div>
        </div>

        <p v-if="validationTouched && !isEmailValid" class="text-xs font-bold text-red-500">{{ t('resetLabel') }}</p>
        <p v-if="errorMessage" class="text-xs font-bold text-red-500">{{ errorMessage }}</p>

        <button
          type="submit"
          :disabled="!isEmailValid || loading || success"
          class="w-full flex items-center justify-center gap-2 rounded-xl px-6 py-4 bg-[#112830] text-white font-bold hover:bg-black transition-all disabled:opacity-50 shadow-lg shadow-black/10"
        >
          <i v-if="loading" class="bx bx-loader-alt animate-spin text-xl"></i>
          <span v-if="!loading && !success">{{ t('resetBtn') }}</span>
          <span v-if="success">Email envoyé !</span>
        </button>
      </form>

      <div class="mt-8 text-center">
        <button @click="$router.push(`/${role}/profil`)" class="text-sm font-bold text-[#10b481] hover:underline">
          <i class="bx bx-arrow-back mr-1"></i> {{ t('return') }}
        </button>
      </div>

      <div v-if="success" class="mt-6 p-4 rounded-xl bg-green-50 border border-green-100 text-green-800 text-sm font-medium animate-fade-in text-center">
        <i class="bx bx-check-circle mr-1"></i> {{ t('responseMessage') }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useApi } from "~/composables/useApi";

const props = defineProps<{
  role: string;
}>();

const { t: nuxtT } = useI18n();
const t = (key: string) => nuxtT(`dashboard.${key}`);

const email = ref('')
const loading = ref(false)
const success = ref(false)
const errorMessage = ref('')
const validationTouched = ref(false)

const isEmailValid = computed(() => {
  const re = /^\S+@\S+\.\S+$/
  return re.test(email.value.trim())
})

const { apiFetch } = useApi()

const onSubmit = async () => {
  validationTouched.value = true
  errorMessage.value = ''

  if (!isEmailValid.value) return

  loading.value = true

  try {
    await apiFetch('/api/forgot-password/', {
      method: 'POST',
      body: { email: email.value.trim() }
    })
    success.value = true
  } catch (err: any) {
    errorMessage.value = err?.data?.error || err?.data?.message || 'Erreur réseau. Réessayez plus tard.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.4s ease-out forwards;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
