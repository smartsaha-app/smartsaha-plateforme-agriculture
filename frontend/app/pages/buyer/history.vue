<template>
  <div class="space-y-8">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-3xl font-black text-[#112830]">Historique des commandes</h1>
        <p class="text-gray-500 font-medium">Consultez l'ensemble de vos transactions passées.</p>
      </div>
    </div>

    <!-- Orders List (Reuse logic from orders) -->
    <div v-if="loading" class="space-y-4">
      <div v-for="i in 5" :key="i" class="h-28 bg-white rounded-3xl border border-gray-100 animate-pulse"></div>
    </div>

    <div v-else-if="orders.length === 0" class="bg-white py-24 rounded-[3rem] border border-gray-100 text-center space-y-6">
      <div class="w-24 h-24 bg-gray-50 rounded-full flex items-center justify-center mx-auto text-gray-200">
        <i class="bx bx-history text-5xl"></i>
      </div>
      <div class="space-y-2">
        <h3 class="text-xl font-black text-[#112830]">Historique vide</h3>
        <p class="text-gray-400 max-w-sm mx-auto">Vous n'avez pas encore effectué d'achats sur la plateforme.</p>
      </div>
    </div>

    <div v-else class="grid grid-cols-1 gap-4">
      <div 
        v-for="order in orders" 
        :key="order.id"
        @click="navigateTo(`/buyer/orders/${order.id}`)"
        class="bg-white p-6 md:p-8 rounded-[2.5rem] border border-gray-100 shadow-sm hover:shadow-md hover:border-[#10b481]/30 transition-all cursor-pointer group relative overflow-hidden"
      >
        <div class="flex flex-col md:flex-row md:items-center gap-6 relative z-10">
          <div class="flex items-center gap-6 flex-1">
            <div class="w-16 h-16 bg-gray-50 rounded-3xl flex items-center justify-center text-[#112830] group-hover:bg-emerald-50 group-hover:text-[#10b481] transition-colors flex-shrink-0">
              <i class="bx bx-package text-3xl"></i>
            </div>
            <div class="min-w-0">
              <div class="flex items-center gap-3 mb-1">
                <h3 class="text-lg font-black text-[#112830] truncate">{{ order.order_number }}</h3>
                <span :class="getStatusClass(order.status)" class="px-3 py-1 rounded-full text-[9px] font-black uppercase tracking-wider">
                  {{ getStatusLabel(order.status) }}
                </span>
              </div>
              <p class="text-sm font-bold text-gray-400">
                Le {{ formatDate(order.created_at) }}
              </p>
            </div>
          </div>

          <div class="text-right">
            <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest mb-1">Total</p>
            <p class="text-xl font-black text-[#10b481]">{{ order.total }} Ar</p>
          </div>
          <div class="w-12 h-12 rounded-2xl bg-gray-50 flex items-center justify-center group-hover:bg-[#112830] group-hover:text-white transition-all">
            <i class="bx bx-chevron-right text-2xl"></i>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useMarketplace } from '~/composables/useMarketplace';

definePageMeta({
  layout: 'dashboard'
});

const { orders, loading, fetchOrders } = useMarketplace();

onMounted(() => {
  fetchOrders();
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
