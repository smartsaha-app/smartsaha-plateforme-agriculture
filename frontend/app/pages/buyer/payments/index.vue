<template>
  <div class="space-y-8">
    <!-- Header -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <h1 class="text-3xl font-black text-[#112830]">Paiements</h1>
        <p class="text-gray-500 font-medium">Gérez vos paiements, factures et historique financier.</p>
      </div>
    </div>

    <!-- Tabs -->
    <div class="flex gap-4 border-b border-gray-100 pb-px">
      <button 
        v-for="tab in tabs" :key="tab.id"
        @click="activeTab = tab.id"
        :class="[activeTab === tab.id ? 'text-[#10b481] border-[#10b481]' : 'text-gray-400 border-transparent hover:text-gray-600']"
        class="pb-4 px-2 border-b-2 font-black text-xs uppercase tracking-widest transition-all"
      >
        {{ tab.label }}
        <span v-if="tab.count > 0" class="ml-2 px-2 py-0.5 bg-gray-100 text-gray-500 rounded-full text-[9px]">{{ tab.count }}</span>
      </button>
    </div>

    <!-- Content -->
    <div v-if="loading" class="grid grid-cols-1 gap-4">
      <div v-for="i in 3" :key="i" class="h-32 bg-white rounded-[2.5rem] border border-gray-100 animate-pulse"></div>
    </div>

    <div v-else class="space-y-6">
      <!-- Tab: Pending Payments -->
      <div v-if="activeTab === 'pending'" class="space-y-4">
        <div v-if="pendingOrders.length === 0" class="bg-white py-20 rounded-[3rem] border border-gray-100 text-center space-y-4">
          <div class="w-20 h-20 bg-gray-50 rounded-full flex items-center justify-center mx-auto text-gray-300">
            <i class="bx bx-check-shield text-4xl"></i>
          </div>
          <p class="text-gray-400 font-bold">Aucun paiement en attente. Tout est à jour !</p>
        </div>
        
        <div 
          v-for="order in pendingOrders" :key="order.id"
          class="bg-white p-6 rounded-[2.5rem] border border-gray-100 shadow-sm flex flex-col md:flex-row items-center gap-6 hover:border-[#10b481]/30 transition-all"
        >
          <div class="w-14 h-14 bg-amber-50 text-amber-500 rounded-2xl flex items-center justify-center text-2xl flex-shrink-0">
            <i class="bx bx-time-five"></i>
          </div>
          <div class="flex-1 text-center md:text-left">
            <h3 class="font-black text-[#112830] text-lg">{{ order.order_number }}</h3>
            <p class="text-xs font-bold text-gray-400">Commande du {{ formatDate(order.created_at) }}</p>
          </div>
          <div class="text-center md:text-right">
            <p class="text-xl font-black text-[#112830]">{{ order.total }} Ar</p>
            <p class="text-[10px] font-black text-amber-500 uppercase tracking-widest">En attente de règlement</p>
          </div>
          <button 
            @click="navigateTo(`/buyer/payments/checkout/${order.id}`)"
            class="w-full md:w-auto px-8 py-3 bg-[#112830] text-white rounded-2xl font-black text-[10px] uppercase tracking-widest hover:bg-[#10b481] transition-all"
          >
            Payer maintenant
          </button>
        </div>
      </div>

      <!-- Tab: Transaction History -->
      <div v-if="activeTab === 'history'" class="bg-white rounded-[3rem] border border-gray-100 shadow-sm overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="bg-gray-50/50">
                <th class="px-8 py-6 text-[10px] font-black text-gray-400 uppercase tracking-widest">ID Transaction</th>
                <th class="px-8 py-6 text-[10px] font-black text-gray-400 uppercase tracking-widest">Date</th>
                <th class="px-8 py-6 text-[10px] font-black text-gray-400 uppercase tracking-widest">Méthode</th>
                <th class="px-8 py-6 text-[10px] font-black text-gray-400 uppercase tracking-widest">Montant</th>
                <th class="px-8 py-6 text-[10px] font-black text-gray-400 uppercase tracking-widest">Statut</th>
                <th class="px-8 py-6 text-[10px] font-black text-gray-400 uppercase tracking-widest text-right">Action</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-50">
              <tr v-for="txn in transactions" :key="txn.id" class="hover:bg-gray-50/30 transition-colors">
                <td class="px-8 py-6">
                  <p class="font-black text-[#112830] text-sm truncate w-32">{{ txn.id }}</p>
                  <p class="text-[10px] font-bold text-gray-400">Order #{{ txn.order }}</p>
                </td>
                <td class="px-8 py-6">
                  <p class="text-sm font-bold text-gray-600">{{ formatDate(txn.created_at) }}</p>
                </td>
                <td class="px-8 py-6">
                  <div class="flex items-center gap-2">
                    <div class="w-8 h-8 bg-gray-100 rounded-lg flex items-center justify-center text-gray-500">
                      <i :class="getPaymentIcon(txn.method)"></i>
                    </div>
                    <span class="text-xs font-black text-[#112830]">{{ txn.method }}</span>
                  </div>
                </td>
                <td class="px-8 py-6">
                  <p class="text-sm font-black text-[#112830]">{{ txn.amount }} {{ txn.currency }}</p>
                </td>
                <td class="px-8 py-6">
                  <span :class="getTxnStatusClass(txn.status)" class="px-3 py-1 rounded-full text-[9px] font-black uppercase tracking-wider">
                    {{ txn.status }}
                  </span>
                </td>
                <td class="px-8 py-6 text-right">
                  <button class="p-2 hover:bg-gray-100 rounded-xl transition-colors text-gray-400 hover:text-[#112830]">
                    <i class="bx bx-download text-xl"></i>
                  </button>
                </td>
              </tr>
              <tr v-if="transactions.length === 0">
                <td colspan="6" class="px-8 py-12 text-center text-gray-400 font-medium italic">
                  Aucune transaction enregistrée.
                </td>
              </tr>
            </tbody>
          </table>
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

const { orders, transactions, loading, fetchOrders, fetchTransactions } = useMarketplace();
const activeTab = ref('pending');

const tabs = computed(() => [
  { id: 'pending', label: 'À régler', count: pendingOrders.value.length },
  { id: 'history', label: 'Historique', count: transactions.value.length },
  { id: 'refunds', label: 'Remboursements', count: 0 }
]);

const pendingOrders = computed(() => {
  return (orders.value || []).filter((o: any) => o.status === 'PENDING');
});

const totalPaid = computed(() => {
  return (transactions.value || [])
    .filter((t: any) => t.status === 'SUCCESS')
    .reduce((sum: number, t: any) => sum + parseFloat(t.amount), 0)
    .toLocaleString();
});

onMounted(() => {
  fetchOrders();
  fetchTransactions();
});

const formatDate = (dateStr: string) => {
  if (!dateStr) return '';
  return new Date(dateStr).toLocaleDateString('fr-FR', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  });
};

const getPaymentIcon = (method: string) => {
  switch (method) {
    case 'STRIPE': return 'bx bxl-stripe';
    case 'MVOLA':
    case 'ORANGE_MONEY':
    case 'AIRTEL_MONEY': return 'bx bx-mobile';
    default: return 'bx bx-credit-card';
  }
};

const getTxnStatusClass = (status: string) => {
  switch (status) {
    case 'SUCCESS': return 'bg-emerald-100 text-emerald-600';
    case 'PENDING':
    case 'PROCESSING': return 'bg-amber-100 text-amber-600';
    case 'FAILED': return 'bg-rose-100 text-rose-600';
    default: return 'bg-gray-100 text-gray-600';
  }
};
</script>
