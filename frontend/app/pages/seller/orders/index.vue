<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8 space-y-6">

    <!-- ===== HEADER ===== -->
    <PageHeader :title="t('seller.ordersTitle')">
      <template #subtitle>
        <i class="bx bx-shopping-bag"></i>
        {{ t('seller.ordersDesc') }}
      </template>
      <template #breadcrumb>
        <NuxtLink to="/seller/dashboard" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
          <span>{{ t('dashboard.home') }}</span>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">{{ t('seller.ordersTitle') }}</span>
      </template>
    </PageHeader>

    <!-- ===== TABS ===== -->
    <div class="flex gap-1.5 bg-gray-100 p-1.5 rounded-2xl w-fit">
      <button v-for="status in statusFilters" :key="status.id"
        @click="activeStatus = status.id"
        :class="[
          'px-5 py-2 rounded-xl text-xs font-bold transition-all',
          activeStatus === status.id ? 'bg-white text-[#112830] shadow-sm' : 'text-gray-400 hover:text-gray-600'
        ]">
        {{ status.label }}
        <span v-if="countByStatus(status.id) > 0"
          class="ml-1.5 px-1.5 py-0.5 rounded-full text-[9px] font-black"
          :class="activeStatus === status.id ? 'bg-[#112830] text-white' : 'bg-gray-200 text-gray-500'">
          {{ countByStatus(status.id) }}
        </span>
      </button>
    </div>

    <!-- ===== LOADING ===== -->
    <div v-if="loading" class="space-y-3">
      <div v-for="i in 5" :key="i" class="h-20 bg-white rounded-2xl border border-gray-100 animate-pulse"></div>
    </div>

    <!-- ===== EMPTY ===== -->
    <div v-else-if="filteredOrders.length === 0" class="bg-white py-20 rounded-2xl border border-gray-100 text-center space-y-4 shadow-sm">
      <div class="w-20 h-20 bg-gray-50 rounded-2xl flex items-center justify-center mx-auto">
        <i class="bx bx-shopping-bag text-4xl text-gray-200"></i>
      </div>
      <div>
        <h3 class="text-base font-black text-[#112830]">{{ t('seller.noOrdersStatus') }}</h3>
        <p class="text-sm text-gray-400">{{ t('seller.noOrdersStatusDesc') }}</p>
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
            class="hover:bg-gray-50/50 transition-colors cursor-pointer group"
            @click="navigateTo(`/seller/orders/${order.id}`)">

            <td class="px-5 py-4">
              <p class="text-sm font-black text-[#112830]">{{ order.order_number }}</p>
              <p class="text-[9px] text-gray-400 font-bold">{{ new Date(order.created_at).toLocaleDateString('fr-FR') }}</p>
            </td>

            <td class="px-5 py-4">
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 bg-gray-100 rounded-lg flex items-center justify-center text-gray-400 flex-shrink-0">
                  <i class="bx bx-user text-base"></i>
                </div>
                <div>
                  <p class="text-sm font-black text-[#112830]">{{ order.buyer_name || order.buyer_details?.username || 'Client' }}</p>
                  <p class="text-[9px] text-gray-400">{{ order.buyer_details?.email || order.buyer_email }}</p>
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

            <td class="px-5 py-4" @click.stop>
              <div class="relative group/status">
                <button class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-[9px] font-black uppercase tracking-widest border hover:border-[#10b481] transition-all"
                  :class="getStatusClass(order.status)">
                  {{ getStatusLabel(order.status) }}
                  <i class="bx bx-chevron-down text-xs"></i>
                </button>
                <div class="absolute top-full left-0 mt-1 w-44 bg-white border border-gray-100 rounded-xl shadow-xl hidden group-hover/status:block z-20 overflow-hidden p-1">
                  <button v-for="s in nextStatuses" :key="s.value"
                    @click="handleUpdateStatus(order, s.value)"
                    class="w-full text-left px-3 py-2 text-[9px] font-black uppercase tracking-widest hover:bg-gray-50 rounded-lg transition-colors">
                    {{ s.label }}
                  </button>
                </div>
              </div>
            </td>

            <td class="px-5 py-4 text-right">
              <NuxtLink :to="`/seller/orders/${order.id}`" @click.stop
                class="w-8 h-8 rounded-lg hover:bg-gray-100 text-gray-300 hover:text-[#112830] transition-all flex items-center justify-center ml-auto">
                <i class="bx bx-show text-lg"></i>
              </NuxtLink>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Toast notification -->
    <transition name="slide-up">
      <div v-if="toast.visible"
        class="fixed bottom-6 left-1/2 -translate-x-1/2 z-[100] px-5 py-3 rounded-2xl shadow-xl flex items-center gap-3 text-sm font-bold"
        :class="toast.type === 'success' ? 'bg-[#112830] text-white' : 'bg-rose-500 text-white'">
        <i :class="toast.type === 'success' ? 'bx bx-check-circle' : 'bx bx-error-circle'" class="text-lg"></i>
        {{ toast.message }}
      </div>
    </transition>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useMarketplace } from '~/composables/useMarketplace';

