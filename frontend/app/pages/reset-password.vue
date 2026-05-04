<template>
  <div class="min-h-screen bg-[#f9f9f9] flex flex-col items-center justify-center p-6 relative">
    
    <!-- Logo -->
    <div class="absolute top-6 left-6 md:top-8 md:left-8 flex items-center gap-3">
      <img
        src="/logo.png"
        alt="Smartsaha Logo"
        class="w-10 h-10 object-contain"
      />
      <div class="flex flex-col text-left">
        <h1 class="text-md font-bold text-[#112830]">Smartsaha</h1>
        <p class="text-gray-500 text-xs">Nurture Data, Harvest Impact.</p>
      </div>
    </div>

    <div class="w-full max-w-md bg-white rounded-2xl shadow-xl border border-gray-100 p-8 relative z-10 mt-12 md:mt-0">
      
      <!-- ÉTAPE 1: Demande par Email -->
      <div v-if="step === 1">
        <header class="mb-8 text-center">
          <h1 class="text-2xl font-black text-[#112830]">{{ t('resetMdpTittle') }}</h1>
          <p class="mt-2 text-sm text-gray-500">{{ t('resetText') }}</p>
        </header>

        <form @submit.prevent="onEmailSubmit" novalidate>
          <label for="email" class="text-gray-700 text-sm font-medium mb-1">{{ t('email') }}</label>
          <div class="mt-1 relative">
            <input
              id="email"
              v-model="email"
              :aria-invalid="!!errorMessage || !isEmailValid"
              type="email"
              placeholder="nom@exemple.com"
              class="appearance-none block w-full px-4 py-3 border rounded shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-[#10b481] transition disabled:opacity-60"
              :disabled="loading"
              required
            />
          </div>

          <p v-if="validationTouched && !isEmailValid" class="mt-2 text-sm text-red-600">{{ t('resetLabel') }}</p>
          <p v-if="errorMessage" class="mt-2 text-sm text-red-600">{{ errorMessage }}</p>

          <button
            type="submit"
            :disabled="!isEmailValid || loading"
            class="mt-6 w-full inline-flex items-center justify-center gap-2 rounded px-4 py-3 bg-[#10b481] text-white font-medium hover:bg-[#0da06a] focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-green-500 disabled:opacity-60 transition-colors"
          >
            <svg v-if="loading" class="w-5 h-5 animate-spin" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-opacity="0.25" stroke-width="4"></circle>
              <path d="M22 12a10 10 0 00-10-10" stroke="currentColor" stroke-width="4" stroke-linecap="round"></path>
            </svg>

            <span v-if="!loading">{{ t('resetBtn') }}</span>
          </button>
        </form>
      </div>

      <!-- ÉTAPE 2: Saisie OTP et Nouveau Mot de Passe -->
      <div v-else-if="step === 2">
        <header class="mb-8 text-center">
          <h1 class="text-2xl font-black text-[#112830]">Nouveau mot de passe</h1>
          <p class="mt-2 text-sm text-gray-500">Un code à 6 chiffres a été envoyé à <strong>{{ email }}</strong>. Veuillez le saisir ci-dessous avec votre nouveau mot de passe.</p>
        </header>

        <form @submit.prevent="onResetSubmit" novalidate v-if="!success">
          <div class="space-y-4">
            <div>
              <label for="otp" class="text-gray-700 text-sm font-medium mb-1">Code de vérification (6 chiffres)</label>
              <div class="mt-1 relative">
                <input
                  id="otp"
                  v-model="code"
                  type="text"
                  placeholder="123456"
                  maxlength="6"
                  class="appearance-none block w-full px-4 py-3 border rounded shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-[#10b481] text-center tracking-widest text-lg font-bold transition disabled:opacity-60"
                  :disabled="loading"
                  required
                />
              </div>
            </div>

            <div>
              <label for="new_password" class="text-gray-700 text-sm font-medium mb-1">Nouveau mot de passe</label>
              <div class="mt-1 relative">
                <input
                  id="new_password"
                  v-model="newPassword"
                  type="password"
                  placeholder="********"
                  class="appearance-none block w-full px-4 py-3 border rounded shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-[#10b481] transition disabled:opacity-60"
                  :disabled="loading"
                  required
                />
              </div>
            </div>

            <div>
              <label for="confirm_password" class="text-gray-700 text-sm font-medium mb-1">Confirmer le mot de passe</label>
              <div class="mt-1 relative">
                <input
                  id="confirm_password"
                  v-model="confirmPassword"
                  type="password"
                  placeholder="********"
                  class="appearance-none block w-full px-4 py-3 border rounded shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-[#10b481] transition disabled:opacity-60"
                  :disabled="loading"
                  required
                />
              </div>
            </div>
          </div>

          <p v-if="errorMessage" class="mt-4 text-sm text-red-600 text-center">{{ errorMessage }}</p>

          <button
            type="submit"
            :disabled="loading || !isResetValid"
            class="mt-6 w-full inline-flex items-center justify-center gap-2 rounded px-4 py-3 bg-[#10b481] text-white font-medium hover:bg-[#0da06a] focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-green-500 disabled:opacity-60 transition-colors"
          >
            <svg v-if="loading" class="w-5 h-5 animate-spin" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-opacity="0.25" stroke-width="4"></circle>
              <path d="M22 12a10 10 0 00-10-10" stroke="currentColor" stroke-width="4" stroke-linecap="round"></path>
            </svg>

            <span v-if="!loading">Enregistrer le mot de passe</span>
          </button>
        </form>
        
        <div v-if="success" class="mt-6 p-4 rounded-lg bg-green-50 border border-green-100 text-green-800 text-sm text-center">
          Votre mot de passe a été réinitialisé avec succès. Vous allez être redirigé vers la page de connexion.
        </div>
      </div>

      <div class="mt-8 text-center text-sm text-gray-500" v-if="!success">
        <NuxtLink to="/login" class="text-[#10b481] hover:underline font-bold flex items-center justify-center gap-1">
          <i class='bx bx-arrow-back'></i> {{ t('return') }}
        </NuxtLink>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useApi } from "~/composables/useApi";

