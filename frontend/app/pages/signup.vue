<template>
  <div class="min-h-screen bg-[#f4f6f8] flex flex-col items-center justify-center px-4 py-10 relative overflow-hidden">

    <!-- Décoration fond -->
    <div class="pointer-events-none absolute inset-0 overflow-hidden">
      <div class="absolute -top-32 -right-32 w-96 h-96 rounded-full bg-[#10b481]/8 blur-3xl" />
      <div class="absolute -bottom-32 -left-32 w-96 h-96 rounded-full bg-[#112830]/6 blur-3xl" />
    </div>

    <!-- Carte principale -->
    <div class="relative w-full max-w-[460px]">

      <!-- ── En-tête marque ──────────────────────────────────────────────── -->
      <div class="text-center mb-7">
        <div class="inline-flex items-center gap-3 mb-4">
          <img src="/logo.png" alt="Smartsaha" class="w-10 h-10 object-contain" />
          <span class="text-xl font-black text-[#112830]">Smartsaha</span>
        </div>
        <h1 class="text-3xl font-black text-[#112830] leading-tight">
          {{ $t('auth.signupHeading') }}
        </h1>
        <p class="text-gray-500 text-sm mt-2">{{ $t('auth.signupSubheading') }}</p>
      </div>

      <!-- ── Indicateur de progression ───────────────────────────────────── -->
      <div class="flex items-center justify-center gap-0 mb-6">
        <template v-for="s in 3" :key="s">
          <div class="flex flex-col items-center">
            <div :class="[
              'w-9 h-9 rounded-full flex items-center justify-center text-sm font-black transition-all duration-300',
              currentStep > s  ? 'bg-[#10b481] text-white shadow-md shadow-[#10b481]/30' :
              currentStep === s ? 'bg-[#112830] text-white shadow-lg' :
              'bg-white text-gray-400 border-2 border-gray-200'
            ]">
              <i v-if="currentStep > s" class="bx bx-check text-base leading-none" />
              <span v-else>{{ s }}</span>
            </div>
            <p :class="[
              'text-[10px] font-bold mt-1 transition-colors',
              currentStep === s ? 'text-[#112830]' : currentStep > s ? 'text-[#10b481]' : 'text-gray-400'
            ]">{{ stepLabels[s - 1] }}</p>
          </div>
          <!-- Barre de connexion -->
          <div v-if="s < 3" :class="[
            'h-0.5 w-16 mx-1 mt-[-14px] rounded-full transition-all duration-500',
            currentStep > s ? 'bg-[#10b481]' : 'bg-gray-200'
          ]" />
        </template>
      </div>

      <!-- ── Corps des étapes ───────────────────────────────────────────── -->
      <div class="bg-white rounded-3xl shadow-xl shadow-gray-200/60 overflow-hidden">
        <Transition :name="transitionName" mode="out-in">

          <!-- ── Étape 1 : Offre ─────────────────────────────────────────── -->
          <div v-if="currentStep === 1" key="step1" class="p-7">
            <div class="mb-5">
              <h2 class="text-lg font-black text-[#112830]">{{ $t('auth.step1Title') }}</h2>
              <p class="text-gray-400 text-xs mt-0.5">{{ $t('auth.step1Subtitle') }}</p>
            </div>

            <div class="grid grid-cols-2 gap-3">
              <!-- FREE -->
              <button type="button" @click="selectedPlan = 'FREE'" :class="[
                'relative flex flex-col items-center text-center p-4 rounded-2xl border-2 transition-all duration-200 overflow-hidden',
                selectedPlan === 'FREE'
                  ? 'border-[#10b481] bg-gradient-to-b from-[#10b481]/8 to-[#10b481]/3'
                  : 'border-gray-100 bg-gray-50/60 hover:border-gray-200 hover:bg-gray-50'
              ]">
                <!-- Radio indicator -->
                <div :class="[
                  'absolute top-3 right-3 w-4.5 h-4.5 w-[18px] h-[18px] rounded-full border-2 flex items-center justify-center transition-all',
                  selectedPlan === 'FREE' ? 'bg-[#10b481] border-[#10b481]' : 'border-gray-300 bg-white'
                ]">
                  <i v-if="selectedPlan === 'FREE'" class="bx bx-check text-white text-[10px] leading-none" />
                </div>

                <!-- Icône -->
                <div :class="[
                  'w-12 h-12 rounded-2xl flex items-center justify-center mb-3 transition-all',
                  selectedPlan === 'FREE' ? 'bg-[#10b481]/15' : 'bg-gray-100'
                ]">
                  <i class="bx bx-leaf text-2xl" :class="selectedPlan === 'FREE' ? 'text-[#10b481]' : 'text-gray-400'" />
                </div>

                <!-- Nom + badge -->
                <p class="text-sm font-black text-[#112830] leading-none">{{ $t('auth.planFree') }}</p>
                <span class="mt-1.5 text-[10px] font-bold text-gray-400 bg-gray-100 px-2 py-0.5 rounded-full">
                  {{ $t('auth.planFreeTag') }}
                </span>

                <!-- Features -->
                <ul class="mt-3 space-y-1 w-full text-left">
                  <li v-for="f in freeFeatures" :key="f" class="flex items-start gap-1.5 text-[10px] text-gray-500">
                    <i class="bx bx-check text-[#10b481] flex-shrink-0 mt-px" />
                    <span>{{ f }}</span>
                  </li>
                </ul>
              </button>

              <!-- PRO -->
              <button type="button" @click="selectedPlan = 'PRO'" :class="[
                'relative flex flex-col items-center text-center p-4 rounded-2xl border-2 transition-all duration-200 overflow-hidden',
                selectedPlan === 'PRO'
                  ? 'border-[#10b481] bg-gradient-to-b from-[#10b481]/8 to-[#10b481]/3'
                  : 'border-gray-100 bg-gray-50/60 hover:border-gray-200 hover:bg-gray-50'
              ]">
                <!-- Badge recommandé -->
                <span class="absolute top-0 left-0 right-0 text-[9px] font-black bg-gradient-to-r from-[#10b481] to-[#0aae74] text-white py-0.5 uppercase tracking-wider text-center">
                  {{ $t('auth.planProRecommended') }}
                </span>

                <!-- Radio indicator -->
                <div :class="[
                  'absolute top-7 right-3 w-[18px] h-[18px] rounded-full border-2 flex items-center justify-center transition-all',
                  selectedPlan === 'PRO' ? 'bg-[#10b481] border-[#10b481]' : 'border-gray-300 bg-white'
                ]">
                  <i v-if="selectedPlan === 'PRO'" class="bx bx-check text-white text-[10px] leading-none" />
                </div>

                <!-- Icône -->
                <div :class="[
                  'w-12 h-12 rounded-2xl flex items-center justify-center mb-3 mt-4 transition-all',
                  selectedPlan === 'PRO' ? 'bg-[#10b481]/15' : 'bg-gray-100'
                ]">
                  <i class="bx bx-crown text-2xl" :class="selectedPlan === 'PRO' ? 'text-[#10b481]' : 'text-gray-400'" />
                </div>

                <!-- Nom + badge -->
                <p class="text-sm font-black text-[#112830] leading-none">{{ $t('auth.planPro') }}</p>
                <span class="mt-1.5 text-[10px] font-bold text-[#10b481] bg-[#10b481]/10 px-2 py-0.5 rounded-full">
                  {{ $t('auth.planProTag') }}
                </span>

                <!-- Features -->
                <ul class="mt-3 space-y-1 w-full text-left">
                  <li v-for="f in proFeatures" :key="f" class="flex items-start gap-1.5 text-[10px] text-gray-500">
                    <i class="bx bx-check text-[#10b481] flex-shrink-0 mt-px" />
                    <span>{{ f }}</span>
                  </li>
                </ul>
              </button>
            </div>

            <button @click="goNext" class="mt-5 w-full py-3.5 bg-[#112830] hover:bg-[#10b481] text-white font-bold rounded-xl transition-all duration-200 flex items-center justify-center gap-2">
              {{ $t('auth.continue') }}
              <i class="bx bx-right-arrow-alt text-lg" />
            </button>
          </div>

          <!-- ── Étape 2 : Type de compte ────────────────────────────────── -->
          <div v-else-if="currentStep === 2" key="step2" class="p-7">
            <div class="mb-5">
              <h2 class="text-lg font-black text-[#112830]">{{ $t('auth.step2Title') }}</h2>
              <p class="text-gray-400 text-xs mt-0.5">{{ $t('auth.step2Subtitle') }}</p>
            </div>

            <div class="grid grid-cols-2 gap-3">
              <button
                v-for="type in accountTypes"
                :key="type.value"
                type="button"
                @click="userType = type.value"
                :class="[
                  'flex flex-col items-center justify-center gap-2.5 p-4 rounded-2xl border-2 transition-all duration-200 min-h-[120px]',
                  userType === type.value
                    ? 'border-[#10b481] bg-gradient-to-br from-[#10b481]/6 to-[#10b481]/3'
                    : 'border-gray-100 bg-gray-50/60 hover:border-gray-200 hover:bg-gray-50'
                ]"
              >
                <div :class="[
                  'w-12 h-12 rounded-2xl flex items-center justify-center transition-all',
                  userType === type.value ? 'bg-[#10b481]/15' : 'bg-gray-100'
                ]">
                  <i :class="['bx text-2xl', type.icon, userType === type.value ? 'text-[#10b481]' : 'text-gray-400']" />
                </div>
                <div class="text-center">
                  <p :class="['text-sm font-black leading-tight', userType === type.value ? 'text-[#112830]' : 'text-gray-600']">{{ type.label }}</p>
                  <p class="text-[10px] text-gray-400 mt-0.5 leading-tight">{{ type.desc }}</p>
                </div>
              </button>
            </div>

            <div class="mt-5 flex gap-3">
              <button @click="goBack" class="w-12 h-12 border-2 border-gray-200 text-gray-400 rounded-xl hover:border-gray-300 hover:text-gray-600 transition-all flex items-center justify-center flex-shrink-0">
                <i class="bx bx-left-arrow-alt text-xl" />
              </button>
              <button @click="goNext" class="flex-1 py-3.5 bg-[#112830] hover:bg-[#10b481] text-white font-bold rounded-xl transition-all duration-200 flex items-center justify-center gap-2">
                {{ $t('auth.continue') }}
                <i class="bx bx-right-arrow-alt text-lg" />
              </button>
            </div>
          </div>

          <!-- ── Étape 3 : Informations ──────────────────────────────────── -->
          <div v-else-if="currentStep === 3" key="step3" class="p-7">
            <div class="mb-4">
              <h2 class="text-lg font-black text-[#112830]">{{ $t('auth.step3Title') }}</h2>
              <p class="text-gray-400 text-xs mt-0.5">{{ $t('auth.step3Subtitle') }}</p>
            </div>

            <!-- Récap modifiable -->
            <div class="flex items-center gap-2.5 p-2.5 bg-[#f8fafb] rounded-xl border border-gray-100 mb-4">
              <div class="flex items-center gap-1.5 px-2 py-1 bg-white rounded-lg border border-gray-100">
                <i class="bx bx-crown text-[#10b481] text-xs" />
                <span class="text-[11px] font-bold text-gray-700">{{ selectedPlan === 'PRO' ? 'Pro' : $t('auth.planFree') }}</span>
              </div>
              <div class="w-px h-4 bg-gray-200" />
              <div class="flex items-center gap-1.5 px-2 py-1 bg-white rounded-lg border border-gray-100">
                <i :class="['bx text-[#10b481] text-xs', currentAccountType?.icon]" />
                <span class="text-[11px] font-bold text-gray-700">{{ currentAccountType?.label }}</span>
              </div>
              <button @click="currentStep = 1" class="ml-auto text-[10px] text-[#10b481] hover:underline font-semibold">
                {{ $t('auth.modify') }}
              </button>
            </div>

            <!-- Formulaire -->
            <form @submit.prevent="handleSignup" class="flex flex-col gap-3">
              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="text-xs font-semibold text-gray-600 mb-1.5 block">{{ $t('auth.firstName') }}</label>
                  <input
                    v-model="formData.first_name"
                    type="text"
                    :placeholder="$t('auth.firstName')"
                    class="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 bg-[#fafafa] text-sm focus:outline-none focus:border-[#10b481] focus:bg-white focus:ring-2 focus:ring-[#10b481]/10 transition-all"
                  />
                </div>
                <div>
                  <label class="text-xs font-semibold text-gray-600 mb-1.5 block">{{ $t('auth.lastName') }}</label>
                  <input
                    v-model="formData.last_name"
                    type="text"
                    :placeholder="$t('auth.lastName')"
                    class="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 bg-[#fafafa] text-sm focus:outline-none focus:border-[#10b481] focus:bg-white focus:ring-2 focus:ring-[#10b481]/10 transition-all"
                  />
                </div>
              </div>

              <div>
                <label class="text-xs font-semibold text-gray-600 mb-1.5 block">{{ $t('auth.email') }}</label>
                <input
                  v-model="formData.email"
                  type="email"
                  :placeholder="$t('auth.email')"
                  class="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 bg-[#fafafa] text-sm focus:outline-none focus:border-[#10b481] focus:bg-white focus:ring-2 focus:ring-[#10b481]/10 transition-all"
                />
              </div>

              <div>
                <label class="text-xs font-semibold text-gray-600 mb-1.5 block">{{ $t('auth.password') }}</label>
                <div class="relative">
                  <input
                    v-model="formData.password"
                    :type="showPassword ? 'text' : 'password'"
                    :placeholder="$t('auth.password')"
                    class="w-full px-3.5 py-2.5 pr-11 rounded-xl border border-gray-200 bg-[#fafafa] text-sm focus:outline-none focus:border-[#10b481] focus:bg-white focus:ring-2 focus:ring-[#10b481]/10 transition-all"
                  />
                  <button type="button" @click="showPassword = !showPassword" class="absolute right-3.5 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors">
                    <i :class="['bx text-lg', showPassword ? 'bx-hide' : 'bx-show']" />
                  </button>
                </div>
                <!-- Indicateur de force du mot de passe -->
                <div class="mt-1.5 flex gap-1">
                  <div v-for="i in 4" :key="i" :class="[
                    'h-0.5 flex-1 rounded-full transition-all duration-300',
                    passwordStrength >= i ? strengthColor : 'bg-gray-200'
                  ]" />
                </div>
                <p class="text-[10px] text-gray-400 mt-1">{{ $t('auth.passwordHint') }}</p>
              </div>

              <button
                type="submit"
                :disabled="isLoading"
                class="w-full py-3.5 bg-[#10b481] hover:bg-[#0aae74] disabled:opacity-60 disabled:cursor-not-allowed text-white font-bold rounded-xl transition-all duration-200 flex items-center justify-center gap-2 mt-1 shadow-md shadow-[#10b481]/20"
              >
                <span v-if="isLoading" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                <i v-else class="bx bx-user-plus text-lg" />
                {{ isLoading ? $t('auth.creating') : $t('auth.signupBtn') }}
              </button>
            </form>

            <div class="mt-4">
              <div class="flex items-center gap-3 mb-3">
                <hr class="flex-1 border-gray-100" />
                <span class="text-[10px] text-gray-400 font-bold uppercase tracking-widest">{{ $t('auth.or') }}</span>
                <hr class="flex-1 border-gray-100" />
              </div>
              <div id="googleButton" class="w-full cursor-pointer flex items-center justify-center gap-3 py-2.5 rounded-xl border border-gray-200 bg-[#fafafa] hover:bg-white hover:border-gray-300 transition-all">
                <img src="/Google__G__logo.svg.png" alt="Google" class="w-4 h-4" />
                <span class="text-sm text-gray-600 font-medium">{{ $t('auth.googleSignIn') }}</span>
              </div>
            </div>

            <div class="mt-4 flex items-center gap-3">
              <button @click="goBack" class="w-11 h-11 border-2 border-gray-200 text-gray-400 rounded-xl hover:border-gray-300 hover:text-gray-600 transition-all flex items-center justify-center flex-shrink-0">
                <i class="bx bx-left-arrow-alt text-xl" />
              </button>
              <p class="text-xs text-gray-400">
                {{ $t('auth.alreadyAccount') }}
                <NuxtLink :to="localePath('/login')" class="text-[#10b481] font-bold hover:underline ml-1">{{ $t('auth.loginTitle') }}</NuxtLink>
              </p>
            </div>
          </div>

        </Transition>
      </div>

      <!-- Lien connexion (étapes 1 & 2) -->
      <p v-if="currentStep < 3" class="text-center text-sm text-gray-500 mt-5">
        {{ $t('auth.alreadyAccount') }}
        <NuxtLink :to="localePath('/login')" class="text-[#10b481] font-bold hover:underline ml-1">{{ $t('auth.loginTitle') }}</NuxtLink>
      </p>
    </div>

    <!-- ── Notification ──────────────────────────────────────────────────── -->
    <Transition name="fade">
      <div v-if="notification.visible" class="fixed inset-0 flex items-center justify-center z-50 bg-black/20 backdrop-blur-sm">
        <div :class="[
          'bg-white rounded-2xl shadow-2xl px-8 py-6 flex flex-col items-center gap-4 w-[340px] text-center',
          notification.type === 'success' ? 'border-t-4 border-[#10b481]' : 'border-t-4 border-red-500'
        ]">
          <div :class="['w-16 h-16 rounded-full flex items-center justify-center', notification.type === 'success' ? 'bg-[#10b481]' : 'bg-red-500']">
            <i :class="['text-4xl text-white bx', notification.type === 'success' ? 'bx-check' : 'bx-x']" />
          </div>
          <p :class="['text-lg font-semibold', notification.type === 'success' ? 'text-[#10b481]' : 'text-red-500']">
            {{ notification.message }}
          </p>
          <p class="text-gray-500 text-sm">
            {{ notification.type === 'success' ? $t('auth.redirecting') : $t('auth.tryAgain') }}
          </p>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useApi } from '~/composables/useApi'

