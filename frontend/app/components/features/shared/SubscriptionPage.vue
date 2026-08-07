<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8 space-y-6">

    <!-- HEADER -->
    <PageHeader :title="t('subscription.title')">
      <template #subtitle>
        <i class="bx bx-crown"></i>
        {{ t('subscription.subtitle') }}
      </template>
      <template #breadcrumb>
        <NuxtLink :to="`/${rolePath}/dashboard`" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
          <span>{{ t('dashboard.dashboard') }}</span>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">{{ t('subscription.sidebarLink') }}</span>
      </template>
    </PageHeader>

    <!-- PLAN ACTUEL -->
    <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
      <div class="flex items-center justify-between flex-wrap gap-4">
        <div class="flex items-center gap-4">
          <div :class="['w-14 h-14 rounded-2xl flex items-center justify-center',
            isPro ? 'bg-amber-50' : 'bg-gray-100']">
            <i :class="['text-2xl', isPro ? 'bx bxs-crown text-amber-500' : 'bx bx-user text-gray-400']"></i>
          </div>
          <div>
            <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest mb-0.5">{{ t('subscription.currentPlan') }}</p>
            <div class="flex items-center gap-2 flex-wrap">
              <span :class="['text-xl font-black', isPro ? 'text-amber-500' : 'text-gray-600']">{{ plan }}</span>
              <span v-if="isPlanExpired"
                class="text-[9px] font-black px-2 py-0.5 rounded-full bg-rose-100 text-rose-600 uppercase tracking-widest">
                {{ t('subscription.expired') }}
              </span>
              <span v-else-if="planDaysLeft !== null && planDaysLeft <= 7 && isPro"
                class="text-[9px] font-black px-2 py-0.5 rounded-full bg-amber-100 text-amber-600 uppercase tracking-widest">
                {{ planDaysLeft }}j restants
              </span>
            </div>
            <p v-if="planExpiresAt && isPro && !isPlanExpired" class="text-xs text-gray-400 mt-0.5">
              {{ t('subscription.expiresOn') }} {{ formatDate(planExpiresAt) }}
            </p>
          </div>
        </div>

        <!-- Statut demande en cours -->
        <div v-if="pendingRequest"
          class="flex items-center gap-2 px-4 py-2.5 bg-amber-50 border border-amber-100 rounded-xl">
          <div class="w-2 h-2 rounded-full bg-amber-400 animate-pulse"></div>
          <span class="text-xs font-bold text-amber-700">{{ t('subscription.pendingRequest') }}</span>
        </div>
      </div>
    </div>

    <!-- COMPARAISON FREE vs PRO -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <!-- FREE -->
      <div :class="['bg-white rounded-2xl border shadow-sm p-6 space-y-4 transition-all',
        isFree && !isPlanExpired ? 'border-[#112830] ring-2 ring-[#112830]/10' : 'border-gray-100']">
        <div class="flex items-center justify-between">
          <div>
            <span class="text-xs font-black text-gray-400 uppercase tracking-widest">{{ t('subscription.freePlan') }}</span>
            <p class="text-2xl font-black text-[#112830] mt-0.5">{{ t('subscription.free') }}</p>
          </div>
          <div v-if="isFree && !isPlanExpired"
            class="px-2 py-1 bg-[#112830] text-white text-[9px] font-black rounded-lg uppercase tracking-widest">
            {{ t('subscription.currentBadge') }}
          </div>
        </div>
        <ul class="space-y-2.5">
          <li v-for="f in freeFeatures" :key="f.label" class="flex items-start gap-2.5 text-sm text-gray-600">
            <i :class="['bx text-base flex-shrink-0 mt-0.5', f.included ? 'bx-check-circle text-[#10b481]' : 'bx-x-circle text-gray-300']"></i>
            <span :class="f.included ? '' : 'text-gray-400'">{{ f.label }}</span>
          </li>
        </ul>
      </div>

      <!-- PRO -->
      <div :class="['bg-white rounded-2xl border shadow-sm p-6 space-y-4 transition-all relative overflow-hidden',
        isPro && !isPlanExpired ? 'border-amber-400 ring-2 ring-amber-400/20' : 'border-amber-200']">
        <div class="absolute top-0 right-0 px-4 py-1.5 bg-amber-400 text-white text-[9px] font-black uppercase tracking-widest rounded-bl-xl">
          {{ t('subscription.recommended') }}
        </div>
        <div class="flex items-center justify-between">
          <div>
            <span class="text-xs font-black text-amber-500 uppercase tracking-widest">{{ t('subscription.proPlan') }}</span>
            <p class="text-2xl font-black text-[#112830] mt-0.5">
              {{ t('subscription.proPrice') }}
              <span class="text-sm font-semibold text-gray-400">/{{ t('subscription.month') }}</span>
            </p>
          </div>
          <div v-if="isPro && !isPlanExpired"
            class="px-2 py-1 bg-amber-400 text-white text-[9px] font-black rounded-lg uppercase tracking-widest">
            {{ t('subscription.currentBadge') }}
          </div>
        </div>
        <ul class="space-y-2.5">
          <li v-for="f in proFeatures" :key="f" class="flex items-start gap-2.5 text-sm text-gray-600">
            <i class="bx bx-check-circle text-amber-500 text-base flex-shrink-0 mt-0.5"></i>
            <span>{{ f }}</span>
          </li>
        </ul>
      </div>
    </div>

    <!-- FORMULAIRE D'UPGRADE / RENOUVELLEMENT -->
    <div v-if="!pendingRequest" class="bg-white rounded-2xl border border-gray-100 shadow-sm p-6 space-y-5">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 bg-amber-50 rounded-xl flex items-center justify-center flex-shrink-0">
          <i class="bx bxs-crown text-amber-500 text-lg"></i>
        </div>
        <div>
          <h2 class="text-base font-black text-[#112830]">
            {{ isPro && !isPlanExpired ? t('subscription.renewTitle') : t('subscription.upgradeTitle') }}
          </h2>
          <p class="text-xs text-gray-400">
            {{ isPro && !isPlanExpired ? t('subscription.renewSubtitle') : t('subscription.upgradeSubtitle') }}
          </p>
        </div>
      </div>

      <!-- Durée -->
      <div class="space-y-2">
        <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest block">{{ t('subscription.duration') }}</label>
        <div class="flex flex-wrap gap-2">
          <button v-for="d in durationOptions" :key="d.days"
            @click="form.duration_days = d.days"
            :class="['px-4 py-2.5 rounded-xl text-xs font-bold border transition-all',
              form.duration_days === d.days
                ? 'bg-[#112830] text-white border-[#112830]'
                : 'bg-gray-50 text-gray-500 border-gray-100 hover:border-gray-300']">
            {{ d.label }}
            <span v-if="d.savings" class="ml-1.5 text-[9px] opacity-70">{{ d.savings }}</span>
          </button>
        </div>
      </div>

      <!-- Stratégie de paiement -->
      <div class="space-y-2">
        <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest block">{{ t('subscription.paymentMethod') }}</label>
        <div class="flex flex-wrap gap-3 justify-start">
          <label
            v-for="method in paymentMethods"
            :key="method.id"
            :class="[
              'flex-none min-w-[120px] max-w-[180px] relative border-2 p-3 sm:p-4 rounded-3xl cursor-pointer transition-all flex flex-col items-center gap-3',
              form.provider === method.id ? 'border-[#10b481] bg-emerald-50/50' : 'border-gray-100 bg-white hover:border-gray-300'
            ]"
          >
            <input type="radio" class="absolute opacity-0 inset-0 cursor-pointer" v-model="form.provider" :value="method.id" />
            <div :class="form.provider === method.id ? 'border-[#10b481] bg-white' : 'border-gray-100 bg-white'" class="w-14 h-14 rounded-3xl flex items-center justify-center transition-all overflow-hidden">
              <img v-if="method.logo" :src="method.logo" :alt="method.name" class="max-h-10 max-w-full object-contain" />
              <i v-else :class="method.icon" class="text-2xl"></i>
            </div>
            <div class="text-center">
              <p class="font-black text-sm text-[#112830]">{{ method.name }}</p>
              <p class="text-[10px] text-gray-400 font-bold uppercase tracking-widest">{{ method.sub }}</p>
            </div>
            <i v-if="form.provider === method.id" class="bx bxs-check-circle absolute top-4 right-4 text-[#10b481] text-xl"></i>
          </label>
        </div>
      </div>

      <!-- Instructions paiement (Si Mobile Money) -->
      <div v-if="form.provider && isMobileMoney" class="p-4 bg-blue-50 border border-blue-100 rounded-xl space-y-3">
        <p class="text-xs font-black text-blue-700">{{ t('subscription.paymentInstructions') }}</p>
        <p class="text-xs text-blue-600 leading-relaxed">
          {{ paymentInstructions }}
        </p>
        <div class="rounded-2xl bg-white p-3 border border-blue-100 text-xs text-slate-700 space-y-2">
          <div class="flex items-center justify-between gap-3">
            <span class="font-black">USSD</span>
            <span class="font-semibold text-[#112830]">{{ selectedPaymentMethod?.ussdCode }}</span>
          </div>
          <div class="flex items-center justify-between gap-3">
            <span class="font-black">{{ t('subscription.recipient') }}</span>
            <span class="text-[#112830]">{{ selectedPaymentMethod?.recipientName }}</span>
          </div>
          <div class="flex items-center justify-between gap-3">
            <span class="font-black">{{ t('subscription.recipientNumber') }}</span>
            <span class="text-[#112830]">{{ selectedPaymentMethod?.recipientNumber }}</span>
          </div>
        </div>
        <p class="text-xs font-bold text-blue-700 mt-2">
          {{ t('subscription.amount') }} : <span class="text-base">{{ selectedPrice }}</span> MGA
        </p>
      </div>

      <!-- FORMULAIRE STRIPE (Paiement Carte Bancaire) -->
      <div v-if="isStripe" class="space-y-3 p-4 border border-gray-100 bg-gray-50/50 rounded-xl">
        <div>
          <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest block">
            Informations de la carte bancaire <span class="text-rose-400">*</span>
          </label>
          <p class="text-xs text-gray-500 mt-0.5 flex items-center gap-1">
            <i class="bx bx-info-circle text-gray-400"></i>
            Saisissez votre numéro de carte, la date d'expiration et le code CVC.
          </p>
        </div>

        <!-- Element Stripe Mount Point -->
        <div class="p-3.5 bg-white border border-gray-200 rounded-xl shadow-sm focus-within:ring-2 focus-within:ring-[#10b481]/20 focus-within:border-[#10b481]">
          <div ref="stripeCardMount"></div>
        </div>
        <p v-if="stripeError" class="text-xs text-rose-500 font-medium flex items-center gap-1">
          <i class="bx bx-error-circle"></i> {{ stripeError }}
        </p>
      </div>

      <!-- CHAMPS MOBILE MONEY (Nom, Tel, Réf) -->
      <template v-if="isMobileMoney">
        <!-- Nom du titulaire -->
        <div class="space-y-2">
          <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest block">
            {{ t('subscription.accountHolderName') }} <span class="text-rose-400">*</span>
          </label>
          <input v-model="form.sender_name" type="text" :placeholder="t('subscription.accountHolderNamePlaceholder')"
            class="w-full px-4 py-3 bg-gray-50 border border-gray-100 rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/30 focus:bg-white transition-all font-medium" />
        </div>

        <!-- Numéro de téléphone -->
        <div class="space-y-2">
          <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest block">
            {{ t('subscription.yourPhone') }} <span class="text-rose-400">*</span>
          </label>
          <div class="relative">
            <i class="bx bx-phone absolute left-4 top-1/2 -translate-y-1/2 text-gray-300 text-lg pointer-events-none"></i>
            <input v-model="form.phone" type="tel" placeholder="034 XX XXX XX"
              class="w-full pl-11 pr-4 py-3 bg-gray-50 border border-gray-100 rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/30 focus:bg-white transition-all font-medium" />
          </div>
        </div>

        <!-- Référence de paiement Mobile Money -->
        <div class="space-y-2">
          <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest block">
            {{ t('subscription.paymentRef') }} <span class="text-rose-400">*</span>
          </label>
          <div class="relative">
            <i class="bx bx-receipt absolute left-4 top-1/2 -translate-y-1/2 text-gray-300 text-lg pointer-events-none"></i>
            <input v-model="form.payment_ref" type="text" :placeholder="t('subscription.paymentRefPlaceholder')"
              class="w-full pl-11 pr-4 py-3 bg-gray-50 border border-gray-100 rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/30 focus:bg-white transition-all font-medium" />
          </div>
          <p class="text-[10px] text-gray-400">{{ t('subscription.paymentRefHelp') }}</p>
        </div>
      </template>

      <!-- Submit Button -->
      <button @click="submitRequest"
        :disabled="isSubmitting || !isFormValid || (isStripe && (!stripeCardReady || !!stripeError))"
        class="w-full py-3.5 bg-[#112830] text-white rounded-xl font-bold text-sm hover:bg-[#10b481] transition-all flex items-center justify-center gap-2 disabled:opacity-40 disabled:cursor-not-allowed">
        <div v-if="isSubmitting" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
        <template v-else>
          <i class="bx bxs-crown text-amber-300 text-base"></i>
          {{ isStripe ? `Payer ${selectedPrice} MGA` : t('subscription.submitRequest') }}
        </template>
      </button>
    </div>

    <!-- DEMANDE EN ATTENTE -->
    <div v-if="pendingRequest" class="bg-amber-50 border border-amber-200 rounded-2xl p-6 flex items-start gap-4">
      <div class="w-11 h-11 bg-amber-100 rounded-xl flex items-center justify-center flex-shrink-0">
        <i class="bx bx-time text-amber-600 text-xl"></i>
      </div>
      <div class="flex-1">
        <h3 class="text-sm font-black text-amber-800">{{ t('subscription.pendingTitle') }}</h3>
        <p class="text-xs text-amber-700 mt-1">{{ t('subscription.pendingDesc') }}</p>
        <div class="mt-3 flex flex-wrap gap-3 text-xs text-amber-700">
          <span class="flex items-center gap-1"><i class="bx bx-money-withdraw"></i> {{ pendingRequest.provider }}</span>
          <span class="flex items-center gap-1"><i class="bx bx-receipt"></i> Réf : {{ pendingRequest.payment_ref }}</span>
          <span class="flex items-center gap-1"><i class="bx bx-calendar"></i> {{ formatDate(new Date(pendingRequest.started_at)) }}</span>
        </div>
      </div>
    </div>

    <!-- TOAST NOTIFICATION -->
    <Transition name="pop-notification">
      <div v-if="notif.visible" class="fixed top-6 left-1/2 -translate-x-1/2 z-[200] w-full max-w-sm px-4">
        <div :class="['bg-white rounded-2xl shadow-xl p-5 flex items-center gap-4 border',
          notif.type === 'success' ? 'border-l-4 border-l-[#10b481] border-gray-100' : 'border-l-4 border-l-rose-500 border-gray-100']">
          <div :class="['w-10 h-10 rounded-xl flex items-center justify-center text-xl flex-shrink-0',
            notif.type === 'success' ? 'bg-emerald-50 text-[#10b481]' : 'bg-rose-50 text-rose-500']">
            <i :class="notif.type === 'success' ? 'bx bx-check-circle' : 'bx bx-error-circle'"></i>
          </div>
          <p class="text-sm font-bold text-[#112830]">{{ notif.message }}</p>
        </div>
      </div>
    </Transition>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount, reactive, watch, nextTick } from 'vue'
