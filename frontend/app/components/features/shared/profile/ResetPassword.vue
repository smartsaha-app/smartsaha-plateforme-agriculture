<template>
  <div class="flex items-center justify-center min-h-[calc(100vh-120px)] px-4 py-8">
    <div class="w-full max-w-lg">

      <!-- Card principale -->
      <div class="bg-white rounded-3xl shadow-xl shadow-gray-100/50 border border-gray-100 overflow-hidden">
        
        <!-- En-tête avec dégradé moderne -->
        <div class="bg-gradient-to-br from-[#112830] via-[#163540] to-[#10b481] p-6 sm:p-8 text-white relative overflow-hidden">
          <!-- Effets de fond discrets -->
          <div class="absolute -right-8 -bottom-8 w-32 h-32 rounded-full bg-[#10b481]/20 blur-xl pointer-events-none"></div>
          <div class="absolute -left-6 -top-6 w-24 h-24 rounded-full bg-white/10 blur-lg pointer-events-none"></div>

          <div class="relative z-10 flex items-center gap-4">
            <div class="w-12 h-12 bg-white/10 backdrop-blur-md border border-white/15 rounded-2xl flex items-center justify-center flex-shrink-0 shadow-inner">
              <i class="bx bx-shield-quarter text-2xl text-emerald-300"></i>
            </div>
            <div>
              <h1 class="text-xl sm:text-2xl font-black text-white tracking-tight">Changer le mot de passe</h1>
              <p class="text-xs sm:text-sm text-gray-300 mt-0.5">Mettez à jour la sécurité de votre compte</p>
            </div>
          </div>
        </div>

        <!-- Corps du formulaire -->
        <div class="p-6 sm:p-8">

          <!-- État Succès -->
          <div v-if="success" class="text-center py-6 space-y-4">
            <div class="w-16 h-16 bg-[#edf8f3] text-[#10b481] border border-[#10b481]/20 rounded-2xl flex items-center justify-center mx-auto shadow-inner">
              <i class="bx bx-check-circle text-4xl"></i>
            </div>
            <div>
              <h2 class="text-lg font-black text-[#112830]">Mot de passe mis à jour !</h2>
              <p class="text-xs sm:text-sm text-gray-500 mt-1">Un e-mail de confirmation vous a été envoyé.</p>
            </div>
            <button
              @click="resetForm"
              class="inline-flex items-center gap-2 px-5 py-2.5 bg-gray-100 hover:bg-gray-200 text-[#112830] font-bold text-xs rounded-xl transition-all mt-2"
            >
              <i class="bx bx-refresh text-base"></i>
              <span>Modifier à nouveau</span>
            </button>
          </div>

          <!-- Formulaire de saisie -->
          <form v-else @submit.prevent="onSubmit" class="space-y-5" novalidate>

            <!-- Nouveau mot de passe -->
            <div>
              <label for="new_password" class="text-gray-700 text-xs font-black uppercase tracking-wider mb-2 block">
                Nouveau mot de passe
              </label>
              <div class="relative">
                <i class="bx bx-key absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 text-lg"></i>
                <input
                  id="new_password"
                  v-model="newPassword"
                  :type="showNew ? 'text' : 'password'"
                  placeholder="Minimum 8 caractères"
                  class="w-full pl-11 pr-11 py-3 bg-gray-50 border border-gray-200 rounded-2xl text-sm font-medium text-[#112830] placeholder-gray-400 focus:bg-white focus:ring-4 focus:ring-[#10b481]/10 focus:border-[#10b481] outline-none transition-all"
                  :disabled="loading"
                />
                <button 
                  type="button" 
                  @click="showNew = !showNew" 
                  class="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors p-1"
                >
                  <i :class="showNew ? 'bx bx-hide' : 'bx bx-show'" class="text-lg"></i>
                </button>
              </div>

              <!-- Jauge de force du mot de passe -->
              <div v-if="newPassword.length > 0" class="mt-2.5 space-y-1">
                <div class="flex gap-1.5">
                  <div 
                    v-for="i in 4" 
                    :key="i" 
                    class="h-1.5 flex-1 rounded-full transition-all duration-300"
                    :class="strengthScore >= i ? strengthColor : 'bg-gray-100'"
                  ></div>
                </div>
                <div class="flex justify-between items-center text-[11px]">
                  <span class="text-gray-400 font-medium">Force du mot de passe</span>
                  <span class="font-bold" :class="strengthTextColor">{{ strengthLabel }}</span>
                </div>
              </div>
            </div>

            <!-- Confirmer le mot de passe -->
            <div>
              <label for="confirm_password" class="text-gray-700 text-xs font-black uppercase tracking-wider mb-2 block">
                Confirmer le mot de passe
              </label>
              <div class="relative">
                <i class="bx bx-check-shield absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 text-lg"></i>
                <input
                  id="confirm_password"
                  v-model="confirmPassword"
                  :type="showConfirm ? 'text' : 'password'"
                  placeholder="Répétez votre mot de passe"
                  class="w-full pl-11 pr-11 py-3 bg-gray-50 border rounded-2xl text-sm font-medium text-[#112830] placeholder-gray-400 focus:bg-white focus:ring-4 outline-none transition-all"
                  :class="confirmBorderClass"
                  :disabled="loading"
                />
                <button 
                  type="button" 
                  @click="showConfirm = !showConfirm" 
                  class="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors p-1"
                >
                  <i :class="showConfirm ? 'bx bx-hide' : 'bx bx-show'" class="text-lg"></i>
                </button>
              </div>

              <!-- Messages de correspondance -->
              <p v-if="confirmPassword.length > 0 && newPassword !== confirmPassword" class="mt-1.5 text-xs text-red-500 font-bold flex items-center gap-1">
                <i class="bx bx-x-circle text-sm"></i> Les mots de passe ne correspondent pas
              </p>
              <p v-if="confirmPassword.length > 0 && newPassword === confirmPassword" class="mt-1.5 text-xs text-[#10b481] font-bold flex items-center gap-1">
                <i class="bx bx-check-circle text-sm"></i> Les mots de passe correspondent
              </p>
            </div>

            <!-- Message d'erreur API -->
            <div v-if="errorMessage" class="flex items-center gap-2.5 p-3.5 bg-red-50 border border-red-100 rounded-2xl text-xs text-red-600 font-medium">
              <i class="bx bx-error-circle text-red-500 text-lg flex-shrink-0"></i>
              <span>{{ errorMessage }}</span>
            </div>

            <!-- Bouton Submit -->
            <button
              type="submit"
              :disabled="loading || !isValid"
              class="w-full flex items-center justify-center gap-2 rounded-2xl px-6 py-3.5 font-bold text-sm transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-md"
              :class="isValid ? 'bg-[#10b481] hover:bg-[#0ea072] text-white shadow-[#10b481]/20 hover:scale-[1.01] active:scale-[0.99]' : 'bg-gray-100 text-gray-400 shadow-none'"
            >
              <i v-if="loading" class="bx bx-loader-alt animate-spin text-lg"></i>
              <i v-else class="bx bx-check text-lg"></i>
              <span>{{ loading ? 'Enregistrement...' : 'Enregistrer le nouveau mot de passe' }}</span>
            </button>

          </form>

          <!-- Retour au profil -->
          <div class="mt-6 text-center" v-if="!success">
            <button 
              type="button"
              @click="$router.push(`/${role}/profil`)" 
              class="inline-flex items-center gap-1.5 text-xs font-bold text-gray-400 hover:text-[#112830] transition-colors"
            >
              <i class="bx bx-left-arrow-alt text-base"></i>
              <span>Retour au profil</span>
            </button>
          </div>

        </div>
      </div>

      <!-- Conseil de sécurité -->
      <div class="mt-4 flex items-start gap-3 p-4 bg-emerald-50/60 border border-emerald-100/80 rounded-2xl">
        <i class="bx bx-[#10b481] bx-shield-alt-2 text-[#10b481] text-xl flex-shrink-0 mt-0.5"></i>
        <p class="text-xs text-gray-600 leading-relaxed">
          <span class="font-bold text-[#112830]">Conseil de sécurité :</span> Utilisez un mot de passe unique d'au moins 8 caractères combinant majuscules, minuscules, chiffres et symboles.
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

const newPassword     = ref('')
const confirmPassword = ref('')
const showNew         = ref(false)
const showConfirm     = ref(false)
const loading         = ref(false)
const success         = ref(false)
const errorMessage    = ref('')

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
  return 'bg-[#10b481]'
})

const strengthTextColor = computed(() => {
  if (strengthScore.value <= 1) return 'text-red-500'
  if (strengthScore.value === 2) return 'text-orange-500'
  if (strengthScore.value === 3) return 'text-yellow-600'
  return 'text-[#10b481]'
})

const strengthLabel = computed(() => {
  if (strengthScore.value <= 1) return 'Faible'
  if (strengthScore.value === 2) return 'Moyen'
  if (strengthScore.value === 3) return 'Bon'
  return 'Très sécurisé'
})

// ── Validation ──────────────────────────────────────
const isValid = computed(() => {
  return newPassword.value.length >= 8 && newPassword.value === confirmPassword.value
})

const confirmBorderClass = computed(() => {
  if (!confirmPassword.value) return 'border-gray-200 focus:ring-[#10b481]/10 focus:border-[#10b481]'
  if (newPassword.value === confirmPassword.value) return 'border-emerald-300 focus:ring-emerald-100 focus:border-[#10b481]'
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