const { t } = useI18n()
const localePath = useLocalePath()
const authStore  = useAuthStore()
const { apiFetch } = useApi()

// ── Navigation entre étapes ────────────────────────────────────────────────
const currentStep    = ref(1)
const transitionName = ref('slide-forward')

const goNext = () => { transitionName.value = 'slide-forward';  currentStep.value++ }
const goBack = () => { transitionName.value = 'slide-backward'; currentStep.value-- }

const stepLabels = computed(() => [
  t('auth.step1Label'),
  t('auth.step2Label'),
  t('auth.step3Label'),
])

// ── Données ────────────────────────────────────────────────────────────────
const selectedPlan = ref<'FREE' | 'PRO'>('FREE')
const userType     = ref<'farmer' | 'enterprise' | 'buyer' | 'seller'>('buyer')
const showPassword = ref(false)
const formData     = ref({ first_name: '', last_name: '', email: '', password: '' })

// ── Types de compte ────────────────────────────────────────────────────────
const accountTypes = computed(() => [
  { value: 'buyer'      as const, icon: 'bx-shopping-bag', label: t('auth.buyer'),        desc: t('auth.buyerDesc') },
  { value: 'farmer'     as const, icon: 'bx-leaf',         label: t('auth.farmer'),       desc: t('auth.farmerDesc') },
  { value: 'seller'     as const, icon: 'bx-store',        label: t('auth.seller'),       desc: t('auth.sellerDesc') },
  { value: 'enterprise' as const, icon: 'bx-buildings',    label: t('auth.organization'), desc: t('auth.organizationDesc') },
])