import { loadStripe, type Stripe } from '@stripe/stripe-js'
import { useApi } from '~/composables/useApi'
import { usePlan } from '~/composables/usePlan'

const props = defineProps<{ rolePath: string }>()

const { t } = useI18n()
const { apiFetch } = useApi()
const { plan, isPro, isFree, planExpiresAt, isPlanExpired, planDaysLeft } = usePlan()

// Clé publique Stripe : reprise via runtimeConfig, comme dans la page checkout
// (à définir dans nuxt.config.ts -> runtimeConfig.public.stripePublishableKey
// et dans les variables d'environnement, ex: NUXT_PUBLIC_STRIPE_PUBLISHABLE_KEY)
const runtimeConfig = useRuntimeConfig()
const stripePublishableKey = runtimeConfig.public.stripePublishableKey || ''
let stripePromise: Promise<Stripe | null> | null = null

const isSubmitting = ref(false)
const pendingRequest = ref<any>(null)
const notif = ref({ visible: false, message: '', type: 'success' as 'success' | 'error' })

// --- Stripe state (aligné sur la page checkout) ---
const stripeInstance = ref<Stripe | null>(null)
const stripeElements = ref<any>(null)
const stripeCardElement = ref<any>(null)
const stripeCardMount = ref<HTMLDivElement | null>(null)
const stripeCardReady = ref(false)
const isCardComplete = ref(false)
const stripeError = ref<string | null>(null)

