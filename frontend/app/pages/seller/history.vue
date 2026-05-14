<template>
  <div class="space-y-8 pb-20">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-3xl font-black text-[#112830]">Historique des ventes</h1>
        <p class="text-gray-500 font-medium">Consultez l'ensemble de vos transactions terminées.</p>
      </div>
    </div>

    <!-- Orders Table -->
    <div v-if="loading" class="space-y-4 animate-pulse">
      <div v-for="i in 5" :key="i" class="h-24 bg-white rounded-[2rem] border border-gray-50 shadow-sm"></div>
    </div>

    <div v-else-if="filteredOrders.length === 0" class="bg-white py-24 rounded-[3rem] border border-gray-100 text-center space-y-6 shadow-sm">
      <div class="w-24 h-24 bg-gray-50 rounded-full flex items-center justify-center mx-auto text-gray-200">
        <i class="bx bx-history text-5xl"></i>
      </div>
      <div class="space-y-2">
        <h3 class="text-xl font-black text-[#112830]">Aucun historique</h3>
        <p class="text-gray-400 max-w-sm mx-auto">Vous n'avez pas encore de commandes terminées.</p>
      </div>
    </div>

    <div v-else class="bg-white rounded-[3rem] border border-gray-50 shadow-sm overflow-hidden">
      <table class="w-full text-left">
        <thead>
          <tr class="bg-gray-50/50">
            <th class="px-8 py-5 text-[10px] font-black text-gray-400 uppercase tracking-widest">N° Commande</th>
            <th class="px-8 py-5 text-[10px] font-black text-gray-400 uppercase tracking-widest">Acheteur</th>
            <th class="px-8 py-5 text-[10px] font-black text-gray-400 uppercase tracking-widest">Articles</th>
            <th class="px-8 py-5 text-[10px] font-black text-gray-400 uppercase tracking-widest">Total</th>
            <th class="px-8 py-5 text-[10px] font-black text-gray-400 uppercase tracking-widest">Statut</th>
            <th class="px-8 py-5"></th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-50">
          <tr v-for="order in filteredOrders" :key="order.id" class="hover:bg-gray-50/50 transition-colors group">
            <td class="px-8 py-6">
              <p class="font-black text-[#112830]">{{ order.order_number }}</p>
              <p class="text-[10px] text-gray-400 font-bold uppercase tracking-widest">{{ new Date(order.created_at).toLocaleDateString() }}</p>
            </td>
            <td class="px-8 py-6">
              <div class="flex items-center gap-3">
                <div class="w-9 h-9 bg-gray-100 rounded-xl flex items-center justify-center text-gray-400">
                  <i class="bx bx-user text-xl"></i>
                </div>
                <div>
                  <p class="text-sm font-black text-[#112830]">{{ order.buyer_details?.username || 'Client' }}</p>
                  <p class="text-[10px] text-gray-400 font-bold">{{ order.buyer_details?.email }}</p>
                </div>
              </div>
            </td>
            <td class="px-8 py-6">
              <div class="flex -space-x-3 overflow-hidden">
                <div v-for="item in order.items?.slice(0, 3)" :key="item.id" class="inline-block h-8 w-8 rounded-lg ring-2 ring-white bg-gray-50 overflow-hidden border border-gray-100">
                  <img v-if="item.product_image" :src="item.product_image" class="h-full w-full object-cover">
                  <div v-else class="h-full w-full flex items-center justify-center text-gray-300">
                    <i class="bx bx-image text-xs"></i>
                  </div>
                </div>
                <div v-if="order.items?.length > 3" class="inline-block h-8 w-8 rounded-lg ring-2 ring-white bg-gray-100 flex items-center justify-center text-[10px] font-black text-gray-400">
                  +{{ order.items.length - 3 }}
                </div>
              </div>
            </td>
            <td class="px-8 py-6">
              <p class="font-black text-[#10b481]">{{ order.total }} Ar</p>
            </td>
            <td class="px-8 py-6">
               <span class="px-3 py-1.5 rounded-xl text-[9px] font-black uppercase tracking-widest border border-gray-100" :class="getStatusClass(order.status)">
                 {{ order.status }}
               </span>
            </td>
            <td class="px-8 py-6 text-right">
              <button class="w-10 h-10 rounded-xl hover:bg-gray-50 text-gray-400 hover:text-[#112830] transition-all">
                <i class="bx bx-show text-2xl"></i>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useApi } from '~/composables/useApi';

definePageMeta({
  layout: 'dashboard'
});

const { apiFetch } = useApi();
const orders = ref<any[]>([]);
const loading = ref(true);

const filteredOrders = computed(() => {
  const all = orders.value || [];
  // L'historique montre les commandes terminées (Livrées ou Annulées)
  return all.filter(o => o.status === 'DELIVERED' || o.status === 'CANCELLED');
});

onMounted(async () => {
  try {
    const data = await apiFetch('/api/orders/orders/?as_seller=true');
    orders.value = data.results || data;
  } catch (err) {
    console.error('Failed to load orders', err);
  } finally {
    loading.value = false;
  }
});

const getStatusClass = (status: string) => {
  switch (status) {
    case 'PENDING': return 'text-amber-600 bg-amber-50';
    case 'PAID': return 'text-emerald-600 bg-emerald-50';
    case 'SHIPPED': return 'text-blue-600 bg-blue-50';
    case 'DELIVERED': return 'text-emerald-600 bg-emerald-100';
    case 'CANCELLED': return 'text-rose-600 bg-rose-50';
    default: return 'text-gray-600 bg-gray-50';
  }
};
</script>
