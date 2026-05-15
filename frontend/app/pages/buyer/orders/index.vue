<template>
  <div class="space-y-8">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-3xl font-black text-[#112830]">Mes Commandes</h1>
        <p class="text-gray-500 font-medium">Historique de vos achats sur la plateforme.</p>
      </div>
      <div class="flex gap-3">
        <div class="relative group hidden md:block">
          <i class="bx bx-search absolute left-4 top-1/2 -translate-y-1/2 text-gray-300 group-focus-within:text-[#10b481] transition-colors"></i>
          <input 
            type="text" 
            placeholder="Rechercher une commande..." 
            class="pl-12 pr-6 py-3 bg-white border border-gray-100 rounded-2xl outline-none focus:ring-2 focus:ring-[#10b481]/50 transition-all text-sm font-medium w-64 shadow-sm"
          />
        </div>
      </div>
    </div>

    <!-- Filters -->
    <div class="flex gap-3 overflow-x-auto pb-4 no-scrollbar">
      <button 
        v-for="filter in filters" 
        :key="filter.value"
        @click="activeFilter = filter.value"
        :class="[activeFilter === filter.value ? 'bg-[#112830] text-white shadow-lg shadow-[#112830]/10' : 'bg-white text-gray-400 hover:bg-gray-50 border-gray-100']"
        class="px-6 py-3 rounded-2xl whitespace-nowrap font-black text-[10px] uppercase tracking-widest transition-all border shadow-sm"
      >
        {{ filter.label }}
      </button>
    </div>

    <!-- Orders List -->
    <div v-if="loading" class="space-y-4">
      <div v-for="i in 5" :key="i" class="h-28 bg-white rounded-3xl border border-gray-100 animate-pulse"></div>
    </div>

    <div v-else-if="filteredOrders.length === 0" class="bg-white py-24 rounded-[3rem] border border-gray-100 text-center space-y-6">
      <div class="w-24 h-24 bg-gray-50 rounded-full flex items-center justify-center mx-auto text-gray-200">
        <i class="bx bx-package text-5xl"></i>
      </div>
      <div class="space-y-2">
        <h3 class="text-xl font-black text-[#112830]">Aucune commande trouvée</h3>
        <p class="text-gray-400 max-w-sm mx-auto">Vous n'avez pas encore passé de commande ou aucune ne correspond à vos filtres.</p>
      </div>
      <NuxtLink to="/marketplace" class="inline-flex items-center gap-2 px-8 py-4 bg-[#10b481] text-white rounded-2xl font-black text-xs uppercase tracking-widest shadow-lg shadow-[#10b481]/20 hover:scale-105 transition-all">
        Aller à la boutique
      </NuxtLink>
    </div>

    <div v-else class="grid grid-cols-1 gap-4">
      <div 
        v-for="order in filteredOrders" 
        :key="order.id"
        @click="navigateTo(`/buyer/orders/${order.id}`)"
        class="bg-white p-6 md:p-8 rounded-[2.5rem] border border-gray-100 shadow-sm hover:shadow-md hover:border-[#10b481]/30 transition-all cursor-pointer group relative overflow-hidden"
      >
        <div class="flex flex-col md:flex-row md:items-center gap-6 relative z-10">
          <!-- Icon & Info -->
          <div class="flex items-center gap-6 flex-1">
            <div class="w-16 h-16 bg-gray-50 rounded-3xl flex items-center justify-center text-[#112830] group-hover:bg-emerald-50 group-hover:text-[#10b481] transition-colors flex-shrink-0">
              <i class="bx bx-shopping-bag text-3xl"></i>
            </div>
            <div class="min-w-0">
              <div class="flex items-center gap-3 mb-1">
                <h3 class="text-lg font-black text-[#112830] truncate">{{ order.order_number }}</h3>
                <span :class="getStatusClass(order.status)" class="px-3 py-1 rounded-full text-[9px] font-black uppercase tracking-wider">
                  {{ getStatusLabel(order.status) }}
                </span>
              </div>
              <p class="text-sm font-bold text-gray-400">
                Commandée le {{ formatDate(order.created_at) }}
              </p>
            </div>
          </div>

          <!-- Items Preview -->
          <div class="hidden lg:flex -space-x-4">
             <div v-for="(item, idx) in order.items?.slice(0, 3)" :key="idx" class="w-12 h-12 rounded-2xl border-4 border-white overflow-hidden bg-gray-100 relative group-hover:translate-y-[-4px] transition-transform" :style="{ transitionDelay: idx * 50 + 'ms' }">
                <img v-if="item.product_image" :src="item.product_image" class="w-full h-full object-cover" />
                <div v-else class="w-full h-full flex items-center justify-center text-gray-300">
                  <i class="bx bx-image text-xl"></i>
                </div>
             </div>
             <div v-if="order.items?.length > 3" class="w-12 h-12 rounded-2xl border-4 border-white bg-gray-100 flex items-center justify-center text-[10px] font-black text-gray-400 relative">
               +{{ order.items.length - 3 }}
             </div>
          </div>

          <!-- Price & Action -->
          <div class="flex items-center justify-between md:justify-end gap-8 border-t md:border-t-0 pt-4 md:pt-0">
            <div class="text-right">
              <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest mb-1">Montant Total</p>
              <p class="text-xl font-black text-[#10b481]">{{ order.total }} Ar</p>
            </div>
            <div class="w-12 h-12 rounded-2xl bg-gray-50 flex items-center justify-center group-hover:bg-[#112830] group-hover:text-white transition-all">
              <i class="bx bx-chevron-right text-2xl"></i>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useMarketplace } from '~/composables/useMarketplace';

definePageMeta({
  layout: 'dashboard'
});

const { orders, loading, fetchOrders } = useMarketplace();
const activeFilter = ref('ALL');

const filters = [
  { label: 'Toutes', value: 'ALL' },
  { label: 'En attente', value: 'PENDING' },
  { label: 'Payées', value: 'PAID' },
  { label: 'En livraison', value: 'SHIPPED' },
  { label: 'Livrées', value: 'DELIVERED' },
  { label: 'Annulées', value: 'CANCELLED' }
];

onMounted(() => {
  fetchOrders();
});

const filteredOrders = computed(() => {
  const all = orders.value || [];
  if (activeFilter.value === 'ALL') return all; // Toutes les commandes de l'utilisateur
  return all.filter((o: any) => o.status === activeFilter.value);
});

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleDateString('fr-FR', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  });
};

const getStatusLabel = (status: string) => {
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

const getStatusClass = (status: string) => {
  switch (status) {
    case 'DELIVERED': return 'bg-emerald-100 text-emerald-600';
    case 'PENDING': return 'bg-amber-100 text-amber-600';
    case 'CANCELLED': return 'bg-rose-100 text-rose-600';
    case 'SHIPPED': return 'bg-blue-100 text-blue-600';
    case 'PAID': return 'bg-emerald-50 text-[#10b481]';
    default: return 'bg-gray-100 text-gray-600';
  }
};
</script>

<style scoped>
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