const form = reactive({
  provider: '',
  phone: '',
  sender_name: '',
  payment_ref: '',
  duration_days: 30,
})

const durationOptions = [
  { days: 30,  label: '1 mois',   savings: '' },
  { days: 90,  label: '3 mois',   savings: '-5%' },
  { days: 180, label: '6 mois',   savings: '-10%' },
  { days: 365, label: '1 an',     savings: '-20%' },
]

const paymentMethods = [
  {
    id: 'MVOLA',
    name: 'MVola',
    sub: 'Mobile Money',
    icon: 'bx bx-phone-incoming',
    isMobile: true,
    number: '034 XX XXX XX',
    ussdCode: '#111*1*1*[VOTRE_NUMÉRO_MVOLA]*[MONTANT]#',
    recipientName: 'SmartSaha',
    recipientNumber: '034 XX XXX XX',
    logo: '/payment-logos/mvola.jpg',
  },
  {
    id: 'ORANGE_MONEY',
    name: 'Orange Money',
    sub: 'Mobile Money',
    icon: 'bx bx-phone-incoming',
    isMobile: true,
    number: '032 XX XXX XX',
    ussdCode: '#144*1*[VOTRE_NUMÉRO_OM]*[MONTANT]#',
    recipientName: 'SmartSaha',
    recipientNumber: '032 XX XXX XX',
    logo: '/payment-logos/orange-money.png',
  },
  {
    id: 'AIRTEL_MONEY',
    name: 'Airtel Money',
    sub: 'Mobile Money',
    icon: 'bx bx-phone-incoming',
    isMobile: true,
    number: '033 XX XXX XX',
    ussdCode: '#436*1*[VOTRE_NUMÉRO_AIRTEL]*[MONTANT]#',
    recipientName: 'SmartSaha',
    recipientNumber: '033 XX XXX XX',
    logo: '/payment-logos/airtel-money.jpg',
  },
  { id: 'STRIPE', name: 'Carte bancaire', sub: 'Visa / Mastercard', logo: '/payment-logos/stripe.png', isMobile: false },
]

