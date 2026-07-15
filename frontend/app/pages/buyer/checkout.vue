<template>
  <div class="min-h-screen bg-gray-50/50 pt-24 pb-20 px-6">
    <div class="max-w-[1200px] mx-auto">
      <!-- Back button -->
      <button @click="navigateTo('/buyer/products')" class="flex items-center gap-2 text-gray-400 hover:text-[#112830] transition-colors mb-8 font-bold text-sm">
        <i class="bx bx-left-arrow-alt text-xl"></i>
        {{ t('buyer.backToProducts') }}
      </button>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-12">
        <!-- Delivery Form -->
        <div class="lg:col-span-2 space-y-8">
          <div class="bg-white rounded-[3rem] p-10 border border-gray-100 shadow-sm">
            <h2 class="text-3xl font-black text-[#112830] mb-8 flex items-center gap-4">
              <span class="w-12 h-12 rounded-2xl bg-emerald-50 text-[#10b481] flex items-center justify-center">
                <i class="bx bx-truck"></i>
              </span>
              {{ t('buyer.deliveryInfoTitle') }}
            </h2>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="space-y-2">
                <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-4">{{ t('buyer.fullNameLabel') }}</label>
                <input v-model="form.delivery_name" type="text" placeholder="Ex: Jean Dupont" class="w-full px-6 py-4 bg-gray-50 border-none rounded-2xl focus:ring-2 focus:ring-[#10b481]/20 transition-all outline-none font-bold text-[#112830]" />
              </div>
              <div class="space-y-2">
                <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-4">{{ t('buyer.contactPhoneLabel') }}</label>
                <input v-model="form.delivery_phone" type="text" placeholder="Ex: +261 34 00 000 00" class="w-full px-6 py-4 bg-gray-50 border-none rounded-2xl focus:ring-2 focus:ring-[#10b481]/20 transition-all outline-none font-bold text-[#112830]" />
              </div>
              <div class="space-y-2 md:col-span-2">
                <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-4">{{ t('buyer.checkoutDesc') }}</label>
                <input v-model="form.delivery_address" type="text" placeholder="Lot IV G 42 Bis..." class="w-full px-6 py-4 bg-gray-50 border-none rounded-2xl focus:ring-2 focus:ring-[#10b481]/20 transition-all outline-none font-bold text-[#112830]" />
              </div>
              <div class="space-y-2">
                <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-4">Ville</label>
                <input v-model="form.delivery_city" type="text" placeholder="Antananarivo" class="w-full px-6 py-4 bg-gray-50 border-none rounded-2xl focus:ring-2 focus:ring-[#10b481]/20 transition-all outline-none font-bold text-[#112830]" />
              </div>
              <div class="space-y-2">
                <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-4">Région</label>
                <input v-model="form.delivery_region" type="text" placeholder="Analamanga" class="w-full px-6 py-4 bg-gray-50 border-none rounded-2xl focus:ring-2 focus:ring-[#10b481]/20 transition-all outline-none font-bold text-[#112830]" />
              </div>
              <div class="space-y-2 md:col-span-2">
                <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-4">{{ t('buyer.deliveryNotesLabel') }}</label>
                <textarea v-model="form.delivery_notes" placeholder="Précisez un lieu de repère ou une instruction particulière..." class="w-full px-6 py-4 bg-gray-50 border-none rounded-2xl focus:ring-2 focus:ring-[#10b481]/20 transition-all outline-none font-bold text-[#112830] h-24 resize-none"></textarea>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-[3rem] p-10 border border-gray-100 shadow-sm">
            <h2 class="text-3xl font-black text-[#112830] mb-8 flex items-center gap-4">
              <span class="w-12 h-12 rounded-2xl bg-blue-50 text-blue-600 flex items-center justify-center">
                <i class="bx bx-credit-card"></i>
              </span>
              {{ t('buyer.paymentMethodTitle') }}
            </h2>

            <fieldset class="flex flex-wrap gap-4 mb-6 pb-2 justify-start">
              <legend class="sr-only">{{ t('buyer.paymentMethodTitle') }}</legend>
              <label
                v-for="method in paymentMethods"
                :key="method.id"
                :for="`payment-method-${method.id}`"
                :class="[
                  'flex-none min-w-[120px] max-w-[170px]',
                  method.id === 'TEST' ? 'flex-none' : '',
                  'relative border-2 p-4 rounded-[2rem] cursor-pointer transition-all duration-200 ease-out flex flex-col items-center gap-3 group hover:-translate-y-0.5',
                  form.payment_method === method.id ? 'border-[#10b481] bg-[#edf8f3] shadow-lg shadow-[#10b481]/10' : 'border-gray-200 hover:border-gray-300'
                ]"
              >
                <input
                  type="radio"
                  v-model="form.payment_method"
                  :value="method.id"
                  :id="`payment-method-${method.id}`"
                  class="sr-only"
                />
                <span v-if="method.id === 'TEST'" class="absolute top-3 left-4 text-[10px] font-black uppercase tracking-widest px-2 py-1 bg-amber-100 text-amber-700 rounded-full">
                  Démo
                </span>
                <div
                  :class="[
                    'flex items-center justify-center w-20 h-20 rounded-3xl transition-all duration-200',
                    form.payment_method === method.id ? 'bg-[#10b481] text-white shadow-inner' : 'bg-gray-100 text-gray-500'
                  ]"
                >
                  <img v-if="method.logo" :src="method.logo" :alt="method.name" class="max-w-full max-h-full object-contain" />
                  <i v-else :class="['text-3xl', method.icon]"></i>
                </div>
                <div class="text-center">
                  <p class="font-black text-[#112830] text-sm">{{ method.name }}</p>
                  <p class="text-[9px] text-gray-500 font-bold uppercase tracking-widest">{{ method.sub }}</p>
                </div>
                <span v-if="form.payment_method === method.id" class="absolute top-4 right-4 text-[#10b481] text-xl">
                  <i class="bx bxs-check-circle"></i>
                </span>
              </label>
            </fieldset>

            <div class="p-6 bg-[#112830] rounded-3xl text-white space-y-4">
              <div class="flex items-center gap-3">
                <span class="w-9 h-9 rounded-xl bg-[#10b481]/20 text-[#10b481] flex items-center justify-center">
                  <i class="bx bx-info-circle text-lg"></i>
                </span>
                <p class="text-xs font-black uppercase tracking-widest text-white/60">Étape suivante</p>
              </div>

              <p class="text-[10px] text-white/70 leading-relaxed">
                Votre commande sera créée maintenant. Vous pourrez ensuite finaliser le paiement sur la page suivante.
              </p>
            </div>
          </div>
        </div>

        <!-- Summary & Action -->
        <div class="space-y-6">
          <div class="bg-[#112830] text-white rounded-[3rem] p-10 shadow-xl relative overflow-hidden">
            <h3 class="text-xl font-black mb-8 relative z-10">{{ t('buyer.summaryTitle') }}</h3>
            
            <div class="space-y-6 mb-8 relative z-10">
              <div v-for="item in cart?.items" :key="item.id" class="flex flex-col gap-2 p-4 bg-white/5 rounded-2xl border border-white/10">
                <div class="flex justify-between items-start gap-4">
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-bold truncate">{{ item.product_name }}</p>
                    <p class="text-[10px] text-white/40 font-bold uppercase tracking-widest">{{ item.price }} Ar / unité</p>
                  </div>
                  <span class="text-sm font-black whitespace-nowrap">{{ item.subtotal }} Ar</span>
                </div>
                
                <div class="flex items-center justify-between mt-2 pt-2 border-t border-white/5">
                  <div class="flex items-center gap-3">
                    <button @click="updateQuantity(item, -1)" :disabled="item.quantity <= 1" class="w-7 h-7 rounded-lg bg-white/10 flex items-center justify-center hover:bg-[#10b481] disabled:opacity-20 transition-all">
                      <i class="bx bx-minus text-xs"></i>
                    </button>
                    <span class="text-xs font-black w-6 text-center">{{ item.quantity }}</span>
                    <button @click="updateQuantity(item, 1)" class="w-7 h-7 rounded-lg bg-white/10 flex items-center justify-center hover:bg-[#10b481] transition-all">
                      <i class="bx bx-plus text-xs"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="space-y-4 pt-6 border-t border-white/10 relative z-10 mb-8">
              <div class="flex justify-between items-center text-sm">
                <span class="text-white/60 font-bold">{{ t('buyer.subtotal') }}</span>
                <span class="font-black">{{ cart?.total || 0 }} Ar</span>
              </div>
              <div class="flex justify-between items-center text-sm">
                <span class="text-white/60 font-bold">{{ t('buyer.delivery') }}</span>
                <span class="font-black">0 Ar</span>
              </div>
              <div class="flex justify-between items-center text-2xl pt-4 border-t border-white/5">
                <span class="font-black">{{ t('buyer.total') }}</span>
                <span class="text-[#10b481] font-black">{{ cart?.total || 0 }} Ar</span>
              </div>
            </div>

            <div v-if="checkoutError" class="mb-6 p-4 bg-rose-500/10 border border-rose-500/20 rounded-2xl flex gap-3 items-center animate-in slide-in-from-top-4">
              <i class="bx bx-error-circle text-rose-500 text-xl"></i>
              <p class="text-[10px] font-black text-rose-400 uppercase tracking-widest leading-tight">{{ checkoutError }}</p>
            </div>

            <button 
              @click="handleCheckout"
              :disabled="loading || !isFormValid"
              class="w-full py-5 bg-[#10b481] hover:bg-white hover:text-[#112830] disabled:bg-white/5 disabled:text-white/20 text-white rounded-2xl font-black text-xs uppercase tracking-widest transition-all mt-4 flex items-center justify-center gap-3 relative z-10"
            >
              <i v-if="loading" class="bx bx-loader-alt animate-spin text-xl"></i>
              <span v-else>{{ t('buyer.confirmAndPay') }}</span>
            </button>

            <!-- Decor -->
            <i class="bx bxs-quote-right absolute top-[-10%] left-[-10%] text-white/5 text-[15rem]"></i>
          </div>

          <div class="p-6 bg-amber-50 rounded-2xl border border-amber-100 flex gap-4">
            <i class="bx bx-info-circle text-2xl text-amber-500"></i>
            <p class="text-[11px] text-amber-700 font-bold leading-relaxed">
              {{ t('buyer.escrowNote') }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Success Modal -->
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useMarketplace } from '~/composables/useMarketplace';

