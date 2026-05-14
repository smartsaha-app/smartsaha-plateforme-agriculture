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

        <div class="grid grid-cols-1 gap-3">
          <button 
            v-for="m in paymentMethods" 
            :key="m.id"
            @click="selectedMethod = m.id"
            :class="[
              selectedMethod === m.id 
                ? 'border-[#10b481] bg-[#10b481]/10 text-white' 
                : 'border-gray-700 bg-[#152e37] text-gray-400 hover:border-gray-500'
            ]"
            class="p-4 border-2 rounded-2xl transition-all flex items-center gap-4 group text-left"
          >
            <div :class="[selectedMethod === m.id ? 'bg-[#10b481] text-white' : 'bg-gray-800 text-gray-500']" class="w-10 h-10 rounded-xl flex items-center justify-center text-xl shrink-0 transition-colors">
              <i :class="m.icon"></i>
            </div>
            <div class="flex-1">
              <div class="flex items-center gap-2">
                <p class="text-xs font-black uppercase tracking-widest" :class="selectedMethod === m.id ? 'text-white' : 'text-gray-400'">{{ m.label }}</p>
                <span v-if="m.id === 'TEST'" class="px-1.5 py-0.5 bg-amber-500 text-[8px] font-black text-white rounded">DEBUG</span>
              </div>
              <p class="text-[10px] font-bold text-gray-500">{{ m.isMobile ? 'Paiement Mobile Money' : 'Simulation de transaction' }}</p>
            </div>
            <div v-if="selectedMethod === m.id" class="w-6 h-6 bg-[#10b481] rounded-full flex items-center justify-center text-white text-sm">
              <i class="bx bx-check"></i>
            </div>
          </button>
        </div>

        <div v-if="isMobileMoney" class="space-y-2">
          <label class="text-[10px] font-black text-gray-400 uppercase tracking-[0.2em]">Numéro de téléphone {{ selectedMethod }}</label>
          <div class="relative">
            <i class="bx bx-phone absolute left-4 top-1/2 -translate-y-1/2 text-gray-500"></i>
            <input 
              v-model="paymentPhone"
              type="tel" 
              placeholder="034 XX XXX XX"
              class="w-full bg-[#152e37] border-2 border-gray-700 rounded-2xl py-4 pl-12 pr-4 text-white font-black placeholder:text-gray-600 focus:border-[#10b481] transition-all outline-none"
            />
          </div>
        </div>

        <button 
          @click="handlePayment"
          :disabled="loading || (isMobileMoney && !paymentPhone)"
          class="w-full py-5 bg-[#10b481] text-white rounded-2xl font-black text-xs uppercase tracking-[0.2em] shadow-lg shadow-[#10b481]/20 hover:bg-[#0da072] active:scale-95 transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <i v-if="loading" class="bx bx-loader-alt animate-spin text-lg"></i>
          <span v-else>Confirmer le règlement</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useMarketplace } from '~/composables/useMarketplace';

definePageMeta({
  layout: 'dashboard'
});

const route = useRoute();
const router = useRouter();
const { orderDetail, loading, error, fetchOrderDetail, initiatePayment } = useMarketplace();

const selectedMethod = ref('MVOLA');
const paymentPhone = ref('');

const paymentMethods = [
  { id: 'MVOLA', label: 'MVola', icon: 'bx bx-phone-incoming', isMobile: true },
  { id: 'ORANGE_MONEY', label: 'Orange Money', icon: 'bx bx-phone-incoming', isMobile: true },
  { id: 'AIRTEL_MONEY', label: 'Airtel Money', icon: 'bx bx-phone-incoming', isMobile: true },
  { id: 'TEST', label: 'Mode Démo / Test', icon: 'bx bx-vial', isMobile: false },
];

const isMobileMoney = computed(() => {
  const method = paymentMethods.find(m => m.id === selectedMethod.value);
  return method?.isMobile;
});

const handlePayment = async () => {
  if (!orderDetail.value) return;

  try {
    await initiatePayment({
      order_id: orderDetail.value.id,
      method: selectedMethod.value,
      phone: paymentPhone.value
    });

    if (isMobileMoney.value) {
      alert("Une demande de paiement a été envoyée sur votre téléphone. Veuillez valider avec votre code secret.");
    } else {
      alert("Paiement réussi !");
    }

    router.push(`/buyer/orders/${orderDetail.value.id}`);
  } catch (err: any) {
    alert("Erreur lors du paiement : " + err.message);
  }
};

onMounted(() => {
  if (route.params.id) {
    fetchOrderDetail(route.params.id as string);
  }
});
</script>
