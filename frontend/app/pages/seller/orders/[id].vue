<template>
  <div class="space-y-8">
    <!-- Header -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div class="space-y-2">
        <button @click="router.back()" class="flex items-center gap-2 text-[10px] font-black text-gray-400 uppercase tracking-widest hover:text-[#10b481] transition-all">
          <i class="bx bx-left-arrow-alt text-lg"></i>
          Retour à la liste
        </button>
        <h1 class="text-3xl font-black text-[#112830]">Commande {{ orderDetail?.order_number }}</h1>
        <div class="flex items-center gap-3">
          <span :class="getStatusClass(orderDetail?.status)" class="px-3 py-1 rounded-full text-[9px] font-black uppercase tracking-wider">
            {{ getStatusLabel(orderDetail?.status) }}
          </span>
          <p class="text-sm font-bold text-gray-400">Reçue le {{ formatDate(orderDetail?.created_at) }}</p>
        </div>
      </div>
      
      <div class="flex gap-3 w-full md:w-auto">
        <button class="flex-1 md:flex-none px-6 py-3 bg-white border border-gray-100 rounded-2xl font-black text-[10px] uppercase tracking-widest hover:bg-gray-50 transition-all flex items-center justify-center gap-2">
          <i class="bx bx-printer text-lg"></i>
          Bon de commande
        </button>
      </div>
    </div>

    <!-- Actions Bar (Floating) -->
    <div v-if="orderDetail?.status !== 'DELIVERED' && orderDetail?.status !== 'CANCELLED'" class="bg-[#112830] p-6 rounded-[2.5rem] shadow-xl shadow-[#112830]/20 flex flex-col md:flex-row items-center justify-between gap-6">
      <div class="flex items-center gap-4">
        <div class="w-12 h-12 bg-[#10b481] text-white rounded-2xl flex items-center justify-center text-2xl">
          <i class="bx bx-zap"></i>
        </div>
        <div>
          <h3 class="text-white font-black text-sm">Action requise</h3>
          <p class="text-gray-400 text-xs font-medium">{{ getNextActionText(orderDetail?.status) }}</p>
        </div>
      </div>
      
      <div class="flex gap-3 w-full md:w-auto">
        <button 
          v-if="orderDetail?.status === 'PAID'"
          @click="updateStatus('CONFIRMED')"
          :disabled="loading"
          class="flex-1 md:flex-none px-8 py-4 bg-[#10b481] text-white rounded-2xl font-black text-[10px] uppercase tracking-widest hover:scale-105 transition-all shadow-lg shadow-[#10b481]/20"
        >
          Confirmer la commande
        </button>
        
        <button 
          v-if="orderDetail?.status === 'CONFIRMED'"
          @click="updateStatus('SHIPPED')"
          :disabled="loading"
          class="flex-1 md:flex-none px-8 py-4 bg-blue-500 text-white rounded-2xl font-black text-[10px] uppercase tracking-widest hover:scale-105 transition-all shadow-lg shadow-blue-500/20"
        >
          Marquer comme expédié
        </button>

        <button 
          v-if="orderDetail?.status === 'SHIPPED'"
          @click="updateStatus('DELIVERED')"
          :disabled="loading"
          class="flex-1 md:flex-none px-8 py-4 bg-emerald-500 text-white rounded-2xl font-black text-[10px] uppercase tracking-widest hover:scale-105 transition-all shadow-lg shadow-emerald-500/20"
        >
          Confirmer la livraison
        </button>
      </div>
    </div>

    <!-- Content Grid -->
    <div v-if="orderDetail" class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Left: Order Items -->
      <div class="lg:col-span-2 space-y-6">
        <div class="bg-white rounded-[3rem] border border-gray-100 shadow-sm overflow-hidden">
          <div class="p-8 border-b border-gray-50 flex items-center justify-between">
            <h3 class="text-lg font-black text-[#112830]">Produits commandés</h3>
            <span class="px-3 py-1 bg-gray-50 text-gray-500 rounded-full text-[10px] font-black uppercase">{{ orderDetail.items?.length }} Articles</span>
          </div>
          <div class="divide-y divide-gray-50">
            <div v-for="item in orderDetail.items" :key="item.id" class="p-8 flex gap-6 items-center">
              <div class="w-20 h-20 bg-gray-50 rounded-3xl overflow-hidden flex-shrink-0 border border-gray-100">
                <img v-if="item.product_image" :src="item.product_image" class="w-full h-full object-cover" />
                <i v-else class="bx bx-image text-gray-200 text-3xl m-auto"></i>
              </div>
              <div class="flex-1 min-w-0">
                <p class="text-lg font-black text-[#112830] truncate">{{ item.product_name }}</p>
                <p class="text-sm font-bold text-[#10b481]">{{ item.price }} Ar / unité</p>
              </div>
              <div class="text-right">
                <p class="text-sm font-bold text-gray-400 uppercase tracking-widest">Quantité commandée</p>
                <p class="text-xl font-black text-[#112830]">x {{ item.quantity }}</p>
                <p v-if="item.product_stock !== undefined" class="text-[10px] font-black mt-1 uppercase tracking-widest" :class="item.product_stock < 5 ? 'text-rose-500' : 'text-gray-400'">
                  Stock actuel: {{ item.product_stock }}
                </p>
              </div>
              <div class="text-right pl-8 border-l border-gray-50 min-w-[120px]">
                <p class="text-sm font-bold text-gray-400 uppercase tracking-widest">Sous-total</p>
                <p class="text-xl font-black text-[#112830]">{{ item.subtotal }} Ar</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right: Delivery & Customer -->
      <div class="space-y-8">
        <div class="bg-white p-8 rounded-[2.5rem] border border-gray-100 shadow-sm space-y-6">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-blue-50 text-blue-500 rounded-xl flex items-center justify-center text-xl">
              <i class="bx bx-user"></i>
            </div>
            <h3 class="text-lg font-black text-[#112830]">Client</h3>
          </div>
          <div class="space-y-4">
            <div class="p-4 bg-gray-50 rounded-2xl flex items-center gap-4">
              <div class="w-10 h-10 bg-white rounded-full flex items-center justify-center font-black text-[#112830] shadow-sm">
                {{ orderDetail.buyer_name?.charAt(0) }}
              </div>
              <div>
                <p class="text-sm font-black text-[#112830]">{{ orderDetail.buyer_name }}</p>
                <p class="text-[10px] font-bold text-gray-400 uppercase tracking-widest">{{ orderDetail.buyer_details?.email }}</p>
              </div>
            </div>
            
            <div class="space-y-3 pt-2">
               <div class="flex items-center gap-3 text-sm text-gray-500">
                 <i class="bx bx-phone text-gray-300"></i>
                 <span class="font-bold">{{ orderDetail.delivery_phone }}</span>
               </div>
               <div class="flex items-start gap-3 text-sm text-gray-500">
                 <i class="bx bx-map text-gray-300 mt-1"></i>
                 <span class="font-bold">{{ orderDetail.delivery_address }}, {{ orderDetail.delivery_city }}</span>
               </div>
            </div>
          </div>
        </div>

        <div class="bg-white p-8 rounded-[2.5rem] border border-gray-100 shadow-sm space-y-6">
          <h3 class="text-lg font-black text-[#112830]">Résumé financier</h3>
          <div class="space-y-3">
            <div class="flex justify-between text-sm">
              <span class="text-gray-400 font-bold">Produits</span>
              <span class="text-[#112830] font-black">{{ orderDetail.subtotal }} Ar</span>
            </div>
            <div class="flex justify-between text-sm">
              <span class="text-gray-400 font-bold">Commission SmartSaha</span>
              <span class="text-rose-500 font-black">- 0 Ar</span>
            </div>
            <div class="pt-4 border-t border-gray-50 flex justify-between items-center">
              <span class="text-lg font-black text-[#112830]">Net à recevoir</span>
              <span class="text-2xl font-black text-[#10b481]">{{ orderDetail.subtotal }} Ar</span>
            </div>
            <div v-if="orderDetail.payment_status === 'ESCROWED'" class="mt-4 p-3 bg-emerald-50 text-emerald-600 rounded-xl text-[10px] font-black uppercase text-center tracking-widest border border-emerald-100">
              <i class="bx bx-lock-alt mr-1"></i>
              Fonds en séquestre
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useMarketplace } from '~/composables/useMarketplace';

