<template>
  <div class="max-w-4xl mx-auto space-y-8">
    <!-- Back & Header -->
    <div class="space-y-4">
      <button @click="router.back()" class="flex items-center gap-2 text-xs font-black text-gray-400 uppercase tracking-widest hover:text-[#10b481] transition-colors">
        <i class="bx bx-left-arrow-alt text-xl"></i>
        Retour
      </button>
      <h1 class="text-3xl font-black text-[#112830]">Finaliser le paiement</h1>
      <p class="text-gray-500 font-medium">
        {{ orderDetail?.checkout_orders?.length > 1 ? `Paiement groupé · ${orderDetail.checkout_orders.length} commandes` : `Commande ${orderDetail?.order_number}` }}
      </p>
    </div>

    <div v-if="loading && !orderDetail" class="bg-white p-12 rounded-[3rem] border border-gray-100 flex items-center justify-center">
      <i class="bx bx-loader-alt animate-spin text-4xl text-[#10b481]"></i>
    </div>

    <div v-else-if="error" class="bg-white p-12 rounded-[3rem] border border-red-100 text-center space-y-4">
      <i class="bx bx-error-circle text-5xl text-red-500"></i>
      <h2 class="text-xl font-black text-[#112830]">Une erreur est survenue</h2>
      <p class="text-gray-500">{{ error }}</p>
      <button @click="fetchOrderDetail(route.params.id as string)" class="px-8 py-3 bg-[#112830] text-white rounded-2xl font-black text-xs uppercase tracking-widest">
        Réessayer
      </button>
    </div>

    <div v-else-if="!orderDetail" class="bg-white p-12 rounded-[3rem] border border-gray-100 text-center space-y-4">
      <i class="bx bx-search text-5xl text-gray-200"></i>
      <h2 class="text-xl font-black text-[#112830]">Commande introuvable</h2>
      <p class="text-gray-500">Nous n'avons pas pu charger les détails de cette commande.</p>
    </div>

    <div v-else-if="orderDetail" class="grid grid-cols-1 md:grid-cols-2 gap-8">
      <!-- Left: Order Summary -->
      <div class="bg-white p-8 rounded-[3rem] border border-gray-100 shadow-sm space-y-6 h-fit">
        <h3 class="text-lg font-black text-[#112830]">Résumé de la commande</h3>
        
        <div class="space-y-4">
          <div v-for="item in orderDetail?.items || []" :key="item.id" class="flex gap-4 items-center">
            <div class="w-12 h-12 bg-gray-50 rounded-xl overflow-hidden flex-shrink-0 border border-gray-100">
              <img v-if="item.product_image" :src="item.product_image" class="w-full h-full object-cover" />
              <i v-else class="bx bx-image text-gray-300 text-xl m-auto"></i>
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-black text-[#112830] truncate">{{ item.product_name }}</p>
              <p class="text-xs font-bold text-gray-400">Qté: {{ item.quantity }} x {{ item.price }} Ar</p>
            </div>
            <p class="text-sm font-black text-[#112830]">{{ item.subtotal }} Ar</p>
          </div>
        </div>

        <div class="pt-6 border-t border-gray-50 space-y-2">
          <div class="flex justify-between text-sm">
            <span class="text-gray-400 font-bold">Sous-total</span>
            <span class="text-[#112830] font-black">{{ orderDetail?.subtotal }} Ar</span>
          </div>
          <div class="flex justify-between text-sm">
            <span class="text-gray-400 font-bold">Livraison</span>
            <span class="text-[#112830] font-black">{{ orderDetail?.delivery_fee }} Ar</span>
          </div>
          <div class="flex justify-between text-2xl pt-4">
            <span class="text-[#112830] font-black">{{ orderDetail?.checkout_orders?.length > 1 ? 'Total à payer' : 'Total' }}</span>
            <span class="text-[#10b481] font-black">{{ orderDetail?.checkout_total ?? orderDetail?.total }} Ar</span>
          </div>
        </div>
        <div v-if="orderDetail?.checkout_orders?.length > 1" class="rounded-2xl border border-sky-100 bg-sky-50 p-4 text-xs text-sky-800">
          <p class="font-black">Paiement unique pour {{ orderDetail.checkout_orders.length }} vendeurs</p>
          <p class="mt-1">Chaque vendeur recevra et suivra uniquement sa propre commande après confirmation du paiement.</p>
        </div>
      </div>

      <!-- Right: Payment Form -->
      <div class="bg-[#112830] p-8 rounded-[3rem] shadow-xl shadow-[#112830]/20 space-y-8">
        <div class="flex items-center gap-3">
          <div class="w-12 h-12 bg-[#10b481] text-white rounded-2xl flex items-center justify-center text-2xl shadow-lg shadow-[#10b481]/20">
            <i class="bx bx-wallet"></i>
          </div>
          <h3 class="text-lg font-black text-white">Moyen de paiement</h3>
        </div>

        <div class="space-y-4">
          <div class="p-4 border border-gray-700 rounded-3xl bg-[#112830]/50 flex items-center gap-4">
            <div class="w-12 h-12 rounded-2xl bg-[#10b481] text-white flex items-center justify-center text-2xl">
              <i :class="currentPaymentMethod?.icon"></i>
            </div>
            <div>
              <p class="text-sm font-black text-white">{{ currentPaymentMethod?.label || orderDetail?.payment_method }}</p>
              <p class="text-[10px] text-gray-400 uppercase tracking-[0.2em]">Mode de paiement choisi</p>
            </div>
          </div>
          <p class="text-[10px] text-gray-400 leading-relaxed">
            Ce mode de paiement a été défini lors de la création de la commande. Vous ne pouvez pas le modifier ici.
          </p>
        </div>

        <div v-if="isMobileMoney" class="space-y-4">
          <div class="rounded-2xl border border-amber-300/20 bg-amber-300/10 p-4 text-amber-50">
            <div class="flex gap-3">
              <i class="bx bx-info-circle mt-0.5 text-xl text-amber-300"></i>
              <div class="space-y-2 text-xs leading-relaxed">
                <p class="font-black uppercase tracking-wider text-amber-200">Instructions de paiement {{ currentPaymentMethod?.label }}</p>
                <p>Composez le code ci-dessous sur votre téléphone, effectuez le paiement du montant indiqué, puis renseignez les informations reçues par SMS.</p>
                <code class="block rounded-xl bg-black/20 px-3 py-2 font-black tracking-wide text-amber-100">{{ currentPaymentMethod?.ussdCode }}</code>
                <p class="text-amber-100/80">Remplacez <strong>[MONTANT]</strong> par le total à payer et utilisez le numéro marchand communiqué par SmartSaha.</p>
              </div>
            </div>
          </div>
          <div class="space-y-2">
            <label class="text-[10px] font-black text-gray-400 uppercase tracking-[0.2em]">Nom du titulaire du compte</label>
            <input
              v-model="senderName"
              type="text"
              placeholder="Nom associé au compte mobile money"
              class="w-full bg-[#152e37] border-2 border-gray-700 rounded-2xl py-4 px-4 text-white font-black placeholder:text-gray-600 focus:border-[#10b481] transition-all outline-none"
            />
          </div>
          <div class="space-y-2">
            <label class="text-[10px] font-black text-gray-400 uppercase tracking-[0.2em]">Numéro qui a envoyé l'argent</label>
            <div class="relative">
              <i class="bx bx-phone absolute left-4 top-1/2 -translate-y-1/2 text-gray-500"></i>
              <input 
                v-model="senderPhone"
                type="tel" 
                placeholder="034 XX XXX XX"
                class="w-full bg-[#152e37] border-2 border-gray-700 rounded-2xl py-4 pl-12 pr-4 text-white font-black placeholder:text-gray-600 focus:border-[#10b481] transition-all outline-none"
              />
            </div>
          </div>
          <div class="space-y-2">
            <label class="text-[10px] font-black text-gray-400 uppercase tracking-[0.2em]">Référence de la transaction</label>
            <input
              v-model="transactionReference"
              type="text"
              placeholder="Référence reçue par SMS"
              class="w-full bg-[#152e37] border-2 border-gray-700 rounded-2xl py-4 px-4 text-white font-black placeholder:text-gray-600 focus:border-[#10b481] transition-all outline-none"
            />
          </div>
        </div>

        <div v-if="orderDetail?.payment_method === 'STRIPE'" class="space-y-4">
          <div class="space-y-2">
            <label class="text-[10px] font-black text-gray-400 uppercase tracking-[0.2em]">Informations de la carte</label>
            <div ref="stripeElementHolder" class="w-full bg-[#152e37] border-2 border-gray-700 rounded-2xl p-4 text-white">
              <div ref="stripeCardMount" class="h-16 rounded-2xl bg-[#0f373f] px-3 py-3"></div>
            </div>
          </div>
          <div class="flex gap-3 rounded-2xl border border-sky-400/20 bg-sky-400/10 p-4 text-sky-100">
            <i class="bx bx-info-circle mt-0.5 text-lg text-sky-300"></i>
            <div class="space-y-1 text-xs leading-relaxed">
              <p class="font-black uppercase tracking-wider text-sky-200">Instructions de paiement</p>
              <p>Saisissez le <strong>numéro de carte</strong>, puis l'<strong>expiration (MM/AA)</strong> et le <strong>CVC</strong> dans le champ ci-dessus.</p>
              <p class="text-sky-200/80">Exemple de test : 4242 4242 4242 4242 · 12/29 · 123</p>
            </div>
          </div>
          <div v-if="stripeError" class="p-4 bg-rose-500/10 border border-rose-500/20 rounded-2xl text-rose-600 text-sm font-bold">
            {{ stripeError }}
          </div>
        </div>

        <div v-if="paymentError" class="mb-4 p-4 bg-rose-500/10 border border-rose-500/20 rounded-2xl text-rose-600 text-sm font-bold">
          {{ paymentError }}
        </div>

        <button 
          type="button"
          @click="handlePayment"
          :disabled="paymentLoading || loading || (isMobileMoney && !isPaymentValid) || (orderDetail?.payment_method === 'STRIPE' && (!stripeCardReady || !!stripeError))"
          class="w-full py-5 bg-[#10b481] text-white rounded-2xl font-black text-xs uppercase tracking-[0.2em] shadow-lg shadow-[#10b481]/20 hover:bg-[#0da072] active:scale-95 transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <i v-if="paymentLoading" class="bx bx-loader-alt animate-spin text-lg"></i>
          <span v-else>Confirmer le règlement</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, onBeforeUnmount, nextTick } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { loadStripe } from '@stripe/stripe-js';
