<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8 space-y-6">

    <!-- ===== HEADER ===== -->
    <PageHeader :title="t('buyer.paymentsTitle')">
      <template #subtitle>
        <i class="bx bx-credit-card"></i>
        {{ t('buyer.paymentsDesc') }}
      </template>
      <template #breadcrumb>
        <NuxtLink to="/buyer/dashboard" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
          <span>Accueil</span>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">{{ t('buyer.paymentsTitle') }}</span>
      </template>
    </PageHeader>

    <!-- ===== STATS ===== -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <div class="bg-[#112830] p-5 rounded-2xl shadow-lg relative overflow-hidden">
        <div class="absolute inset-0 opacity-5 pointer-events-none">
          <div class="absolute -bottom-6 -right-6 w-24 h-24 border-4 border-white rounded-full"></div>
        </div>
        <div class="relative z-10">
          <div class="w-9 h-9 bg-[#10b481] rounded-xl flex items-center justify-center mb-3">
            <i class="bx bx-wallet text-white text-base"></i>
          </div>
          <p class="text-[9px] font-black text-white/50 uppercase tracking-widest mb-0.5">{{ t('buyer.totalPaid') }}</p>
          <p class="text-xl font-black text-white">{{ formatAmount(totalPaid) }}</p>
        </div>
      </div>
      <div class="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm">
        <div class="w-9 h-9 bg-amber-50 text-amber-500 rounded-xl flex items-center justify-center mb-3">
          <i class="bx bx-time-five text-base"></i>
        </div>
        <p class="text-[9px] font-black text-gray-400 uppercase tracking-widest mb-0.5">{{ t('buyer.pendingCount') }}</p>
        <p class="text-xl font-black text-[#112830]">{{ pendingOrders.length }}</p>
        <p class="text-xs text-gray-400 mt-0.5">commande{{ pendingOrders.length !== 1 ? 's' : '' }} à régler</p>
      </div>
      <div class="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm">
        <div class="w-9 h-9 bg-blue-50 text-blue-500 rounded-xl flex items-center justify-center mb-3">
          <i class="bx bx-transfer text-base"></i>
        </div>
        <p class="text-[9px] font-black text-gray-400 uppercase tracking-widest mb-0.5">{{ t('buyer.transactionsCount') }}</p>
        <p class="text-xl font-black text-[#112830]">{{ transactions.length }}</p>
        <p class="text-xs text-gray-400 mt-0.5">{{ t('buyer.transactionsRecorded') }}</p>
      </div>
    </div>

    <!-- ===== TABS ===== -->
    <div class="flex gap-1 bg-gray-100 p-1.5 rounded-2xl w-fit">
      <button v-for="tab in tabs" :key="tab.id" @click="activeTab = tab.id"
        :class="[
          'px-5 py-2 rounded-xl text-xs font-bold transition-all',
          activeTab === tab.id ? 'bg-white text-[#112830] shadow-sm' : 'text-gray-400 hover:text-gray-600'
        ]">
        {{ tab.label }}
        <span v-if="tab.count > 0"
          class="ml-1.5 px-1.5 py-0.5 rounded-full text-[8px] font-black"
          :class="activeTab === tab.id ? 'bg-[#112830] text-white' : 'bg-gray-200 text-gray-500'">
          {{ tab.count }}
        </span>
      </button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="space-y-3">
      <div v-for="i in 3" :key="i" class="h-24 bg-white rounded-2xl border border-gray-100 animate-pulse"></div>
    </div>

    <template v-else>

      <!-- ===== TAB: À RÉGLER ===== -->
      <div v-if="activeTab === 'pending'" class="space-y-3">
        <div v-if="pendingOrders.length === 0" class="bg-white py-16 rounded-2xl border border-gray-100 text-center space-y-4 shadow-sm">
          <div class="w-16 h-16 bg-emerald-50 rounded-2xl flex items-center justify-center mx-auto">
            <i class="bx bx-check-shield text-3xl text-[#10b481]"></i>
          </div>
          <p class="text-sm font-bold text-gray-400">{{ t('buyer.noPending') }}</p>
        </div>

        <div v-for="order in pendingOrders" :key="order.id"
          class="bg-white p-5 rounded-2xl border border-amber-100 shadow-sm flex flex-col sm:flex-row items-start sm:items-center gap-4 hover:shadow-md transition-all">
          <div class="w-11 h-11 bg-amber-50 text-amber-500 rounded-xl flex items-center justify-center flex-shrink-0">
            <i class="bx bx-time-five text-xl"></i>
          </div>
          <div class="flex-1 min-w-0">
            <h3 class="text-sm font-black text-[#112830]">{{ order.order_number }}</h3>
            <p class="text-xs font-medium text-gray-400">{{ t('buyer.orderedOn') }} {{ formatDate(order.created_at) }}</p>
          </div>
          <div class="flex items-center gap-4 w-full sm:w-auto justify-between sm:justify-end">
            <div class="text-right">
              <p class="text-base font-black text-[#112830]">{{ order.total }} Ar</p>
              <p class="text-[9px] font-black text-amber-500 uppercase tracking-widest">{{ t('buyer.toSettle') }}</p>
            </div>
            <NuxtLink :to="`/buyer/payments/checkout/${order.id}`"
              class="px-5 py-2.5 bg-[#112830] text-white rounded-xl font-bold text-xs uppercase tracking-widest hover:bg-[#10b481] transition-all shadow-sm flex-shrink-0">
              Payer
            </NuxtLink>
          </div>
        </div>
      </div>

      <!-- ===== TAB: HISTORIQUE ===== -->
      <div v-if="activeTab === 'history'" class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
        <div v-if="transactions.length === 0" class="py-16 text-center space-y-3">
          <div class="w-16 h-16 bg-gray-50 rounded-2xl flex items-center justify-center mx-auto">
            <i class="bx bx-transfer text-3xl text-gray-200"></i>
          </div>
          <p class="text-sm text-gray-400 font-medium">{{ t('buyer.noTransactions') }}</p>
        </div>
        <div v-else class="overflow-x-auto">
          <table class="w-full text-left">
            <thead>
              <tr class="bg-gray-50/70 border-b border-gray-100">
                <th class="px-5 py-4 text-[9px] font-black text-gray-400 uppercase tracking-widest">{{ t('buyer.colTransaction') }}</th>
                <th class="px-5 py-4 text-[9px] font-black text-gray-400 uppercase tracking-widest">{{ t('buyer.colDate') }}</th>
                <th class="px-5 py-4 text-[9px] font-black text-gray-400 uppercase tracking-widest">{{ t('buyer.colMethod') }}</th>
                <th class="px-5 py-4 text-[9px] font-black text-gray-400 uppercase tracking-widest">{{ t('buyer.colAmount') }}</th>
                <th class="px-5 py-4 text-[9px] font-black text-gray-400 uppercase tracking-widest">{{ t('dashboard.status') }}</th>
                <th class="px-5 py-4"></th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-50">
              <tr v-for="txn in transactions" :key="txn.id" class="hover:bg-gray-50/50 transition-colors">
                <td class="px-5 py-4">
                  <p class="text-xs font-black text-[#112830] truncate w-28">{{ txn.id }}</p>
                  <p class="text-[9px] text-gray-400 font-bold">Cmd #{{ txn.order }}</p>
                </td>
                <td class="px-5 py-4">
                  <p class="text-xs font-medium text-gray-600">{{ formatDate(txn.created_at) }}</p>
                </td>
                <td class="px-5 py-4">
                  <div class="flex items-center gap-2">
                    <div class="w-7 h-7 bg-gray-100 rounded-lg flex items-center justify-center text-gray-500">
                      <i :class="getPaymentIcon(txn.method)" class="text-sm"></i>
                    </div>
                    <span class="text-xs font-bold text-[#112830]">{{ txn.method }}</span>
                  </div>
                </td>
                <td class="px-5 py-4">
                  <p class="text-sm font-black text-[#112830]">{{ txn.amount }} {{ txn.currency }}</p>
                </td>
                <td class="px-5 py-4">
                  <span :class="getTxnStatusClass(txn.status)"
                    class="px-2.5 py-1 rounded-lg text-[9px] font-black uppercase tracking-widest">
                    {{ getTxnStatusLabel(txn.status) }}
                  </span>
                </td>
                <td class="px-5 py-4 text-right">
                  <button class="w-8 h-8 rounded-lg hover:bg-gray-100 text-gray-300 hover:text-[#112830] transition-all flex items-center justify-center ml-auto">
                    <i class="bx bx-download text-base"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- ===== TAB: REMBOURSEMENTS ===== -->
      <div v-if="activeTab === 'refunds'" class="bg-white py-16 rounded-2xl border border-gray-100 text-center space-y-4 shadow-sm">
        <div class="w-16 h-16 bg-gray-50 rounded-2xl flex items-center justify-center mx-auto">
          <i class="bx bx-refresh text-3xl text-gray-200"></i>
        </div>
        <div>
          <h3 class="text-sm font-black text-[#112830]">{{ t('buyer.noRefunds') }}</h3>
          <p class="text-xs text-gray-400 mt-1">{{ t('buyer.noRefundsDesc') }}</p>
        </div>
      </div>

    </template>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useMarketplace } from '~/composables/useMarketplace';