const currentAccountType = computed(() => accountTypes.value.find(a => a.value === userType.value))

// ── Features ───────────────────────────────────────────────────────────────
const freeFeatures = computed(() => [t('auth.freeFeature1'), t('auth.freeFeature2'), t('auth.freeFeature3'), t('auth.freeFeature4'), t('auth.freeFeature5'), t('auth.freeFeature6')])
const proFeatures  = computed(() => [t('auth.proFeature1'),  t('auth.proFeature2'),  t('auth.proFeature3'), t('auth.proFeature4'), t('auth.proFeature5'), t('auth.proFeature6')])

// ── Force du mot de passe ──────────────────────────────────────────────────
const passwordStrength = computed(() => {
  const p = formData.value.password
  if (!p) return 0
  let score = 0
  if (p.length >= 8)               score++
  if (/[A-Z]/.test(p))             score++
  if (/[0-9]/.test(p))             score++
  if (/[^A-Za-z0-9]/.test(p))     score++
  return score
})
const strengthColor = computed(() => {
  if (passwordStrength.value <= 1) return 'bg-red-400'
  if (passwordStrength.value === 2) return 'bg-orange-400'
  if (passwordStrength.value === 3) return 'bg-yellow-400'
  return 'bg-[#10b481]'
})

// ── État UI ────────────────────────────────────────────────────────────────
const isLoading    = ref(false)
const googleLoaded = ref(false)
const notification = ref({ visible: false, message: '', type: 'success' as 'success' | 'error' })

