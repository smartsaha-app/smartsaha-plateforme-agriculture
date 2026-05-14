<template>
  <div class="space-y-8">
    <!-- Back & Header -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div class="space-y-2">
        <button @click="router.back()" class="flex items-center gap-2 text-xs font-black text-gray-400 uppercase tracking-widest hover:text-[#10b481] transition-colors mb-4">
          <i class="bx bx-left-arrow-alt text-xl"></i>
          Retour aux commandes
        </button>
        <div class="flex items-center gap-4">
          <h1 class="text-3xl font-black text-[#112830]">{{ orderDetail?.order_number }}</h1>
          <span :class="getStatusClass(orderDetail?.status)" class="px-4 py-1.5 rounded-full text-[10px] font-black uppercase tracking-[0.2em]">
            {{ getStatusLabel(orderDetail?.status) }}
          </span>
        </div>
        <p class="text-gray-500 font-medium">Passée le {{ formatDate(orderDetail?.created_at) }}</p>
      </div>
      
      <div class="flex gap-3 w-full md:w-auto">
        <button class="flex-1 md:flex-none px-6 py-3 bg-white border border-gray-100 text-[#112830] rounded-2xl font-black text-xs uppercase tracking-widest hover:bg-gray-50 transition-all flex items-center justify-center gap-2">
          <i class="bx bx-printer text-lg"></i>
          Facture
        </button>
        <button class="flex-1 md:flex-none px-6 py-3 bg-[#112830] text-white rounded-2xl font-black text-xs uppercase tracking-widest shadow-lg shadow-[#112830]/10 hover:bg-[#10b481] transition-all flex items-center justify-center gap-2">
          <i class="bx bx-support text-lg"></i>
          Aide
        </button>
      </div>
    </div>

    <div v-if="loading" class="grid grid-cols-1 lg:grid-cols-3 gap-8 animate-pulse">
      <div class="lg:col-span-2 space-y-6">
        <div class="h-64 bg-white rounded-[2.5rem] border border-gray-100"></div>
        <div class="h-96 bg-white rounded-[2.5rem] border border-gray-100"></div>
      </div>
      <div class="h-[500px] bg-white rounded-[2.5rem] border border-gray-100"></div>
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

    <div v-else-if="orderDetail" class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Left Column: Details & Items -->
      <div class="lg:col-span-2 space-y-8">
        <!-- Status Timeline -->
        <div class="bg-white p-8 rounded-[2.5rem] border border-gray-100 shadow-sm overflow-hidden relative">
          <h3 class="text-lg font-black text-[#112830] mb-8">Suivi de commande</h3>
          
          <div class="flex justify-between relative">
            <div class="absolute top-5 left-0 w-full h-1 bg-gray-50 z-0"></div>
            <div 
              class="absolute top-5 left-0 h-1 bg-[#10b481] z-0 transition-all duration-1000" 
              :style="{ width: getProgressWidth(orderDetail.status) + '%' }"
            ></div>
            
            <div v-for="step in statusSteps" :key="step.key" class="relative z-10 flex flex-col items-center gap-3">
              <div 
                :class="[
                  isStepCompleted(step.key, orderDetail.status) 
                    ? 'bg-[#10b481] text-white scale-110' 
                    : isStepActive(step.key, orderDetail.status)
                      ? 'bg-white border-4 border-[#10b481] text-[#10b481]'
                      : 'bg-white border-4 border-gray-50 text-gray-200'
                ]"
                class="w-12 h-12 rounded-2xl flex items-center justify-center text-xl transition-all shadow-sm"
              >
                <i :class="step.icon"></i>
              </div>
              <div class="text-center">
                <p class="text-[10px] font-black uppercase tracking-widest text-[#112830]">{{ step.label }}</p>
                <p v-if="isStepCompleted(step.key, orderDetail.status)" class="text-[9px] font-bold text-[#10b481]">Terminé</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Order Items -->
        <div class="bg-white rounded-[2.5rem] border border-gray-100 shadow-sm overflow-hidden">
          <div class="p-8 border-b border-gray-50 flex items-center justify-between">
            <h3 class="text-lg font-black text-[#112830]">Articles commandés</h3>
            <span class="px-4 py-1.5 bg-gray-50 rounded-full text-[10px] font-black text-gray-400 uppercase tracking-widest">
              {{ orderDetail.items?.length }} Article(s)
            </span>
          </div>
          
          <div class="divide-y divide-gray-50">
            <div v-for="item in orderDetail.items" :key="item.id" class="p-8 flex flex-col md:flex-row gap-6 hover:bg-gray-50/50 transition-colors">
              <div class="w-24 h-24 bg-gray-100 rounded-3xl overflow-hidden flex-shrink-0 border border-gray-100">
                <img v-if="item.product_image" :src="item.product_image" class="w-full h-full object-cover" />
                <div v-else class="w-full h-full flex items-center justify-center text-gray-300">
                  <i class="bx bx-image text-4xl"></i>
                </div>
              </div>
              
              <div class="flex-1 space-y-2">
                <div class="flex justify-between items-start">
                  <div>
                    <h4 class="text-xl font-black text-[#112830]">{{ item.product_name }}</h4>
                    <p class="text-sm font-bold text-gray-400">Vendu par <span class="text-[#10b481]">{{ item.seller_name }}</span></p>
                  </div>
                  <p class="text-lg font-black text-[#112830]">{{ item.subtotal }} Ar</p>
                </div>
                
                <div class="flex items-center gap-6 pt-2">
                  <div class="flex items-center gap-2">
                    <span class="text-[10px] font-black text-gray-300 uppercase tracking-widest">Quantité:</span>
                    <span class="text-sm font-black text-[#112830]">{{ item.quantity }}</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <span class="text-[10px] font-black text-gray-300 uppercase tracking-widest">Prix unit.:</span>
                    <span class="text-sm font-black text-[#112830]">{{ item.price }} Ar</span>
                  </div>
                </div>
              </div>

              <div class="flex items-center justify-end">
                <button 
                  v-if="orderDetail.status === 'DELIVERED'"
                  class="px-4 py-2 bg-emerald-50 text-[#10b481] rounded-xl font-black text-[10px] uppercase tracking-widest hover:bg-[#10b481] hover:text-white transition-all"
                >
                  Donner un avis
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column: Info Summaries -->
      <div class="space-y-8">
        <!-- Delivery Address -->
        <div class="bg-white p-8 rounded-[2.5rem] border border-gray-100 shadow-sm space-y-6">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-blue-50 text-blue-500 rounded-xl flex items-center justify-center text-xl">
              <i class="bx bx-map"></i>
            </div>
            <h3 class="text-lg font-black text-[#112830]">Livraison</h3>
          </div>
          
          <div class="space-y-4">
            <div class="space-y-1">
              <p class="text-[10px] font-black text-gray-300 uppercase tracking-widest">Destinataire</p>
              <p class="text-sm font-black text-[#112830]">{{ orderDetail.delivery_name }}</p>
              <p class="text-sm font-bold text-gray-500">{{ orderDetail.delivery_phone }}</p>
            </div>
            
            <div class="space-y-1 pt-2 border-t border-gray-50">
              <p class="text-[10px] font-black text-gray-300 uppercase tracking-widest">Adresse</p>
              <p class="text-sm font-bold text-gray-600 leading-relaxed">
                {{ orderDetail.delivery_address }}<br />
                {{ orderDetail.delivery_city }}, {{ orderDetail.delivery_region }}
              </p>
            </div>

            <div v-if="orderDetail.delivery_notes" class="p-4 bg-amber-50 rounded-2xl">
               <p class="text-[9px] font-black text-amber-600 uppercase tracking-widest mb-1">Notes</p>
               <p class="text-xs font-bold text-amber-700 italic">{{ orderDetail.delivery_notes }}</p>
            </div>
          </div>
        </div>

        <!-- Payment Summary -->
        <div class="bg-white p-8 rounded-[2.5rem] border border-gray-100 shadow-sm space-y-6">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-emerald-50 text-[#10b481] rounded-xl flex items-center justify-center text-xl">
              <i class="bx bx-credit-card"></i>
            </div>
            <h3 class="text-lg font-black text-[#112830]">Paiement</h3>
          </div>
          
          <div class="space-y-3 pt-2">
            <div class="flex justify-between text-sm">
              <span class="text-gray-400 font-bold">Méthode</span>
              <span class="text-[#112830] font-black">{{ orderDetail.payment_method }}</span>
            </div>
            <div class="flex justify-between text-sm">
              <span class="text-gray-400 font-bold">Statut paiement</span>
              <span :class="orderDetail.payment_status === 'PAID' ? 'text-emerald-500' : 'text-amber-500'" class="font-black">{{ orderDetail.payment_status }}</span>
            </div>
            <div class="h-px bg-gray-50 my-4"></div>
            <div class="flex justify-between text-sm">
              <span class="text-gray-400 font-bold">Sous-total</span>
              <span class="text-[#112830] font-black">{{ orderDetail.subtotal }} Ar</span>
            </div>
            <div class="flex justify-between text-sm">
              <span class="text-gray-400 font-bold">Frais de livraison</span>
              <span class="text-[#112830] font-black">{{ orderDetail.delivery_fee }} Ar</span>
            </div>
            <div class="flex justify-between text-xl pt-4">
              <span class="text-[#112830] font-black">Total</span>
              <span class="text-[#10b481] font-black">{{ orderDetail.total }} Ar</span>
            </div>
          </div>
        </div>

        <!-- Payment Button (only if pending) -->
        <div v-if="orderDetail.status === 'PENDING'" class="flex justify-end pt-4">
          <button 
            @click="navigateTo(`/buyer/payments/checkout/${orderDetail.id}`)"
            class="w-full py-4 bg-[#112830] text-white rounded-2xl font-black text-xs uppercase tracking-widest shadow-lg shadow-[#112830]/10 hover:bg-[#10b481] transition-all flex items-center justify-center gap-2"
          >
            <i class="bx bx-credit-card text-lg"></i>
            Payer maintenant
          </button>
        </div>

        <!-- Receipt Confirmation Button (only if shipped) -->
        <div v-if="orderDetail.status === 'SHIPPED'" class="flex justify-end pt-4">
          <button 
            @click="handleConfirmReceipt"
            :disabled="loading"
            class="w-full py-4 bg-[#10b481] text-white rounded-2xl font-black text-xs uppercase tracking-widest shadow-lg shadow-[#10b481]/10 hover:bg-[#112830] transition-all flex items-center justify-center gap-2"
          >
            <i class="bx bx-check-circle text-lg"></i>
            Confirmer la réception
          </button>
        </div>
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
const { orderDetail, loading, error, fetchOrderDetail, updateOrderStatus } = useMarketplace();

const handleConfirmReceipt = async () => {
  if (!confirm("Avez-vous bien reçu votre commande ? Cette action libérera les fonds pour le vendeur.")) return;
  try {
    await updateOrderStatus(orderDetail.value.id, 'DELIVERED');
    alert("Merci ! Votre commande est maintenant terminée.");
  } catch (err: any) {
    alert("Une erreur est survenue.");
  }
};

const statusSteps = [
  { key: 'PENDING', label: 'Commande passée', icon: 'bx bx-time' },
  { key: 'PAID', label: 'Paiement reçu', icon: 'bx bx-credit-card' },
  { key: 'CONFIRMED', label: 'En préparation', icon: 'bx bx-check-double' },
  { key: 'SHIPPED', label: 'En cours de livraison', icon: 'bx bx-package' },
  { key: 'DELIVERED', label: 'Commande livrée', icon: 'bx bx-home-heart' }
];

onMounted(() => {
  if (route.params.id) {
    fetchOrderDetail(route.params.id as string);
  }
});

const formatDate = (dateStr?: string) => {
  if (!dateStr) return '';
  return new Date(dateStr).toLocaleDateString('fr-FR', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

const getStatusLabel = (status?: string) => {
  if (!status) return '';
  const statuses: Record<string, string> = {
    'PENDING': 'En attente',
    'PAID': 'Payé',
    'CONFIRMED': 'Confirmé',
    'SHIPPED': 'Expédié',
    'DELIVERED': 'Livré',
    'CANCELLED': 'Annulé'
  };
  return statuses[status] || status;
};

const getStatusClass = (status?: string) => {
  switch (status) {
    case 'DELIVERED': return 'bg-emerald-100 text-emerald-600';
    case 'PENDING': return 'bg-amber-100 text-amber-600';
    case 'CANCELLED': return 'bg-rose-100 text-rose-600';
    case 'SHIPPED': return 'bg-blue-100 text-blue-600';
    default: return 'bg-gray-100 text-gray-600';
  }
};

const isStepCompleted = (stepKey: string, currentStatus: string) => {
  const order = ['PENDING', 'PAID', 'CONFIRMED', 'SHIPPED', 'DELIVERED'];
  const currentIndex = order.indexOf(currentStatus);
  const stepIndex = order.indexOf(stepKey);
  return stepIndex < currentIndex && stepIndex !== -1;
};

const isStepActive = (stepKey: string, currentStatus: string) => {
  return stepKey === currentStatus;
};

const getProgressWidth = (currentStatus: string) => {
  const order = ['PENDING', 'PAID', 'CONFIRMED', 'SHIPPED', 'DELIVERED'];
  const index = order.indexOf(currentStatus);
  if (index === -1) return 0;
  return (index / (order.length - 1)) * 100;
};
</script>
