<template>
  <div class=" flex items-center justify-center mt-16">
    <div class="w-full max-w-md bg-white rounded  border border-gray-100 p-8">
      <header class="mb-6 text-center">
        <h1 class="text-2xl font-semibold text-gray-900">{{ t('resetMdpTittle') }}</h1>
        <p class="mt-2 text-sm text-gray-500">{{ t('resetText') }}</p>
      </header>

      <form @submit.prevent="onSubmit" novalidate>
        <label for="email" class="text-gray-700 text-sm font-medium mb-1">{{ t('email') }}</label>
        <div class="mt-1 relative">
          <input
            id="email"
            v-model="email"
            :aria-invalid="!!errorMessage || !isEmailValid"
            type="email"
            placeholder="nom@exemple.com"
            class="appearance-none block w-full px-4 py-3 border rounded shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-[#10b481] transition disabled:opacity-60"
            :disabled="loading || success"
            required
          />
        </div>

        <p v-if="validationTouched && !isEmailValid" class="mt-2 text-sm text-red-600">{{ t('resetLabel') }}</p>
        <p v-if="errorMessage" class="mt-2 text-sm text-red-600">{{ errorMessage }}</p>

        <button
          type="submit"
          :disabled="!isEmailValid || loading || success"
          class="mt-6 w-full inline-flex items-center justify-center gap-2 rounded px-4 py-3 bg-[#10b481] text-white font-medium hover:bg-[#10b481] focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-green-500 disabled:opacity-60"
        >
          <svg v-if="loading" class="w-5 h-5 animate-spin" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-opacity="0.25" stroke-width="4"></circle>
            <path d="M22 12a10 10 0 00-10-10" stroke="currentColor" stroke-width="4" stroke-linecap="round"></path>
          </svg>

          <span v-if="!loading && !success">{{ t('resetBtn') }}</span>
          <span v-if="success">{{ t('errorMessage') }}</span>
        </button>
      </form>

      <div class="mt-6 text-center text-sm text-gray-500">
        <NuxtLink to="/login" class="underline">{{ t('return') }}</NuxtLink>
      </div>

      <div v-if="success" class="mt-6 p-4 rounded-lg bg-green-50 border border-green-100 text-green-800 text-sm">
        {{ t('responseMessage') }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">

definePageMeta({ layout: "dashboard" });
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useApi } from "~/composables/useApi";

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

const router = useRouter()
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
    if (err?.data?.error) {
      errorMessage.value = err.data.error
    } else if (err?.data?.message) {
      errorMessage.value = err.data.message
    } else {
      errorMessage.value = 'Erreur réseau. Réessaie plus tard.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
body { font-family: Inter, ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial }
</style>