const { t: nuxtT } = useI18n();
const t = (key: string, defaultText: string = '') => {
  const text = nuxtT(`dashboard.${key}`);
  return text.startsWith('dashboard.') ? defaultText || text : text;
};

const step = ref(1)

const email = ref('')
const code = ref('')
const newPassword = ref('')
const confirmPassword = ref('')

const loading = ref(false)
const success = ref(false)
const errorMessage = ref('')
const validationTouched = ref(false)

const isEmailValid = computed(() => {
  const re = /^\S+@\S+\.\S+$/
  return re.test(email.value.trim())
})

const isResetValid = computed(() => {
  return code.value.length === 6 && newPassword.value.length >= 8 && newPassword.value === confirmPassword.value;
})

const router = useRouter()
const { apiFetch } = useApi()

const onEmailSubmit = async () => {
  validationTouched.value = true
  errorMessage.value = ''

  if (!isEmailValid.value) return

  loading.value = true

  try {
    await apiFetch('/api/forgot-password/', {
      method: 'POST',
      body: { email: email.value.trim() }
    })

    // Passer à l'étape 2 (OTP)
    step.value = 2
  } catch (err: any) {
    if (err?.data?.error) {
      errorMessage.value = err.data.error
    } else if (err?.data?.message) {
      // Dans notre backend "Si l'email existe, un lien a été envoyé"
      step.value = 2
    } else {
      errorMessage.value = 'Erreur réseau. Réessaie plus tard.'
    }
  } finally {
    loading.value = false
  }
}

const onResetSubmit = async () => {
  errorMessage.value = '';

  if (newPassword.value !== confirmPassword.value) {
    errorMessage.value = 'Les mots de passe ne correspondent pas.';
    return;
  }
  
  if (newPassword.value.length < 8) {
    errorMessage.value = 'Le mot de passe doit contenir au moins 8 caractères.';
    return;
  }

  loading.value = true;

  try {
    await apiFetch(`/api/reset-password/`, {
      method: 'POST',
      body: { 
        email: email.value.trim(),
        code: code.value.trim(),
        new_password: newPassword.value,
        confirm_password: confirmPassword.value
      }
    });

    success.value = true;
    setTimeout(() => {
      router.push('/login');
    }, 3000);
  } catch (err: any) {
    if (err?.data?.error) {
      errorMessage.value = err.data.error;
    } else {
      errorMessage.value = 'Erreur réseau ou code expiré.';
    }
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
body { font-family: Inter, ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial }
</style>