const { t } = useI18n();
definePageMeta({ layout: 'dashboard' });

const { orders, transactions, loading, fetchOrders, fetchTransactions } = useMarketplace();
const activeTab = ref('pending');

onMounted(() => {
  fetchOrders();
  fetchTransactions();
});

const tabs = computed(() => [
  { id: 'pending',  label: t('buyer.tabPending'),  count: pendingOrders.value.length  },
  { id: 'history',  label: t('buyer.tabHistory'), count: transactions.value.length   },
  { id: 'refunds',  label: t('buyer.tabRefunds'), count: 0                           },
]);

const pendingOrders = computed(() =>
  (orders.value || []).filter((o: any) => o.status === 'PENDING')
);

const totalPaid = computed(() =>
  (transactions.value || [])
    .filter((t: any) => t.status === 'SUCCESS')
    .reduce((sum: number, t: any) => sum + parseFloat(t.amount || 0), 0)
);

function formatAmount(val: number) {
  return new Intl.NumberFormat('fr-MG').format(val) + ' Ar';
}

function formatDate(d: string) {
  if (!d) return '';
  return new Date(d).toLocaleDateString('fr-FR', { day: 'numeric', month: 'short', year: 'numeric' });
}

function getPaymentIcon(method: string) {
  if (method === 'STRIPE')       return 'bx bxl-stripe';
  if (['MVOLA', 'ORANGE_MONEY', 'AIRTEL_MONEY'].includes(method)) return 'bx bx-mobile';
  return 'bx bx-credit-card';
}

function getTxnStatusLabel(status: string) {
  const map: Record<string, string> = { SUCCESS: t('buyer.txnSuccess'), PENDING: t('buyer.statusPending'), PROCESSING: t('buyer.txnProcessing'), FAILED: t('buyer.txnFailed') };
  return map[status] || status;
}

function getTxnStatusClass(status: string) {
  switch (status) {
    case 'SUCCESS':    return 'bg-emerald-50 text-emerald-600';
    case 'PENDING':
    case 'PROCESSING': return 'bg-amber-50 text-amber-600';
    case 'FAILED':     return 'bg-rose-50 text-rose-600';
    default:           return 'bg-gray-50 text-gray-500';
  }
}
</script>