const showNotification = (message: string, type: 'success' | 'error' = 'success', duration = 3000) => {
  notification.value = { visible: true, message, type }
  setTimeout(() => (notification.value.visible = false), duration)
}

// ── Soumission ────────────────────────────────────────────────────────────
const handleSignup = async () => {
  const { email, password, first_name, last_name } = formData.value

  if (!email || !password) { showNotification(t('auth.fillFields'), 'error'); return }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { showNotification(t('auth.invalidEmailFormat'), 'error'); return }
  if (password.length < 8) { showNotification(t('auth.passwordTooShort'), 'error'); return }

  isLoading.value = true
  try {
    await apiFetch('/api/signup/', {
      method: 'POST',
      body: {
        username:   email,
        email,
        first_name: first_name || '',
        last_name:  last_name  || '',
        password,
        role:
          userType.value === 'buyer'      ? 'BUYER'      :
          userType.value === 'seller'     ? 'SELLER_PUR' :
          userType.value === 'farmer'     ? 'AGRICULTEUR':
          'ORGANISATION',
        plan: selectedPlan.value,
      },
    })

    showNotification(t('auth.accountCreated'), 'success')

    try {
      const loginData: any = await apiFetch('/api/login/', {
        method: 'POST',
        body: { email, password },
      })
      authStore.setUserData({
        token:    loginData.token,
        uuid:     loginData.user.uuid,
        username: loginData.user.username,
        spaces:   loginData.user.spaces,
      })
      setTimeout(() => navigateTo(userType.value === 'enterprise' ? '/onboarding' : authStore.getWorkspacePath()), 1000)
    } catch {
      setTimeout(() => navigateTo('/login'), 1000)
    }
  } catch (error: any) {
    const isNetworkError =
      (typeof navigator !== 'undefined' && !navigator.onLine) || !error.status ||
      error.name === 'TypeError' || error.message?.toLowerCase().includes('failed to fetch')

    if (isNetworkError) { showNotification(t('auth.networkError'), 'error', 5000); return }

    let msg = t('auth.tryAgain')
    if (error.data?.email) {
      const e = Array.isArray(error.data.email) ? error.data.email[0] : error.data.email
      msg = String(e).toLowerCase().includes('already') ? t('auth.emailAlreadyUsed') : String(e)
    } else if (error.data) {
      const first = Object.values(error.data)[0]
      if (first) msg = Array.isArray(first) ? (first[0] as string) : String(first)
    }
    showNotification(msg, 'error')
  } finally {
    isLoading.value = false
  }
}

