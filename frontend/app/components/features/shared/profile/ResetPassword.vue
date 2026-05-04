<template>
  <div class="flex items-center justify-center min-h-[calc(100vh-120px)] px-4 py-10">
    <div class="w-full max-w-lg">

      <!-- Card principale -->
      <div class="bg-white rounded-3xl shadow-2xl shadow-gray-100 border border-gray-100 overflow-hidden">
        
        <!-- Header avec dégradé -->
        <div class="bg-gradient-to-br from-[#112830] to-[#1a3d4a] px-8 py-8">
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 bg-white/10 backdrop-blur rounded-2xl flex items-center justify-center flex-shrink-0">
              <i class="bx bx-lock-alt text-2xl text-white"></i>
            </div>
            <div>
              <h1 class="text-xl font-black text-white">Changer le mot de passe</h1>
              <p class="text-sm text-white/60 mt-0.5">Mettez à jour la sécurité de votre compte</p>
            </div>
          </div>
        </div>

        <!-- Formulaire -->
        <div class="px-8 py-8">

          <!-- État Succès -->
          <div v-if="success" class="text-center py-6">
            <div class="w-16 h-16 bg-green-50 rounded-full flex items-center justify-center mx-auto mb-4">
              <i class="bx bx-check text-4xl text-green-500"></i>
            </div>
            <h2 class="text-lg font-bold text-[#112830]">Mot de passe mis à jour !</h2>
            <p class="text-sm text-gray-500 mt-2">Un email de confirmation vous a été envoyé.</p>
            <button
              @click="resetForm"
              class="mt-6 text-sm font-bold text-[#10b481] hover:underline"
            >
              Modifier à nouveau
            </button>
          </div>

          <!-- Formulaire de saisie -->
          <form v-else @submit.prevent="onSubmit" class="space-y-5" novalidate>

            <!-- Nouveau mot de passe -->
            <div>
              <label for="new_password" class="text-xs font-bold text-gray-500 uppercase tracking-widest mb-2 block">
                Nouveau mot de passe
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                  <i class="bx bx-key text-gray-400 text-lg"></i>
                </div>
                <input
                  id="new_password"
                  v-model="newPassword"
                  :type="showNew ? 'text' : 'password'"
                  placeholder="Minimum 8 caractères"
                  class="w-full pl-11 pr-11 py-3.5 bg-gray-50 border border-gray-200 rounded-xl text-sm text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#10b481]/30 focus:border-[#10b481] transition-all"
                  :disabled="loading"
                />
                <button type="button" @click="showNew = !showNew" class="absolute inset-y-0 right-0 pr-4 flex items-center text-gray-400 hover:text-gray-600 transition-colors">
                  <i :class="showNew ? 'bx bx-hide' : 'bx bx-show'" class="text-lg"></i>
                </button>
              </div>

              <!-- Jauge de force du mot de passe -->
              <div v-if="newPassword.length > 0" class="mt-2">
                <div class="flex gap-1 mb-1">
                  <div v-for="i in 4" :key="i" class="h-1 flex-1 rounded-full transition-all duration-300"
                    :class="strengthScore >= i ? strengthColor : 'bg-gray-200'">
                  </div>
                </div>
                <p class="text-xs font-medium" :class="strengthTextColor">{{ strengthLabel }}</p>
              </div>
            </div>

            <!-- Confirmer le mot de passe -->
            <div>
              <label for="confirm_password" class="text-xs font-bold text-gray-500 uppercase tracking-widest mb-2 block">
                Confirmer le mot de passe
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                  <i class="bx bx-check-shield text-gray-400 text-lg"></i>
                </div>
                <input
                  id="confirm_password"
                  v-model="confirmPassword"
                  :type="showConfirm ? 'text' : 'password'"
                  placeholder="Répétez votre mot de passe"
                  class="w-full pl-11 pr-11 py-3.5 bg-gray-50 border rounded-xl text-sm text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 transition-all"
                  :class="confirmBorderClass"
                  :disabled="loading"
                />
                <button type="button" @click="showConfirm = !showConfirm" class="absolute inset-y-0 right-0 pr-4 flex items-center text-gray-400 hover:text-gray-600 transition-colors">
                  <i :class="showConfirm ? 'bx bx-hide' : 'bx bx-show'" class="text-lg"></i>
                </button>
              </div>
              <p v-if="confirmPassword.length > 0 && newPassword !== confirmPassword" class="mt-1.5 text-xs text-red-500 font-medium">
                <i class="bx bx-x-circle mr-1"></i>Les mots de passe ne correspondent pas
              </p>
              <p v-if="confirmPassword.length > 0 && newPassword === confirmPassword" class="mt-1.5 text-xs text-green-600 font-medium">
                <i class="bx bx-check-circle mr-1"></i>Les mots de passe correspondent
              </p>
            </div>

            <!-- Message d'erreur API -->
            <div v-if="errorMessage" class="flex items-center gap-2 p-3 bg-red-50 border border-red-100 rounded-xl">
              <i class="bx bx-error-circle text-red-500 text-lg flex-shrink-0"></i>
              <p class="text-xs text-red-600 font-medium">{{ errorMessage }}</p>
            </div>

            <!-- Bouton Submit -->
            <button
              type="submit"
              :disabled="loading || !isValid"
              class="w-full flex items-center justify-center gap-2 rounded-xl px-6 py-4 font-bold text-sm transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg"
              :class="isValid ? 'bg-[#10b481] text-white hover:bg-[#0da06a] shadow-[#10b481]/25' : 'bg-gray-100 text-gray-400 shadow-none'"
            >
              <i v-if="loading" class="bx bx-loader-alt animate-spin text-lg"></i>
              <i v-else class="bx bx-save text-lg"></i>
              <span>{{ loading ? 'Enregistrement...' : 'Enregistrer le nouveau mot de passe' }}</span>
            </button>

          </form>

          <!-- Retour au profil -->
          <div class="mt-6 text-center" v-if="!success">
            <button @click="$router.push(`/${role}/profil`)" class="text-sm font-bold text-gray-400 hover:text-[#10b481] transition-colors">
              <i class="bx bx-arrow-back mr-1"></i>Retour au profil
            </button>
          </div>

        </div>
      </div>

      <!-- Conseil de sécurité -->
      <div class="mt-4 flex items-start gap-3 px-4 py-3 bg-blue-50 border border-blue-100 rounded-2xl">
        <i class="bx bx-shield-quarter text-blue-400 text-xl flex-shrink-0 mt-0.5"></i>
        <p class="text-xs text-blue-600">
          <span class="font-bold">Conseil de sécurité :</span> Utilisez un mot de passe unique d'au moins 8 caractères mélangeant lettres, chiffres et symboles.
        </p>
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