const PRICES: Record<number, number> = { 30: 15000, 90: 42750, 180: 81000, 365: 144000 }
const selectedPrice = computed(() => PRICES[form.duration_days] ?? 15000)

const selectedPaymentMethod = computed(() => paymentMethods.find(method => method.id === form.provider) ?? null)
const isMobileMoney = computed(() => selectedPaymentMethod.value?.isMobile ?? false)
const isStripe = computed(() => form.provider === 'STRIPE')

const paymentInstructions = computed(() => {
  if (!selectedPaymentMethod.value) return ''
  if (selectedPaymentMethod.value.isMobile) {
    return t('subscription.mobileMoneyInstructions', {
      number: selectedPaymentMethod.value.number,
      amount: selectedPrice.value,
    })
  }
  return ''
})

const isFormValid = computed(() => {
  if (!form.provider) return false
  if (isMobileMoney.value) {
    return !!(form.payment_ref && form.phone && form.sender_name)
  }
  if (isStripe.value) {
    return isCardComplete.value
  }
  return false
})

// --- Initialisation et montage de l'élément carte Stripe ---
// Reprend le pattern de la page checkout : instance chargée une seule fois,
// élément recréé proprement si on quitte puis revient sur STRIPE.
async function setupStripeElements() {
  await nextTick()

  if (!stripeCardMount.value) return

  if (!stripePublishableKey) {
    stripeError.value = 'Clé publique Stripe non configurée.'
    return
  }

  if (!stripePromise) {
    stripePromise = loadStripe(stripePublishableKey)
  }

  const stripe = await stripePromise
  if (!stripe) {
    stripeError.value = 'Impossible de charger Stripe.'
    return
  }

  stripeInstance.value = stripe
  stripeElements.value = stripe.elements()

  if (stripeCardElement.value?.destroy) {
    stripeCardElement.value.destroy()
    stripeCardElement.value = null
  }
  stripeCardMount.value.innerHTML = ''
  stripeCardReady.value = false

  const card = stripeElements.value.create('card', {
    hidePostalCode: true,
    style: {
      base: {
        fontSize: '14px',
        color: '#112830',
        fontFamily: 'sans-serif',
        '::placeholder': { color: '#9ca3af' },
      },
      invalid: { color: '#f43f5e' },
    },
  })

  card.mount(stripeCardMount.value)
  stripeCardElement.value = card

  card.on('ready', () => {
    stripeCardReady.value = true
  })
  card.on('change', (event: any) => {
    isCardComplete.value = event.complete
    stripeError.value = event.error ? event.error.message : null
  })
}