import { useMarketplace } from '~/composables/useMarketplace';

const { t } = useI18n();
const runtimeConfig = useRuntimeConfig();
const stripePublishableKey = runtimeConfig.public.stripePublishableKey || '';
let stripePromise: Promise<any> | null = null;
definePageMeta({
  layout: 'dashboard'
});

const route = useRoute();
const router = useRouter();
const { orderDetail, loading, error, fetchOrderDetail, initiatePayment, createStripePaymentIntent, confirmStripePaymentIntent } = useMarketplace();

const paymentLoading = ref(false);
const paymentError = ref<string | null>(null);
const stripeError = ref<string | null>(null);
const stripeElementHolder = ref<HTMLDivElement | null>(null);
const stripeInstance = ref<any>(null);
const stripeElements = ref<any>(null);
const stripeCardElement = ref<any>(null);
const stripeCardMount = ref<HTMLDivElement | null>(null);
const stripeCardReady = ref(false);

const selectedMethod = ref('MVOLA');
const senderPhone = ref('');
const senderName = ref('');
const transactionReference = ref('');

const paymentMethods = [
  { id: 'MVOLA', label: 'MVola', icon: 'bx bx-phone-incoming', isMobile: true, ussdCode: '#111*1*1*[NUMERO_MARCHAND]*[MONTANT]#' },
  { id: 'ORANGE_MONEY', label: 'Orange Money', icon: 'bx bx-phone-incoming', isMobile: true, ussdCode: '#144*1*[NUMERO_MARCHAND]*[MONTANT]#' },
  { id: 'AIRTEL_MONEY', label: 'Airtel Money', icon: 'bx bx-phone-incoming', isMobile: true, ussdCode: '#436*1*[NUMERO_MARCHAND]*[MONTANT]#' },
  { id: 'TEST', label: 'Mode Démo / Test', icon: 'bx bx-vial', isMobile: false },
  { id: 'STRIPE', label: 'Carte Bancaire', icon: 'bx bxl-stripe', isMobile: false },
];