const { t } = useI18n();
definePageMeta({ layout: 'dashboard' });

const { cart, fetchCart, checkout, addToCart } = useMarketplace();
const loading = ref(false);
const checkoutError = ref<string | null>(null);

onMounted(() => {
  fetchCart();
});

const form = ref({
  delivery_name: '',
  delivery_phone: '',
  delivery_address: '',
  delivery_city: '',
  delivery_region: '',
  delivery_notes: '',
  payment_method: 'TEST',
  buyer_name: '',
});

// IMPORTANT :
// - ussdCode doit pointer vers VOTRE propre numéro marchand (jamais un tiers).
// - recipientName / recipientNumber sont affichés en clair pour que l'utilisateur
//   puisse vérifier AVANT d'envoyer, plutôt que de faire confiance uniquement au code.
// - Ces valeurs doivent idéalement venir de votre config backend (numéro marchand
//   par opérateur), pas être codées en dur ici en production.
const paymentMethods = [
  { id: 'TEST',         name: 'Paiement test',  sub: 'Simulation instantanée', icon: 'bx bx-test-tube' },
  {
    id: 'MVOLA',
    name: 'MVola',
    sub: 'Mobile Money',
    logo: '/payment-logos/mvola.jpg',
    ussdCode: '#111*1*1*[VOTRE_NUMERO_MVOLA]*[MONTANT]#',
    recipientName: 'Yves Aimable',
    recipientNumber: '0345883074',
  },
  {
    id: 'ORANGE_MONEY',
    name: 'Orange Money',
    sub: 'Mobile Money',
    logo: '/payment-logos/orange-money.png',
    ussdCode: '#144*1*[VOTRE_NUMERO_OM]*[MONTANT]#',
    recipientName: 'Yves Aimable',
    recipientNumber: '0326836795',
  },
  {
    id: 'AIRTEL_MONEY',
    name: 'Airtel Money',
    sub: 'Mobile Money',
    logo: '/payment-logos/airtel-money.jpg',
    ussdCode: '#436*1*[VOTRE_NUMERO_AIRTEL]*[MONTANT]#',
    recipientName: 'Yves Aimable',
    recipientNumber: '0339442387',
  },
  { id: 'STRIPE', name: 'Carte Bancaire', sub: 'Visa / Mastercard', logo: '/payment-logos/stripe.png' },
];