// ── Google Auth ────────────────────────────────────────────────────────────
const renderGoogleButton = () => {
  if (!googleLoaded.value || !window.google) return
  window.google.accounts.id.initialize({
    client_id: '186820827638-9915pmkfj0s6ch5tdrc73vakoep2vlsd.apps.googleusercontent.com',
    callback: async (response: any) => {
      try {
        isLoading.value = true
        const data: any = await apiFetch('/api/google-login/', {
          method: 'POST',
          body: {
            token: response.credential,
            role:
              userType.value === 'buyer'      ? 'BUYER'      :
              userType.value === 'seller'     ? 'SELLER_PUR' :
              userType.value === 'farmer'     ? 'AGRICULTEUR':
              'ORGANISATION',
          },
        })
        authStore.setUserData({ token: data.token, uuid: data.user.uuid, username: data.user.username, spaces: data.user.spaces })
        showNotification(t('auth.signInSuccess'), 'success')
        setTimeout(() => navigateTo(userType.value === 'enterprise' ? '/onboarding' : authStore.getWorkspacePath()), 800)
      } catch {
        showNotification(t('auth.googleFailed'), 'error')
      } finally {
        isLoading.value = false
      }
    },
    auto_select: false,
  })
  window.google.accounts.id.renderButton(
    document.getElementById('googleButton'),
    { size: 'large', type: 'standard', shape: 'rectangular', width: '100%', theme: 'outline', text: 'continue_with' }
  )
}

onMounted(() => {
  if (!window.google) {
    const script  = document.createElement('script')
    script.src    = 'https://accounts.google.com/gsi/client'
    script.async  = true
    script.defer  = true
    script.onload = () => { googleLoaded.value = true; renderGoogleButton() }
    document.head.appendChild(script)
  } else {
    googleLoaded.value = true
    renderGoogleButton()
  }
})
</script>

<style scoped>
.slide-forward-enter-active,
.slide-forward-leave-active,
.slide-backward-enter-active,
.slide-backward-leave-active {
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}
.slide-forward-enter-from  { transform: translateX(20px); opacity: 0; }
.slide-forward-leave-to    { transform: translateX(-20px); opacity: 0; }
.slide-backward-enter-from { transform: translateX(-20px); opacity: 0; }
.slide-backward-leave-to   { transform: translateX(20px); opacity: 0; }

.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from,  .fade-leave-to      { opacity: 0; }
</style>