const currentPaymentMethod = computed(() => {
  return paymentMethods.find(m => m.id === selectedMethod.value) ?? null;
});

const isMobileMoney = computed(() => {
  return currentPaymentMethod.value?.isMobile ?? false;
});

const isPaymentValid = computed(() => {
  if (!isMobileMoney.value) {
    return true;
  }
  return !!(senderPhone.value && senderName.value && transactionReference.value);
});

const setupStripeElements = async () => {
  if (!orderDetail.value || orderDetail.value.payment_method !== 'STRIPE') {
    return;
  }

  await nextTick();

  if (!stripeElementHolder.value) {
    return;
  }

  if (!stripePublishableKey) {
    stripeError.value = 'Clé publique Stripe non configurée.';
    return;
  }

  if (!stripePromise) {
    stripePromise = loadStripe(stripePublishableKey);
  }

  const stripe = await stripePromise;
  if (!stripe) {
    stripeError.value = 'Impossible de charger Stripe.';
    return;
  }

  stripeInstance.value = stripe;
  stripeElements.value = stripe.elements();
  stripeElementHolder.value.style.minHeight = '70px';
  stripeElementHolder.value.style.padding = '0';

  if (!stripeCardMount.value) {
    stripeError.value = 'Impossible d’afficher le champ de carte.';
    return;
  }
  if (stripeCardElement.value?.destroy) {
    stripeCardElement.value.destroy();
    stripeCardElement.value = null;
  }
  stripeCardMount.value.innerHTML = '';
  stripeCardMount.value.style.minHeight = '56px';

  const card = stripeElements.value.create('card', {
    hidePostalCode: true,
    style: {
      base: {
        color: '#ffffff',
        fontSize: '16px',
        iconColor: '#a0aec0',
        '::placeholder': { color: '#a0aec0' }
      },
      invalid: {
        color: '#f56565',
        iconColor: '#ff6b6b'
      }
    }
  });

  stripeCardReady.value = false;
  card.mount(stripeCardMount.value);
  stripeCardElement.value = card;

  card.on('ready', () => {
    stripeCardReady.value = true;
  });
  card.on('change', (event: any) => {
    if (event.error) {
      stripeError.value = event.error.message;
    } else {
      stripeError.value = null;
    }
  });
};