const { apiFetch } = useApi()

const newPassword    = ref('')
const confirmPassword = ref('')
const showNew        = ref(false)
const showConfirm    = ref(false)
const loading        = ref(false)
const success        = ref(false)
const errorMessage   = ref('')

// ── Force du mot de passe ──────────────────────────
const strengthScore = computed(() => {
  const pw = newPassword.value
  if (pw.length === 0) return 0
  let score = 0
  if (pw.length >= 8)  score++
  if (pw.length >= 12) score++
  if (/[A-Z]/.test(pw) && /[a-z]/.test(pw)) score++
  if (/[0-9]/.test(pw)) score++
  if (/[^A-Za-z0-9]/.test(pw)) score++
  return Math.min(score, 4)
})

const strengthColor = computed(() => {
  if (strengthScore.value <= 1) return 'bg-red-500'
  if (strengthScore.value === 2) return 'bg-orange-400'
  if (strengthScore.value === 3) return 'bg-yellow-400'
  return 'bg-green-500'
})

const strengthTextColor = computed(() => {
  if (strengthScore.value <= 1) return 'text-red-500'
  if (strengthScore.value === 2) return 'text-orange-400'
  if (strengthScore.value === 3) return 'text-yellow-500'
  return 'text-green-600'
})

const strengthLabel = computed(() => {
  if (strengthScore.value <= 1) return 'Faible'
  if (strengthScore.value === 2) return 'Acceptable'
  if (strengthScore.value === 3) return 'Bon'
  return 'Très sécurisé'
})

// ── Validation ──────────────────────────────────────
const isValid = computed(() => {
  return newPassword.value.length >= 8 && newPassword.value === confirmPassword.value
})

const confirmBorderClass = computed(() => {
  if (!confirmPassword.value) return 'border-gray-200 focus:ring-[#10b481]/30 focus:border-[#10b481]'
  if (newPassword.value === confirmPassword.value) return 'border-green-300 focus:ring-green-200 focus:border-green-400'
  return 'border-red-300 focus:ring-red-100 focus:border-red-400'
})

// ── Soumission ─────────────────────────────────────
const onSubmit = async () => {
  errorMessage.value = ''
  if (!isValid.value) return

  loading.value = true
  try {
    await apiFetch('/api/change-password/', {
      method: 'POST',
      body: {
        new_password:     newPassword.value,
        confirm_password: confirmPassword.value,
      }
    })
    success.value = true
  } catch (err: any) {
    errorMessage.value = err?.data?.error || 'Erreur réseau. Réessayez plus tard.'
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  newPassword.value     = ''
  confirmPassword.value = ''
  success.value         = false
  errorMessage.value    = ''
}
</script>

<style scoped>
.animate-spin {
  animation: spin 0.8s linear infinite;
}
@keyframes spin {
  from { transform: rotate(0deg); }
  to   { transform: rotate(360deg); }
}
</style>
