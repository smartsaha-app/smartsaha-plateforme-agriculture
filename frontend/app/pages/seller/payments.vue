<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8 space-y-6">

    <!-- ===== HEADER ===== -->
    <PageHeader :title="t('seller.revenuesTitle')">
      <template #subtitle>
        <i class="bx bx-wallet"></i>
        {{ t('seller.revenuesDesc') }}
      </template>
      <template #breadcrumb>
        <NuxtLink to="/seller/dashboard" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
          <span>{{ t('dashboard.home') }}</span>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">{{ t('seller.revenuesTitle') }}</span>
      </template>
    </PageHeader>

    <!-- ===== STATS ===== -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-5">

      <!-- Solde disponible -->
      <div class="bg-[#112830] p-6 rounded-2xl shadow-lg relative overflow-hidden">
        <div class="absolute inset-0 opacity-5 pointer-events-none">
          <div class="absolute -bottom-8 -right-8 w-32 h-32 border-4 border-white rounded-full"></div>
          <div class="absolute top-4 -left-4 w-20 h-20 border-2 border-white rounded-full"></div>
        </div>
        <div class="relative z-10">
          <div class="flex items-center justify-between mb-4">
            <div class="w-10 h-10 bg-[#10b481] rounded-xl flex items-center justify-center">
              <i class="bx bx-trending-up text-white text-lg"></i>
            </div>
            <span class="text-[9px] font-black text-white/40 uppercase tracking-widest">{{ t('seller.availableBalance') }}</span>
          </div>
          <p class="text-[9px] font-black text-white/50 uppercase tracking-widest mb-1">{{ t('seller.availableBalance') }}</p>
          <p class="text-2xl font-black text-white">{{ formatAmount(sellerStats.available_balance) }}</p>
          <button @click="openWithdrawModal"
            class="mt-4 w-full py-2.5 bg-[#10b481] text-white rounded-xl font-bold text-xs uppercase tracking-widest hover:bg-emerald-400 transition-all">
            {{ t('seller.withdraw') }}
          </button>
        </div>
      </div>

      <!-- Ventes totales -->
      <div class="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm space-y-4">
        <div class="w-10 h-10 bg-blue-50 text-blue-500 rounded-xl flex items-center justify-center text-lg">
          <i class="bx bx-shopping-bag"></i>
        </div>
        <div>
          <p class="text-[9px] font-black text-gray-400 uppercase tracking-widest mb-1">{{ t('seller.totalSalesLabel') }}</p>
          <p class="text-2xl font-black text-[#112830]">{{ formatAmount(sellerStats.total_sales) }}</p>
          <p class="text-xs text-gray-400 mt-1">{{ t('seller.allDeliveredLabel') }}</p>
        </div>
      </div>

      <!-- Escrow -->
      <div class="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm space-y-4">
        <div class="w-10 h-10 bg-amber-50 text-amber-500 rounded-xl flex items-center justify-center text-lg">
          <i class="bx bx-lock-alt"></i>
        </div>
        <div>
          <p class="text-[9px] font-black text-gray-400 uppercase tracking-widest mb-1">{{ t('seller.escrow') }}</p>
          <p class="text-2xl font-black text-[#112830]">{{ formatAmount(sellerStats.escrow_balance) }}</p>
          <p class="text-xs text-gray-400 mt-1">{{ t('seller.escrowDesc') }}</p>
        </div>
      </div>
    </div>

    <!-- ===== TRANSACTIONS RÉCENTES ===== -->
    <div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
      <div class="px-6 py-4 border-b border-gray-50 flex items-center justify-between">
        <h3 class="text-sm font-black text-[#112830]">{{ t('seller.lastPayments') }}</h3>
        <NuxtLink to="/seller/history"
          class="text-[10px] font-black text-[#10b481] uppercase tracking-widest hover:underline flex items-center gap-1">
          {{ t('seller.seeHistory') }}
          <i class="bx bx-right-arrow-alt"></i>
        </NuxtLink>
      </div>

      <div v-if="loadingOrders" class="p-10 flex justify-center">
        <div class="w-8 h-8 border-2 border-[#10b481] border-t-transparent rounded-full animate-spin"></div>
      </div>

      <div v-else-if="deliveredOrders.length === 0" class="p-16 text-center space-y-3">
        <div class="w-16 h-16 bg-gray-50 rounded-2xl flex items-center justify-center mx-auto">
          <i class="bx bx-transfer text-3xl text-gray-200"></i>
        </div>
        <p class="text-sm text-gray-400 font-medium">{{ t('seller.noPayments') }}</p>
        <p class="text-xs text-gray-300">{{ t('seller.noPaymentsDesc') }}</p>
      </div>

      <div v-else class="divide-y divide-gray-50">
        <div v-for="order in deliveredOrders.slice(0, 8)" :key="order.id"
          class="flex items-center gap-4 px-6 py-4 hover:bg-gray-50/50 transition-colors">
          <div class="w-10 h-10 bg-emerald-50 text-emerald-600 rounded-xl flex items-center justify-center flex-shrink-0">
            <i class="bx bx-check-circle text-lg"></i>
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-black text-[#112830] truncate">
              {{ order.buyer_name || order.buyer_details?.username || 'Client' }}
            </p>
            <p class="text-[9px] text-gray-400 font-bold">
              {{ order.order_number }} · {{ new Date(order.updated_at || order.created_at).toLocaleDateString('fr-FR') }}
            </p>
          </div>
          <div class="text-right flex-shrink-0">
            <p class="text-sm font-black text-[#10b481]">+{{ order.total }} Ar</p>
            <span class="text-[9px] font-black px-2 py-0.5 bg-emerald-50 text-emerald-600 rounded-lg uppercase tracking-widest">
              {{ t('seller.statusDelivered') }}
            </span>
          </div>
          <NuxtLink :to="`/seller/orders/${order.id}`"
            class="w-8 h-8 rounded-lg hover:bg-gray-100 text-gray-300 hover:text-[#112830] transition-all flex items-center justify-center flex-shrink-0">
            <i class="bx bx-chevron-right text-lg"></i>
          </NuxtLink>
        </div>
      </div>
    </div>

    <!-- ===== MODAL RETRAIT ===== -->
    <div v-if="showWithdrawModal" class="fixed inset-0 z-[100] flex items-center justify-center p-6 backdrop-blur-sm bg-black/20">
      <div class="bg-white w-full max-w-sm rounded-2xl p-8 shadow-2xl space-y-5 border border-gray-100">
        <div class="text-center space-y-2">
          <div class="w-14 h-14 bg-[#112830] rounded-2xl flex items-center justify-center mx-auto">
            <i class="bx bx-wallet text-2xl text-[#10b481]"></i>
          </div>
          <h2 class="text-base font-black text-[#112830]">{{ t('seller.withdrawModalTitle') }}</h2>
          <p class="text-sm text-gray-400">
            {{ t('seller.availableBalanceColon') }}
            <span class="font-black text-[#10b481]">{{ formatAmount(sellerStats.available_balance) }}</span>
          </p>
        </div>
        <div class="space-y-2">
          <label class="text-[9px] font-black text-gray-400 uppercase tracking-widest block">{{ t('seller.withdrawAmountLabel') }}</label>
          <input v-model="withdrawAmount" type="number" placeholder="Ex: 50000"
            class="w-full px-4 py-3 bg-gray-50 border border-gray-100 rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/30 font-medium" />
        </div>
        <div class="flex gap-3">
          <button @click="showWithdrawModal = false"
            class="flex-1 py-3 rounded-xl border border-gray-100 text-gray-500 font-bold text-sm hover:bg-gray-50 transition-colors">
            {{ t('dashboard.cancel') }}
          </button>
          <button @click="submitWithdraw" :disabled="!withdrawAmount || isWithdrawing"
            class="flex-1 py-3 rounded-xl bg-[#112830] text-white font-bold text-sm hover:bg-[#10b481] transition-all disabled:opacity-40 flex items-center justify-center gap-2">
            <div v-if="isWithdrawing" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            <i v-else class="bx bx-send"></i>
            {{ t('seller.withdrawBtn') }}
          </button>
        </div>
      </div>
    </div>

    <!-- Toast -->
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

const { apiFetch } = useApi();
const { sellerStats, fetchSellerStats } = useMarketplace();

const loadingOrders     = ref(true);
const allOrders         = ref<any[]>([]);
const showWithdrawModal = ref(false);
const withdrawAmount    = ref('');
const isWithdrawing     = ref(false);
const toast = ref({ visible: false, message: '', type: 'success' as 'success' | 'error' });

const deliveredOrders = computed(() =>
  allOrders.value.filter(o => o.status === 'DELIVERED')
);

onMounted(async () => {
  fetchSellerStats();
  try {
    const data = await apiFetch('/api/orders/orders/?as_seller=true');
    allOrders.value = data.results || data || [];
  } catch (err) {
    console.error('Erreur chargement commandes', err);
  } finally {
    loadingOrders.value = false;
  }
});

function formatAmount(val: number) {
  return new Intl.NumberFormat('fr-MG').format(val || 0) + ' Ar';
}

function showToast(message: string, type: 'success' | 'error' = 'success') {
  toast.value = { visible: true, message, type };
  setTimeout(() => (toast.value.visible = false), 3000);
}

function openWithdrawModal() {
  withdrawAmount.value = '';
  showWithdrawModal.value = true;
}

async function submitWithdraw() {
  if (!withdrawAmount.value) return;
  isWithdrawing.value = true;
  try {
    await apiFetch('/api/payments/withdraw/', {
      method: 'POST',
      body: { amount: Number(withdrawAmount.value) },
    });
    showWithdrawModal.value = false;
    showToast(t('seller.withdrawSuccess'));
    fetchSellerStats();
  } catch {
    showToast(t('seller.withdrawError'), 'error');
  } finally {
    isWithdrawing.value = false;
  }
}
</script>

<style scoped>
.slide-up-enter-active, .slide-up-leave-active { transition: all 0.3s ease; }
.slide-up-enter-from, .slide-up-leave-to { opacity: 0; transform: translate(-50%, 1rem); }
</style>