// Attendre que l'élément carte soit réellement prêt avant de lancer la confirmation
async function waitForStripeCardReady() {
  if (stripeCardReady.value) return

  await new Promise<void>((resolve, reject) => {
    const timeout = setTimeout(() => {
      reject(new Error('Le formulaire de paiement Stripe n’est pas prêt après attente.'))
    }, 15000)

    const stop = watch(stripeCardReady, (ready) => {
      if (ready) {
        clearTimeout(timeout)
        stop()
        resolve()
      }
    })
  })
}

onBeforeUnmount(() => {
  if (stripeCardElement.value?.destroy) {
    stripeCardElement.value.destroy()
  }
})

watch(() => form.provider, async (newProvider) => {
  if (newProvider === 'STRIPE') {
    await setupStripeElements()
  }
})

const freeFeatures = computed(() => [
  { label: t('subscription.feature.parcels3'), included: true },
  { label: t('subscription.feature.surface2000'), included: true },
  { label: t('subscription.feature.crops'), included: true },
  { label: t('subscription.feature.aiChat'), included: true },
  { label: t('subscription.feature.unlimitedParcels'), included: false },
  { label: t('subscription.feature.unlimitedSurface'), included: false },
  { label: t('subscription.feature.advancedAnalytics'), included: false },
  { label: t('subscription.feature.prioritySupport'), included: false },
])

