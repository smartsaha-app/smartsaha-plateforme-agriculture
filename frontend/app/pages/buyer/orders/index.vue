<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8 space-y-6">

    <!-- ===== HEADER ===== -->
    <PageHeader :title="t('buyer.ordersTitle')">
      <template #subtitle>
        <i class="bx bx-package"></i>
        {{ t('buyer.ordersDesc') }}
      </template>
      <template #breadcrumb>
        <NuxtLink to="/buyer/dashboard" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
          <span>Accueil</span>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">Commandes</span>
      </template>
    </PageHeader>

    <!-- ===== TOOLBAR ===== -->
    <div class="flex flex-col sm:flex-row gap-3 items-start sm:items-center justify-between">
      <!-- Recherche -->
      <div class="relative flex-1 max-w-sm">
        <i class="bx bx-search absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-base pointer-events-none"></i>
        <input v-model="searchQuery" type="text" :placeholder="t('buyer.searchOrder')"
          class="w-full pl-9 pr-8 py-2.5 bg-white border border-gray-100 rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/30 transition-all font-medium text-[#112830] shadow-sm" />
        <button v-if="searchQuery" @click="searchQuery = ''" class="absolute right-2.5 top-1/2 -translate-y-1/2 text-gray-300 hover:text-gray-500">
          <i class="bx bx-x"></i>
        </button>
      </div>
      <span class="text-xs font-bold text-gray-400">
        {{ filteredOrders.length }} commande{{ filteredOrders.length !== 1 ? 's' : '' }}
      </span>
    </div>

    <!-- ===== FILTER TABS ===== -->
    <div class="flex gap-1.5 overflow-x-auto pb-1">
      <button v-for="filter in filters" :key="filter.value"
        @click="activeFilter = filter.value"
        :class="[
          'px-4 py-2 rounded-xl whitespace-nowrap font-bold text-xs transition-all flex-shrink-0',
          activeFilter === filter.value ? 'bg-[#112830] text-white shadow-sm' : 'bg-white text-gray-400 hover:bg-gray-50 border border-gray-100'
        ]">
        {{ filter.label }}
        <span v-if="countByFilter(filter.value) > 0"
          class="ml-1.5 px-1.5 py-0.5 rounded-full text-[8px] font-black"
          :class="activeFilter === filter.value ? 'bg-white/20 text-white' : 'bg-gray-100 text-gray-500'">
          {{ countByFilter(filter.value) }}
        </span>
      </button>
    </div>

    <!-- ===== LOADING ===== -->
    <div v-if="loading" class="space-y-3">
      <div v-for="i in 5" :key="i" class="h-24 bg-white rounded-2xl border border-gray-100 animate-pulse"></div>
    </div>

    <!-- ===== EMPTY ===== -->
    <div v-else-if="filteredOrders.length === 0" class="bg-white py-20 rounded-2xl border border-gray-100 text-center space-y-5 shadow-sm">
      <div class="w-20 h-20 bg-gray-50 rounded-2xl flex items-center justify-center mx-auto">
        <i class="bx bx-package text-4xl text-gray-200"></i>
      </div>
      <div>
        <h3 class="text-base font-black text-[#112830]">{{ t('buyer.noOrders') }} trouvée</h3>
        <p class="text-sm text-gray-400 mt-1">Vous n'avez pas encore passé de commande ou aucune ne correspond à vos filtres.</p>
      </div>
      <NuxtLink to="/buyer/products"
        class="inline-flex items-center gap-2 px-5 py-2.5 bg-[#10b481] text-white rounded-xl font-bold text-sm shadow-sm hover:bg-emerald-400 transition-all">
        <i class="bx bx-store"></i>
        Aller à la boutique
      </NuxtLink>
    </div>

    <!-- ===== ORDERS LIST ===== -->
    <div v-else class="space-y-3">
      <div v-for="order in filteredOrders" :key="order.id"
        @click="navigateTo(`/buyer/orders/${order.id}`)"
        class="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md hover:border-[#10b481]/20 transition-all cursor-pointer group">

        <div class="flex flex-col sm:flex-row sm:items-center gap-4">
          <!-- Icon + info -->
          <div class="flex items-center gap-4 flex-1 min-w-0">
            <div class="w-12 h-12 bg-gray-50 rounded-xl flex items-center justify-center text-[#112830] group-hover:bg-emerald-50 group-hover:text-[#10b481] transition-colors flex-shrink-0">
              <i class="bx bx-shopping-bag text-xl"></i>
            </div>
            <div class="min-w-0">
              <div class="flex items-center gap-2 mb-0.5 flex-wrap">
                <h3 class="text-sm font-black text-[#112830] truncate">{{ order.order_number }}</h3>
                <span :class="getStatusClass(order.status)"
                  class="px-2 py-0.5 rounded-lg text-[8px] font-black uppercase tracking-wider flex-shrink-0">
                  {{ getStatusLabel(order.status) }}
                </span>
              </div>
              <p class="text-xs font-medium text-gray-400">{{ formatDate(order.created_at) }}</p>
            </div>
          </div>

          <!-- Aperçu articles -->
          <div class="hidden lg:flex -space-x-3 flex-shrink-0">
            <div v-for="(item, idx) in order.items?.slice(0, 3)" :key="idx"
              class="w-10 h-10 rounded-xl border-2 border-white overflow-hidden bg-gray-100"
              :style="{ transitionDelay: idx * 50 + 'ms' }">
              <img v-if="item.product_image" :src="item.product_image" class="w-full h-full object-cover" />
              <div v-else class="w-full h-full flex items-center justify-center text-gray-300">
                <i class="bx bx-image text-xs"></i>
              </div>
            </div>
            <div v-if="order.items?.length > 3"
              class="w-10 h-10 rounded-xl border-2 border-white bg-gray-100 flex items-center justify-center text-[9px] font-black text-gray-400">
              +{{ (order.items?.length ?? 0) - 3 }}
            </div>
          </div>

          <!-- Montant + chevron -->
          <div class="flex items-center justify-between sm:justify-end gap-6 border-t sm:border-t-0 pt-3 sm:pt-0">
            <div class="text-right">
              <p class="text-[9px] font-black text-gray-400 uppercase tracking-widest mb-0.5">{{ t('buyer.total') }}</p>
              <p class="text-base font-black text-[#10b481]">{{ order.total }} Ar</p>
            </div>
            <div class="w-9 h-9 rounded-xl bg-gray-50 flex items-center justify-center group-hover:bg-[#112830] group-hover:text-white transition-all">
              <i class="bx bx-chevron-right text-lg"></i>
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

