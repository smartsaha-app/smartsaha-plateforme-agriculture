<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8 space-y-6">

    <!-- ===== HEADER ===== -->
    <PageHeader :title="t('seller.historyTitle')">
      <template #subtitle>
        <i class="bx bx-history"></i>
        {{ t('seller.historyDesc') }}
      </template>
      <template #breadcrumb>
        <NuxtLink to="/seller/dashboard" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
          <span>{{ t('dashboard.home') }}</span>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">{{ t('seller.historyTitle') }}</span>
      </template>
    </PageHeader>

    <!-- ===== FILTERS ===== -->
    <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-3 flex items-center gap-2 overflow-x-auto">
      <div class="flex gap-1.5 flex-shrink-0">
        <button v-for="f in statusFilters" :key="f.value"
          @click="filterStatus = f.value"
          :class="[
            'px-4 py-2 rounded-xl text-xs font-bold transition-all',
            filterStatus === f.value ? 'bg-[#112830] text-white' : 'bg-gray-50 text-gray-400 hover:bg-gray-100'
          ]">
          {{ f.label }}
          <span v-if="countByFilter(f.value) > 0"
            class="ml-1.5 px-1.5 py-0.5 rounded-full text-[8px] font-black"
            :class="filterStatus === f.value ? 'bg-white/20 text-white' : 'bg-gray-200 text-gray-500'">
            {{ countByFilter(f.value) }}
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

    <!-- ===== LOADING ===== -->
    <div v-if="loading" class="space-y-3">
      <div v-for="i in 5" :key="i" class="h-20 bg-white rounded-2xl border border-gray-100 animate-pulse"></div>
    </div>

    <!-- ===== EMPTY ===== -->
    <div v-else-if="filteredOrders.length === 0" class="bg-white py-20 rounded-2xl border border-gray-100 text-center space-y-4 shadow-sm">
      <div class="w-20 h-20 bg-gray-50 rounded-2xl flex items-center justify-center mx-auto">
        <i class="bx bx-history text-4xl text-gray-200"></i>
      </div>
      <div>
        <h3 class="text-base font-black text-[#112830]">{{ t('seller.noHistory') }}</h3>
        <p class="text-sm text-gray-400">{{ t('seller.noHistoryDesc') }}</p>
      </div>
    </div>

    <!-- ===== TABLE ===== -->
    <div v-else class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
      <table class="w-full text-left">
        <thead>
          <tr class="bg-gray-50/70 border-b border-gray-100">
            <th class="px-5 py-4 text-[9px] font-black text-gray-400 uppercase tracking-widest">{{ t('seller.colOrderNum') }}</th>
            <th class="px-5 py-4 text-[9px] font-black text-gray-400 uppercase tracking-widest">{{ t('seller.colBuyer') }}</th>
            <th class="px-5 py-4 text-[9px] font-black text-gray-400 uppercase tracking-widest hidden md:table-cell">{{ t('seller.colItems') }}</th>
            <th class="px-5 py-4 text-[9px] font-black text-gray-400 uppercase tracking-widest">{{ t('seller.colTotal') }}</th>
            <th class="px-5 py-4 text-[9px] font-black text-gray-400 uppercase tracking-widest">{{ t('dashboard.status') }}</th>
            <th class="px-5 py-4"></th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-50">
          <tr v-for="order in filteredOrders" :key="order.id"
            class="hover:bg-gray-50/50 transition-colors group">

            <td class="px-5 py-4">
              <p class="text-sm font-black text-[#112830]">{{ order.order_number }}</p>
              <p class="text-[9px] text-gray-400 font-bold">
                {{ new Date(order.created_at).toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' }) }}
              </p>
            </td>

            <td class="px-5 py-4">
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 bg-gray-100 rounded-lg flex items-center justify-center text-gray-400 flex-shrink-0">
                  <i class="bx bx-user text-base"></i>
                </div>
                <div class="min-w-0">
                  <p class="text-sm font-black text-[#112830] truncate">
                    {{ order.buyer_details?.username || order.buyer_name || 'Client' }}
                  </p>
                  <p class="text-[9px] text-gray-400 font-bold truncate">{{ order.buyer_details?.email }}</p>
                </div>
              </div>
            </td>

            <td class="px-5 py-4 hidden md:table-cell">
              <div class="flex -space-x-2">
                <div v-for="item in order.items?.slice(0, 3)" :key="item.id"
                  class="w-8 h-8 rounded-lg ring-2 ring-white bg-gray-50 border border-gray-100 overflow-hidden">
                  <img v-if="item.product_image" :src="item.product_image" class="w-full h-full object-cover" />
                  <div v-else class="w-full h-full flex items-center justify-center text-gray-300">
                    <i class="bx bx-image text-xs"></i>
                  </div>
                </div>
                <div v-if="order.items?.length > 3"
                  class="w-8 h-8 rounded-lg ring-2 ring-white bg-gray-100 flex items-center justify-center text-[9px] font-black text-gray-400">
                  +{{ order.items.length - 3 }}
                </div>
              </div>
            </td>

            <td class="px-5 py-4">
              <p class="text-sm font-black text-[#10b481]">{{ order.total }} Ar</p>
            </td>

            <td class="px-5 py-4">
              <span class="px-2.5 py-1 rounded-lg text-[9px] font-black uppercase tracking-widest border"
                :class="getStatusClass(order.status)">
                {{ getStatusLabel(order.status) }}
              </span>
            </td>

            <td class="px-5 py-4 text-right">
              <NuxtLink :to="`/seller/orders/${order.id}`"
                class="w-8 h-8 rounded-lg hover:bg-gray-100 text-gray-300 hover:text-[#112830] transition-all flex items-center justify-center ml-auto">
                <i class="bx bx-show text-lg"></i>
              </NuxtLink>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';


definePageMeta({ layout: 'dashboard' });
const { t } = useI18n();

const { apiFetch } = useApi();

const orders  = ref<any[]>([]);
const loading = ref(true);
const filterStatus = ref('ALL');
const search  = ref('');

const statusFilters = computed(() => [
  { value: 'ALL',       label: t('seller.filterAll')       },
  { value: 'DELIVERED', label: t('seller.filterDelivered') },
  { value: 'CANCELLED', label: t('seller.filterCancelled') },
]);

onMounted(async () => {
  try {
    const data = await apiFetch('/api/orders/orders/?as_seller=true');
    const all  = data.results || data || [];
    orders.value = all.filter((o: any) => o.status === 'DELIVERED' || o.status === 'CANCELLED');
  } catch (err) {
    console.error('Erreur chargement historique', err);
  } finally {
    loading.value = false;
  }
});

function countByFilter(value: string) {
  if (value === 'ALL') return orders.value.length;
  return orders.value.filter(o => o.status === value).length;
}

const filteredOrders = computed(() => {
  let list = orders.value;
  if (filterStatus.value !== 'ALL') {
    list = list.filter(o => o.status === filterStatus.value);
  }
  if (search.value) {
    const q = search.value.toLowerCase();
    list = list.filter(o =>
      o.order_number?.toLowerCase().includes(q) ||
      (o.buyer_name || o.buyer_details?.username || '').toLowerCase().includes(q)
    );
  }
  return list;
});

const getStatusLabel = (status: string) => {
  const map: Record<string, string> = {
    DELIVERED: t('seller.statusDelivered'),
    CANCELLED: t('seller.statusCancelled'),
    PAID:      t('seller.statusPaid'),
    SHIPPED:   t('seller.statusShipped'),
  };
  return map[status] || status;
};

const getStatusClass = (status: string) => {
  switch (status) {
    case 'DELIVERED': return 'bg-emerald-50 text-emerald-600 border-emerald-100';
    case 'CANCELLED': return 'bg-rose-50 text-rose-500 border-rose-100';
    case 'PAID':      return 'bg-blue-50 text-blue-600 border-blue-100';
    case 'SHIPPED':   return 'bg-indigo-50 text-indigo-600 border-indigo-100';
    default:          return 'bg-gray-50 text-gray-500 border-gray-100';
  }
};
</script>