definePageMeta({
  layout: 'dashboard'
});

const route = useRoute();
const router = useRouter();
const { orderDetail, loading, fetchOrderDetail, updateOrderStatus } = useMarketplace();

onMounted(() => {
  if (route.params.id) {
    fetchOrderDetail(route.params.id as string);
  }
});

const updateStatus = async (status: string) => {
  if (!confirm(`Confirmer le passage au statut: ${getStatusLabel(status)} ?`)) return;
  try {
    await updateOrderStatus(orderDetail.value.id, status);
    alert("Statut mis à jour avec succès");
  } catch (err: any) {
    alert("Erreur: " + err.message);
  }
};

const formatDate = (dateStr: string) => {
  if (!dateStr) return '';
  return new Date(dateStr).toLocaleDateString('fr-FR', {
    day: 'numeric', month: 'long', year: 'numeric'
  });
};

const getStatusLabel = (status: string) => {
  const statuses: any = {
    'PENDING': 'Attente Paiement',
    'PAID': 'Payé (À préparer)',
    'CONFIRMED': 'En préparation',
    'SHIPPED': 'Expédié',
    'DELIVERED': 'Livré',
    'CANCELLED': 'Annulé'
  };
  return statuses[status] || status;
};

const getStatusClass = (status: string) => {
  switch (status) {
    case 'PAID': return 'bg-emerald-50 text-[#10b481]';
    case 'CONFIRMED': return 'bg-blue-50 text-blue-600';
    case 'SHIPPED': return 'bg-amber-50 text-amber-600';
    case 'DELIVERED': return 'bg-emerald-100 text-emerald-600';
    default: return 'bg-gray-100 text-gray-600';
  }
};

const getNextActionText = (status: string) => {
  switch (status) {
    case 'PENDING': return 'En attente du règlement de l\'acheteur.';
    case 'PAID': return 'Le paiement a été reçu. Veuillez préparer la commande et confirmer.';
    case 'CONFIRMED': return 'La commande est prête. Remettez-la au livreur et marquez-la comme expédiée.';
    case 'SHIPPED': return 'Le colis est en route. Confirmez la livraison une fois reçue.';
    case 'DELIVERED': return 'Commande terminée et fonds débloqués.';
    default: return 'Aucune action requise.';
  }
};
</script>
