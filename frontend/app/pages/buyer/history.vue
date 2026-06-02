<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8 space-y-6">

    <!-- ===== HEADER ===== -->
    <PageHeader :title="t('buyer.buyerHistoryTitle')">
      <template #subtitle>
        <i class="bx bx-history"></i>
        {{ t('buyer.buyerHistoryDesc') }}
      </template>
      <template #breadcrumb>
        <NuxtLink to="/buyer/dashboard" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
          <span>{{ t('dashboard.home') }}</span>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">{{ t('dashboard.history') }}</span>
      </template>
    </PageHeader>

    <!-- ===== FILTERS ===== -->
    <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-3 flex items-center gap-2 overflow-x-auto">
      <div class="flex gap-1.5 flex-shrink-0">
        <button v-for="f in statusFilters" :key="f.value"
          @click="filterStatus = f.value"
          :class="[
            'px-4 py-2 rounded-xl text-xs font-bold transition-all flex-shrink-0',
            filterStatus === f.value ? 'bg-[#112830] text-white' : 'bg-gray-50 text-gray-400 hover:bg-gray-100'
          ]">
          {{ f.label }}
          <span v-if="countByStatus(f.value) > 0"
            class="ml-1.5 px-1.5 py-0.5 rounded-full text-[8px] font-black"
            :class="filterStatus === f.value ? 'bg-white/20 text-white' : 'bg-gray-200 text-gray-500'">
            {{ countByStatus(f.value) }}
          </span>
        </button>
      </div>

      <div class="hidden md:block w-px h-7 bg-gray-100 flex-shrink-0"></div>

      <div class="flex-1 min-w-[140px] relative">
        <i class="bx bx-search absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-sm pointer-events-none"></i>
        <input v-model="search" type="text" placeholder="Rechercher..."
          class="w-full pl-9 pr-7 py-2 bg-gray-50 border border-gray-100 rounded-xl text-xs outline-none focus:ring-2 focus:ring-[#10b481]/20 font-medium text-[#112830]" />
        <button v-if="search" @click="search = ''" class="absolute right-2 top-1/2 -translate-y-1/2 text-gray-300 hover:text-gray-500">
          <i class="bx bx-x text-sm"></i>
        </button>
      </div>

      <span class="ml-auto text-xs font-bold text-gray-400 whitespace-nowrap flex-shrink-0">
        {{ filteredOrders.length }} commande{{ filteredOrders.length !== 1 ? 's' : '' }}
      </span>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="space-y-3">
      <div v-for="i in 5" :key="i" class="h-20 bg-white rounded-2xl border border-gray-100 animate-pulse"></div>
    </div>

    <!-- Empty -->
    <div v-else-if="filteredOrders.length === 0" class="bg-white py-20 rounded-2xl border border-gray-100 text-center space-y-5 shadow-sm">
      <div class="w-20 h-20 bg-gray-50 rounded-2xl flex items-center justify-center mx-auto">
        <i class="bx bx-history text-4xl text-gray-200"></i>
      </div>
      <div>
        <h3 class="text-base font-black text-[#112830]">{{ t('buyer.historyEmpty') }}</h3>
        <p class="text-sm text-gray-400 mt-1">{{ t('buyer.historyEmptyDesc') }}</p>
      </div>
    </div>

    <!-- Orders list -->
    <div v-else class="space-y-3">
      <div v-for="order in filteredOrders" :key="order.id"
        @click="navigateTo(`/buyer/orders/${order.id}`)"
        class="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md hover:border-[#10b481]/20 transition-all cursor-pointer group">

        <div class="flex flex-col sm:flex-row sm:items-center gap-4">
          <div class="flex items-center gap-4 flex-1 min-w-0">
            <div class="w-11 h-11 bg-gray-50 rounded-xl flex items-center justify-center text-[#112830] group-hover:bg-emerald-50 group-hover:text-[#10b481] transition-colors flex-shrink-0">
              <i class="bx bx-package text-xl"></i>
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

          <div class="flex items-center justify-between sm:justify-end gap-4 border-t sm:border-t-0 pt-3 sm:pt-0">
            <div class="text-right">
              <p class="text-[9px] font-black text-gray-400 uppercase tracking-widest mb-0.5">Total</p>
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

definePageMeta({ layout: 'dashboard' });
const { t } = useI18n();

const { loading, fetchOrders } = useMarketplace();
const { apiFetch } = useApi();

const allOrders   = ref<any[]>([]);
const filterStatus = ref('ALL');
const search       = ref('');

const statusFilters = computed(() => [
  { value: 'ALL',       label: t('buyer.filterAll')       },
  { value: 'DELIVERED', label: t('buyer.filterDelivered') },
  { value: 'CANCELLED', label: t('buyer.filterCancelled') },
]);

onMounted(async () => {
  try {
    const data = await apiFetch('/api/orders/orders/');
    const all  = data.results || data || [];
    allOrders.value = all.filter((o: any) => o.status === 'DELIVERED' || o.status === 'CANCELLED');
  } catch (err) {
    console.error('Erreur historique', err);
  }
});

function countByStatus(value: string) {
  if (value === 'ALL') return allOrders.value.length;
  return allOrders.value.filter(o => o.status === value).length;
}

const filteredOrders = computed(() => {
  let list = allOrders.value;
  if (filterStatus.value !== 'ALL') list = list.filter(o => o.status === filterStatus.value);
  if (search.value) {
    const q = search.value.toLowerCase();
    list = list.filter(o => o.order_number?.toLowerCase().includes(q));
  }
  return list;
});

function formatDate(d: string) {
  return new Date(d).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' });
}

function getStatusLabel(status: string) {
  const map: Record<string, string> = {
    DELIVERED: 'Livrée', CANCELLED: 'Annulée', PAID: 'Payée', SHIPPED: 'Expédiée',
  };
  return map[status] || status;
}

function getStatusClass(status: string) {
  switch (status) {
    case 'DELIVERED': return 'bg-emerald-100 text-emerald-600';
    case 'CANCELLED': return 'bg-rose-100 text-rose-600';
    case 'PAID':      return 'bg-emerald-50 text-[#10b481]';
    case 'SHIPPED':   return 'bg-blue-100 text-blue-600';
    default:          return 'bg-gray-100 text-gray-600';
  }
}
</script>