const waitForStripeCardReady = async () => {
  if (stripeCardReady.value) {
    return;
  }

  await new Promise<void>((resolve, reject) => {
    const timeout = setTimeout(() => {
      reject(new Error('Le formulaire de paiement Stripe n’est pas prêt après attente.'));
    }, 15000);

    const stop = watch(stripeCardReady, (ready) => {
      if (ready) {
        clearTimeout(timeout);
        stop();
        resolve();
      }
    });
  });
};

onBeforeUnmount(() => {
  const card = stripeCardElement.value;
  if (card?.destroy) {
    card.destroy();
  }
});

watch(orderDetail, async (detail) => {
  if (detail?.payment_method) {
    selectedMethod.value = detail.payment_method;
  }
  await setupStripeElements();
}, { immediate: true });

const handlePayment = async () => {
  if (!orderDetail.value) return;
  if (isMobileMoney.value && !isPaymentValid.value) {
    paymentError.value = t('buyer.paymentFormInvalid');
    return;
  }

  paymentLoading.value = true;
  paymentError.value = null;

  try {
        if (orderDetail.value.payment_method === 'STRIPE') {
        const paymentIntent = await createStripePaymentIntent(orderDetail.value.id);
        if (!paymentIntent?.client_secret) {
          throw new Error('Impossible de créer le paiement Stripe.');
        }

        if (!stripeInstance.value || !stripeCardElement.value) {
          await setupStripeElements();
        }

        await waitForStripeCardReady();

        const result = await stripeInstance.value.confirmCardPayment(paymentIntent.client_secret, {
          payment_method: { card: stripeCardElement.value },
        });

        if (result.error) {
          paymentError.value = result.error.message || 'Erreur de paiement Stripe.';
          return;
        }

        const paymentIntentStatus = result.paymentIntent?.status;
        if (paymentIntentStatus === 'succeeded') {
          await confirmStripePaymentIntent(result.paymentIntent.id);
          await fetchOrderDetail(orderDetail.value.id);
          router.push(`/buyer/orders/${orderDetail.value.id}`);
          return;
        }

        paymentError.value = `Paiement non finalisé (${paymentIntentStatus || 'statut inconnu'}).`;
        return;
    }

    const response = await initiatePayment({
      order_id: orderDetail.value.id,
      method: selectedMethod.value,
      phone: senderPhone.value,
      sender_phone: senderPhone.value,
      sender_name: senderName.value,
      transaction_reference: transactionReference.value,
    });

    console.log('payment response', response);
    await fetchOrderDetail(orderDetail.value.id);
    router.push(`/buyer/orders/${orderDetail.value.id}`);
  } catch (err: any) {
    console.error('Payment error:', err?.message || err);
    paymentError.value = err?.detail || err?.message || t('dashboard.error_save');
  } finally {
    paymentLoading.value = false;
  }
};

onMounted(() => {
  if (route.params.id) {
    fetchOrderDetail(route.params.id as string);
  }
});
</script>