definePageMeta({ layout: 'dashboard' });
const { t } = useI18n();

const { orders, loading, fetchOrders, updateOrderStatus } = useMarketplace();
const activeStatus = ref('ALL');

const toast = ref({ visible: false, message: '', type: 'success' as 'success' | 'error' });

function showToast(message: string, type: 'success' | 'error' = 'success') {
  toast.value = { visible: true, message, type };
  setTimeout(() => (toast.value.visible = false), 3000);
}

const statusFilters = computed(() => [
  { id: 'ALL',       label: t('seller.tabAll')       },
  { id: 'PENDING',   label: t('seller.tabPending')   },
  { id: 'PAID',      label: t('seller.tabPaid')      },
  { id: 'CONFIRMED', label: t('seller.tabConfirmed') },
  { id: 'SHIPPED',   label: t('seller.tabShipped')   },
  { id: 'DELIVERED', label: t('seller.tabDelivered') },
]);

const nextStatuses = computed(() => [
  { value: 'CONFIRMED', label: t('seller.actionConfirm') },
  { value: 'SHIPPED',   label: t('seller.actionShip')    },
  { value: 'DELIVERED', label: t('seller.actionDeliver') },
  { value: 'CANCELLED', label: t('seller.actionCancel')  },
]);

onMounted(() => fetchOrders({ as_seller: 'true' }));

function countByStatus(id: string) {
  const all = orders.value || [];
  if (id === 'ALL') return all.filter(o => o.status !== 'DELIVERED' && o.status !== 'CANCELLED').length;
  return all.filter(o => o.status === id).length;
}

const filteredOrders = computed(() => {
  const all = orders.value || [];
  if (activeStatus.value === 'ALL') return all.filter(o => o.status !== 'DELIVERED' && o.status !== 'CANCELLED');
  return all.filter(o => o.status === activeStatus.value);
});

const getStatusLabel = (status: string) => {
  const map: Record<string, string> = {
    PENDING:   t('seller.statusPending'),
    PAID:      t('seller.statusPaid'),
    CONFIRMED: t('seller.statusConfirmed'),
    SHIPPED:   t('seller.statusShipped'),
    DELIVERED: t('seller.statusDelivered'),
    CANCELLED: t('seller.statusCancelled'),
  };
  return map[status] || status;
};

const getStatusClass = (status: string) => {
  switch (status) {
    case 'PENDING':   return 'bg-amber-50 text-amber-600 border-amber-100';
    case 'PAID':      return 'bg-emerald-50 text-emerald-600 border-emerald-100';
    case 'CONFIRMED': return 'bg-blue-50 text-blue-600 border-blue-100';
    case 'SHIPPED':   return 'bg-indigo-50 text-indigo-600 border-indigo-100';
    case 'DELIVERED': return 'bg-emerald-100 text-emerald-700 border-emerald-200';
    case 'CANCELLED': return 'bg-rose-50 text-rose-600 border-rose-100';
    default:          return 'bg-gray-50 text-gray-500 border-gray-100';
  }
};

async function handleUpdateStatus(order: any, newStatus: string) {
  try {
    await updateOrderStatus(order.id, newStatus);
    order.status = newStatus;
    showToast(`${getStatusLabel(newStatus)}`);
  } catch {
    showToast(t('seller.updateStatusError'), 'error');
  }
}
</script>

<style scoped>
.slide-up-enter-active, .slide-up-leave-active { transition: all 0.3s ease; }
.slide-up-enter-from, .slide-up-leave-to { opacity: 0; transform: translate(-50%, 1rem); }
</style>