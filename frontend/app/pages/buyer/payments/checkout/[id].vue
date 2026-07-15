<template>
  <div class="max-w-4xl mx-auto space-y-8">
    <!-- Back & Header -->
    <div class="space-y-4">
      <button @click="router.back()" class="flex items-center gap-2 text-xs font-black text-gray-400 uppercase tracking-widest hover:text-[#10b481] transition-colors">
        <i class="bx bx-left-arrow-alt text-xl"></i>
        Retour
      </button>
      <h1 class="text-3xl font-black text-[#112830]">Finaliser le paiement</h1>
      <p class="text-gray-500 font-medium">Commande {{ orderDetail?.order_number }}</p>
    </div>

    <div v-if="loading" class="bg-white p-12 rounded-[3rem] border border-gray-100 flex items-center justify-center">
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
            <span class="text-[#112830] font-black">Total</span>
            <span class="text-[#10b481] font-black">{{ orderDetail?.total }} Ar</span>
          </div>
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
            <label class="text-[10px] font-black text-gray-400 uppercase tracking-[0.2em]">Nom du titulaire du compte</label>
            <input
              v-model="senderName"
              type="text"
              placeholder="Nom associé au compte mobile money"
              class="w-full bg-[#152e37] border-2 border-gray-700 rounded-2xl py-4 px-4 text-white font-black placeholder:text-gray-600 focus:border-[#10b481] transition-all outline-none"
            />
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

        <div v-if="paymentError" class="mb-4 p-4 bg-rose-500/10 border border-rose-500/20 rounded-2xl text-rose-600 text-sm font-bold">
          {{ paymentError }}
        </div>

        <button 
          type="button"
          @click="handlePayment"
          :disabled="paymentLoading || loading || (isMobileMoney && !isPaymentValid)"
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
import { ref, computed, watch, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useMarketplace } from '~/composables/useMarketplace';

const { t } = useI18n();
definePageMeta({
  layout: 'dashboard'
});

const route = useRoute();
const router = useRouter();
const { orderDetail, loading, error, fetchOrderDetail, initiatePayment } = useMarketplace();

const paymentLoading = ref(false);
const paymentError = ref<string | null>(null);

const selectedMethod = ref('MVOLA');
const senderPhone = ref('');
const senderName = ref('');
const transactionReference = ref('');

const paymentMethods = [
  { id: 'MVOLA', label: 'MVola', icon: 'bx bx-phone-incoming', isMobile: true },
  { id: 'ORANGE_MONEY', label: 'Orange Money', icon: 'bx bx-phone-incoming', isMobile: true },
  { id: 'AIRTEL_MONEY', label: 'Airtel Money', icon: 'bx bx-phone-incoming', isMobile: true },
  { id: 'TEST', label: 'Mode Démo / Test', icon: 'bx bx-vial', isMobile: false },
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

watch(orderDetail, (detail) => {
  if (detail?.payment_method) {
    selectedMethod.value = detail.payment_method;
  }
}, { immediate: true });

const handlePayment = async () => {
  if (!orderDetail.value) return;
  if (isMobileMoney.value && !isPaymentValid.value) {
    paymentError.value = t('buyer.paymentFormInvalid');
    return;
  }

  paymentLoading.value = true;
  paymentError.value = null;

  console.log('handlePayment payload', {
    order_id: orderDetail.value.id,
    method: selectedMethod.value,
    phone: senderPhone.value,
    sender_phone: senderPhone.value,
    sender_name: senderName.value,
    transaction_reference: transactionReference.value,
  });

  try {
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