const { t } = useI18n();
definePageMeta({ layout: 'dashboard' });

const { orders, loading, fetchOrders } = useMarketplace();
const activeFilter = ref('ALL');
const searchQuery  = ref('');

const filters = computed(() => [
  { label: t('buyer.filterAll2'),      value: 'ALL'       },
  { label: t('buyer.statusPending'),   value: 'PENDING'   },
  { label: t('buyer.statusPaid'),      value: 'PAID'      },
  { label: t('buyer.statusShipped'),   value: 'SHIPPED'   },
  { label: t('buyer.statusDelivered'), value: 'DELIVERED' },
  { label: t('buyer.statusCancelled'), value: 'CANCELLED' },
]);

onMounted(() => fetchOrders());

function countByFilter(value: string) {
  const all = orders.value || [];
  if (value === 'ALL') return all.length;
  return all.filter((o: any) => o.status === value).length;
}

const filteredOrders = computed(() => {
  let list = orders.value || [];
  if (activeFilter.value !== 'ALL') list = list.filter((o: any) => o.status === activeFilter.value);
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase();
    list = list.filter((o: any) => o.order_number?.toLowerCase().includes(q));
  }
  return list;
});

const formatDate = (d: string) =>
  new Date(d).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' });

const getStatusLabel = (status: string) => {
  const map: Record<string, string> = {
    PENDING: 'En attente', PAID: 'Payée', CONFIRMED: 'Confirmée',
    SHIPPED: 'Expédiée', DELIVERED: 'Livrée', CANCELLED: 'Annulée',
  };
  return map[status] || status;
};

const getStatusClass = (status: string) => {
  switch (status) {
    case 'DELIVERED': return 'bg-emerald-100 text-emerald-600';
    case 'PENDING':   return 'bg-amber-100 text-amber-600';
    case 'CANCELLED': return 'bg-rose-100 text-rose-600';
    case 'SHIPPED':   return 'bg-blue-100 text-blue-600';
    case 'PAID':      return 'bg-emerald-50 text-[#10b481]';
    default:          return 'bg-gray-100 text-gray-600';
  }
};
</script>