const updateQuantity = async (item: any, delta: number) => {
  try {
    if (item.quantity + delta < 1) return;
    const productId = typeof item.product === 'object' ? item.product.id : item.product;
    await addToCart(productId, delta);
    await fetchCart();
  } catch (err: any) {
    alert(err.data?.error || t('dashboard.error_save'));
  }
};

const isFormValid = computed(() => {
  return !!(
    form.value.delivery_name &&
    form.value.delivery_phone &&
    form.value.delivery_address &&
    form.value.delivery_city &&
    form.value.delivery_region &&
    (cart.value?.items?.length ?? 0) > 0
  );
});

const handleCheckout = async () => {
  loading.value = true;
  checkoutError.value = null;
  try {
    // Étape 1 — créer la commande
    const order = await checkout({
      delivery_name:    form.value.delivery_name,
      delivery_phone:   form.value.delivery_phone,
      delivery_address: form.value.delivery_address,
      delivery_city:    form.value.delivery_city,
      delivery_region:  form.value.delivery_region,
      delivery_notes:   form.value.delivery_notes,
      payment_method:   form.value.payment_method,
      buyer_name:       form.value.delivery_name,
    });

    // Étape 2 — rediriger vers la page de finalisation du paiement
    await navigateTo(`/buyer/payments/checkout/${order.id}`);
  } catch (err: any) {
    checkoutError.value = err.data?.error || err.data?.detail || t('dashboard.error_save');
  } finally {
    loading.value = false;
  }
};
</script>