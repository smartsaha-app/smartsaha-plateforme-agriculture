<template>
  <div class="min-h-screen bg-gray-50/50 pt-24 pb-20 px-6">
    <div class="max-w-[1200px] mx-auto">
      <!-- Back button -->
      <button @click="navigateTo('/marketplace')" class="flex items-center gap-2 text-gray-400 hover:text-[#112830] transition-colors mb-8 font-bold text-sm">
        <i class="bx bx-left-arrow-alt text-xl"></i>
        Retour au marketplace
      </button>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-12">
        <!-- Delivery Form -->
        <div class="lg:col-span-2 space-y-8">
          <div class="bg-white rounded-[3rem] p-10 border border-gray-100 shadow-sm">
            <h2 class="text-3xl font-black text-[#112830] mb-8 flex items-center gap-4">
              <span class="w-12 h-12 rounded-2xl bg-emerald-50 text-[#10b481] flex items-center justify-center">
                <i class="bx bx-truck"></i>
              </span>
              Informations de Livraison
            </h2>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="space-y-2">
                <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-4">Nom complet de réception</label>
                <input v-model="form.delivery_name" type="text" placeholder="Ex: Jean Dupont" class="w-full px-6 py-4 bg-gray-50 border-none rounded-2xl focus:ring-2 focus:ring-[#10b481]/20 transition-all outline-none font-bold text-[#112830]" />
              </div>
              <div class="space-y-2">
                <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-4">Téléphone de contact</label>
                <input v-model="form.delivery_phone" type="text" placeholder="Ex: +261 34 00 000 00" class="w-full px-6 py-4 bg-gray-50 border-none rounded-2xl focus:ring-2 focus:ring-[#10b481]/20 transition-all outline-none font-bold text-[#112830]" />
              </div>
              <div class="space-y-2 md:col-span-2">
                <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-4">Adresse exacte</label>
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
                <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-4">Notes pour le livreur (Optionnel)</label>
                <textarea v-model="form.delivery_notes" placeholder="Précisez un lieu de repère ou une instruction particulière..." class="w-full px-6 py-4 bg-gray-50 border-none rounded-2xl focus:ring-2 focus:ring-[#10b481]/20 transition-all outline-none font-bold text-[#112830] h-24 resize-none"></textarea>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-[3rem] p-10 border border-gray-100 shadow-sm">
            <h2 class="text-3xl font-black text-[#112830] mb-8 flex items-center gap-4">
              <span class="w-12 h-12 rounded-2xl bg-blue-50 text-blue-600 flex items-center justify-center">
                <i class="bx bx-credit-card"></i>
              </span>
              Mode de Paiement
            </h2>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <label 
                v-for="method in paymentMethods" 
                :key="method.id"
                :class="[form.payment_method === method.id ? 'border-[#10b481] bg-emerald-50/50' : 'border-gray-100 hover:border-gray-200']"
                class="relative border-2 p-6 rounded-3xl cursor-pointer transition-all flex flex-col items-center gap-4 group"
              >
                <input type="radio" v-model="form.payment_method" :value="method.id" class="absolute opacity-0" />
                <div :class="[form.payment_method === method.id ? 'bg-[#10b481] text-white' : 'bg-gray-100 text-gray-400']" class="w-12 h-12 rounded-2xl flex items-center justify-center text-2xl transition-all">
                  <i :class="method.icon"></i>
                </div>
                <div class="text-center">
                  <p class="font-black text-[#112830] text-sm">{{ method.name }}</p>
                  <p class="text-[10px] text-gray-400 font-bold uppercase tracking-widest">{{ method.sub }}</p>
                </div>
                <i v-if="form.payment_method === method.id" class="bx bxs-check-circle absolute top-4 right-4 text-[#10b481] text-xl animate-in zoom-in"></i>
              </label>
            </div>
          </div>
        </div>

        <!-- Summary & Action -->
        <div class="space-y-6">
          <div class="bg-[#112830] text-white rounded-[3rem] p-10 shadow-xl relative overflow-hidden">
            <h3 class="text-xl font-black mb-8 relative z-10">Récapitulatif</h3>
            
            <div class="space-y-4 mb-8 relative z-10">
              <div v-for="item in cart?.items" :key="item.id" class="flex justify-between items-start gap-4">
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-bold truncate">{{ item.product_name }}</p>
                  <p class="text-[10px] text-white/40 font-bold uppercase tracking-widest">{{ item.quantity }} unité(s)</p>
                </div>
                <span class="text-sm font-black whitespace-nowrap">{{ item.subtotal }} Ar</span>
              </div>
            </div>

            <div class="space-y-4 pt-6 border-t border-white/10 relative z-10">
              <div class="flex justify-between items-center text-sm">
                <span class="text-white/40 font-bold">Sous-total</span>
                <span class="font-black">{{ cart?.total || 0 }} Ar</span>
              </div>
              <div class="flex justify-between items-center text-sm">
                <span class="text-white/40 font-bold">Livraison</span>
                <span class="font-black">0 Ar</span>
              </div>
              <div class="flex justify-between items-center text-2xl pt-4">
                <span class="font-black">Total</span>
                <span class="text-[#10b481] font-black">{{ cart?.total || 0 }} Ar</span>
              </div>
            </div>

            <button 
              @click="handleCheckout"
              :disabled="loading || !isFormValid"
              class="w-full py-5 bg-[#10b481] hover:bg-white hover:text-[#112830] disabled:bg-white/5 disabled:text-white/20 text-white rounded-2xl font-black text-xs uppercase tracking-widest transition-all mt-10 flex items-center justify-center gap-3 relative z-10"
            >
              <i v-if="loading" class="bx bx-loader-alt animate-spin text-xl"></i>
              <span v-else>Confirmer et Payer</span>
            </button>

            <!-- Decor -->
            <i class="bx bxs-quote-right absolute top-[-10%] left-[-10%] text-white/5 text-[15rem]"></i>
          </div>

          <div class="p-6 bg-amber-50 rounded-2xl border border-amber-100 flex gap-4">
            <i class="bx bx-info-circle text-2xl text-amber-500"></i>
            <p class="text-[11px] text-amber-700 font-bold leading-relaxed">
              En cliquant sur confirmer, vous acceptez nos conditions de vente. Les fonds seront conservés par SmartSaha jusqu'à la réception de votre commande (Paiement Sécurisé).
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Success Modal -->
    <div v-if="successOrder" class="fixed inset-0 z-[200] flex items-center justify-center p-6 backdrop-blur-xl bg-black/60 animate-in fade-in duration-500">
      <div class="bg-white rounded-[4rem] p-16 max-w-xl w-full text-center space-y-8 shadow-2xl relative overflow-hidden">
        <div class="w-24 h-24 bg-emerald-50 text-[#10b481] rounded-[2rem] flex items-center justify-center text-5xl mx-auto shadow-xl shadow-emerald-500/20">
          <i class="bx bx-check-circle"></i>
        </div>
        <div>
          <h2 class="text-4xl font-black text-[#112830] mb-2">Commande Réussie !</h2>
          <p class="text-gray-400 font-bold tracking-tight">Votre commande <span class="text-[#10b481]">#{{ successOrder.order_number }}</span> est en cours de traitement.</p>
        </div>
        <div class="pt-8 flex flex-col gap-4">
          <button @click="navigateTo('/farmer/orders')" class="w-full py-5 bg-[#112830] text-white rounded-2xl font-black text-xs uppercase tracking-widest">Suivre ma commande</button>
          <button @click="navigateTo('/marketplace')" class="w-full py-5 bg-gray-50 text-gray-400 hover:text-[#112830] rounded-2xl font-black text-xs uppercase tracking-widest transition-all">Retourner à la boutique</button>
        </div>
        <!-- Decorative bg -->
        <div class="absolute bottom-[-10%] right-[-10%] w-64 h-64 bg-[#10b481]/5 rounded-full blur-[80px]"></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useMarketplace } from '~/composables/useMarketplace';