const proFeatures = computed(() => [
  t('subscription.feature.parcels3'),
  t('subscription.feature.surface2000'),
  t('subscription.feature.crops'),
  t('subscription.feature.aiChat'),
  t('subscription.feature.unlimitedParcels'),
  t('subscription.feature.unlimitedSurface'),
  t('subscription.feature.advancedAnalytics'),
  t('subscription.feature.prioritySupport'),
])

function formatDate(d: Date | null): string {
  if (!d) return ''
  return new Date(d).toLocaleDateString('fr-FR', { day: '2-digit', month: 'long', year: 'numeric' })
}

function showNotif(message: string, type: 'success' | 'error') {
  notif.value = { visible: true, message, type }
  setTimeout(() => (notif.value.visible = false), 5000)
}

async function fetchMySubscription() {
  try {
    const data: any = await apiFetch('/api/mobile/payments/my-subscription/')
    if (data?.status === 'PENDING') pendingRequest.value = data
    else pendingRequest.value = null
  } catch (_) {}
}

async function submitRequest() {
  if (!isFormValid.value) {
    showNotif(t('subscription.errorRequest'), 'error')
    return
  }

  isSubmitting.value = true
  stripeError.value = null

  try {
    if (isStripe.value) {
      // 1. Créer le PaymentIntent Stripe pour cet abonnement → renvoie le client_secret
      const res: any = await apiFetch('/api/mobile/payments/subscription-payment-intent/', {
        method: 'POST',
        body: {
          duration_days: form.duration_days,
        },
      })

      const clientSecret = res?.client_secret
      const paymentIntentId = res?.payment_intent_id

      if (!clientSecret) {
        throw new Error('Impossible d’obtenir le secret d’intention de paiement de Stripe.')
      }

      // 2. S'assurer que l'élément carte est bien monté et prêt avant de confirmer
      if (!stripeInstance.value || !stripeCardElement.value) {
        await setupStripeElements()
      }
      await waitForStripeCardReady()

      // 3. Confirmer le paiement avec la carte saisie
      const { paymentIntent, error } = await stripeInstance.value!.confirmCardPayment(clientSecret, {
        payment_method: {
          card: stripeCardElement.value,
        },
      })

      if (error) {
        stripeError.value = error.message || 'Erreur lors de la validation du paiement.'
        showNotif(error.message || t('subscription.errorRequest'), 'error')
        return
      }

      if (paymentIntent?.status === 'succeeded') {
        // 4. Confirmer côté backend pour activer immédiatement le plan PRO
        //    (filet de sécurité en plus du webhook Stripe)
        await apiFetch('/api/mobile/payments/subscription-confirm-stripe/', {
          method: 'POST',
          body: { payment_intent_id: paymentIntent.id || paymentIntentId },
        })
        showNotif('Paiement effectué avec succès !', 'success')
      } else {
        showNotif(`Paiement non finalisé (${paymentIntent?.status || 'statut inconnu'}).`, 'error')
        return
      }
    } else {
      // Soumission standard pour Mobile Money
      await apiFetch('/api/mobile/payments/subscription-request/', {
        method: 'POST',
        body: {
          provider: form.provider,
          phone: form.phone || undefined,
          sender_name: form.sender_name || undefined,
          payment_ref: form.payment_ref,
          duration_days: form.duration_days,
        },
      })
      showNotif(t('subscription.successRequest'), 'success')
    }

    await fetchMySubscription()
  } catch (err: any) {
    const msg = err?.data?.detail || err?.data?.sender_name?.[0] || err?.data?.payment_ref?.[0] || err?.data?.phone?.[0] || err?.message
    showNotif(msg || t('subscription.errorRequest'), 'error')
  } finally {
    isSubmitting.value = false
  }
}

onMounted(() => fetchMySubscription())
</script>

<style scoped>
.pop-notification-enter-active, .pop-notification-leave-active {
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.pop-notification-enter-from, .pop-notification-leave-to {
  opacity: 0;
  transform: translate(-50%, -16px) scale(0.92);
}
</style>