const { cart, fetchCart, checkout } = useMarketplace();
const loading = ref(false);
const successOrder = ref<any>(null);

const form = ref({
  delivery_name: '',
  delivery_phone: '',
  delivery_address: '',
  delivery_city: '',
  delivery_region: '',
  delivery_notes: '',
  payment_method: 'MVOLA',
  buyer_name: '' // Will be set to delivery_name if empty
});

const paymentMethods = [
  { id: 'MVOLA', name: 'MVola', sub: 'Mobile Money', icon: 'bx bx-mobile-vibration' },
  { id: 'ORANGE_MONEY', name: 'Orange Money', sub: 'Mobile Money', icon: 'bx bx-mobile' },
  { id: 'STRIPE', name: 'Carte Bancaire', sub: 'Visa / Mastercard', icon: 'bx bx-credit-card' }
];

onMounted(() => {
  fetchCart();
});

const isFormValid = computed(() => {
  return form.value.delivery_name && 
         form.value.delivery_phone && 
         form.value.delivery_address && 
         form.value.delivery_city && 
         form.value.delivery_region;
});

const handleCheckout = async () => {
  loading.value = true;
  try {
    const response = await checkout({
      ...form.value,
      buyer_name: form.value.delivery_name
    });
    successOrder.value = response;
  } catch (err) {
    console.error('Checkout failed', err);
    // Optionnel: Notification d'erreur
  } finally {
    loading.value = false;
  }
};
</script>
