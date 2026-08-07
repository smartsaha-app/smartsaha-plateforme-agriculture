<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8 space-y-6">

    <!-- ===== HEADER ===== -->
    <PageHeader :title="orderDetail ? `Commande ${orderDetail.order_number}` : 'Chargement...'">
      <template #subtitle>
        <template v-if="orderDetail">
          <span :class="getStatusClass(orderDetail.status)"
            class="px-2.5 py-1 rounded-lg text-[9px] font-black uppercase tracking-widest">
            {{ getStatusLabel(orderDetail.status) }}
          </span>
          <span class="text-gray-400">· {{ t('seller.receivedOn') }} {{ formatDate(orderDetail.created_at) }}</span>
        </template>
      </template>
      <template #breadcrumb>
        <NuxtLink to="/seller/dashboard" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
          <span>{{ t('dashboard.home') }}</span>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <NuxtLink to="/seller/orders" class="hover:text-[#10b481] transition-colors">{{ t('seller.ordersTitle') }}</NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">{{ t('seller.orderDetailTitle') }}</span>
      </template>
    </PageHeader>

    <!-- Action button after header -->
    <div class="flex justify-end -mt-2">
      <button @click="printOrder"
        class="flex items-center gap-2 px-4 py-2.5 bg-white border border-gray-100 rounded-xl text-sm font-bold text-[#112830] hover:bg-gray-50 transition-all shadow-sm">
        <i class="bx bx-printer text-base"></i>
        Bon de commande
      </button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex justify-center py-20">
      <div class="w-10 h-10 border-2 border-[#10b481] border-t-transparent rounded-full animate-spin"></div>
    </div>

    <template v-else-if="orderDetail">

      <!-- ===== ACTION BAR ===== -->
      <div v-if="orderDetail.status !== 'DELIVERED' && orderDetail.status !== 'CANCELLED'"
        class="bg-[#112830] p-5 rounded-2xl shadow-lg flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div class="flex items-center gap-4">
          <div class="w-10 h-10 bg-[#10b481] text-white rounded-xl flex items-center justify-center flex-shrink-0">
            <i class="bx bx-info-circle text-lg"></i>
          </div>
          <div>
            <p class="text-white font-black text-sm">{{ t('seller.requiredAction') }}</p>
            <p class="text-gray-400 text-xs font-medium">{{ getNextActionText(orderDetail.status) }}</p>
          </div>
        </div>
        <div class="flex gap-2 w-full sm:w-auto">
          <button v-if="orderDetail.status === 'PAID'" @click="confirmStatusChange('CONFIRMED')" :disabled="updating"
            class="flex-1 sm:flex-none px-5 py-2.5 bg-[#10b481] text-white rounded-xl font-bold text-xs uppercase tracking-widest hover:bg-emerald-400 transition-all disabled:opacity-50">
            Confirmer la commande
          </button>
          <button v-if="orderDetail.status === 'CONFIRMED'" @click="confirmStatusChange('SHIPPED')" :disabled="updating"
            class="flex-1 sm:flex-none px-5 py-2.5 bg-blue-500 text-white rounded-xl font-bold text-xs uppercase tracking-widest hover:bg-blue-400 transition-all disabled:opacity-50">
            Marquer expédiée
          </button>
          <button v-if="orderDetail.status === 'SHIPPED'" @click="confirmStatusChange('DELIVERED')" :disabled="updating"
            class="flex-1 sm:flex-none px-5 py-2.5 bg-emerald-500 text-white rounded-xl font-bold text-xs uppercase tracking-widest hover:bg-emerald-400 transition-all disabled:opacity-50">
            Confirmer livraison
          </button>
        </div>
      </div>

      <!-- ===== CONTENT ===== -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

        <!-- Left: produits commandés -->
        <div class="lg:col-span-2 space-y-4">
          <div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
            <div class="px-6 py-4 border-b border-gray-50 flex items-center justify-between">
              <h3 class="text-sm font-black text-[#112830]">{{ t('seller.orderedProducts') }}</h3>
              <span class="px-2.5 py-1 bg-gray-50 text-gray-500 rounded-lg text-[9px] font-black uppercase">
                {{ orderDetail.items?.length }} article{{ (orderDetail.items?.length || 0) > 1 ? 's' : '' }}
              </span>
            </div>
            <div class="divide-y divide-gray-50">
              <div v-for="item in orderDetail.items" :key="item.id" class="p-5 flex gap-4 items-center">
                <div class="w-16 h-16 bg-gray-50 rounded-xl overflow-hidden border border-gray-100 flex-shrink-0">
                  <img v-if="item.product_image" :src="item.product_image" class="w-full h-full object-cover" />
                  <i v-else class="bx bx-image text-gray-200 text-2xl flex items-center justify-center h-full w-full"></i>
                </div>
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-black text-[#112830] truncate">{{ item.product_name }}</p>
                  <p class="text-xs font-bold text-[#10b481]">{{ item.price }} Ar / unité</p>
                  <p v-if="item.product_stock !== undefined"
                    class="text-[9px] font-black uppercase tracking-widest mt-0.5"
                    :class="item.product_stock < 5 ? 'text-rose-500' : 'text-gray-400'">
                    Stock: {{ item.product_stock }}
                  </p>
                </div>
                <div class="text-right flex-shrink-0">
                  <p class="text-[9px] font-bold text-gray-400 uppercase tracking-widest">Qté</p>
                  <p class="text-lg font-black text-[#112830]">×{{ item.quantity }}</p>
                </div>
                <div class="text-right border-l border-gray-100 pl-4 flex-shrink-0 min-w-[90px]">
                  <p class="text-[9px] font-bold text-gray-400 uppercase tracking-widest">{{ t('buyer.subtotal') }}</p>
                  <p class="text-base font-black text-[#112830]">{{ item.subtotal }} Ar</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right: client + finances -->
        <div class="space-y-4">

          <!-- Client -->
          <div class="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm space-y-4">
            <div class="flex items-center gap-3 mb-1">
              <div class="w-9 h-9 bg-blue-50 text-blue-500 rounded-xl flex items-center justify-center">
                <i class="bx bx-user text-base"></i>
              </div>
              <h3 class="text-sm font-black text-[#112830]">{{ t('seller.buyerInfo') }}</h3>
            </div>

            <div class="flex items-center gap-3 p-3 bg-gray-50 rounded-xl">
              <div class="w-9 h-9 bg-[#112830] rounded-full flex items-center justify-center text-white font-black text-sm flex-shrink-0">
                {{ (orderDetail.buyer_name || '?').charAt(0).toUpperCase() }}
              </div>
              <div class="min-w-0">
                <p class="text-sm font-black text-[#112830] truncate">{{ orderDetail.buyer_name }}</p>
                <p class="text-[9px] text-gray-400 font-bold truncate">{{ orderDetail.buyer_details?.email }}</p>
              </div>
            </div>

            <div class="space-y-2.5">
              <div class="flex items-center gap-2.5 text-sm text-gray-500">
                <i class="bx bx-phone text-gray-300 flex-shrink-0"></i>
                <span class="font-medium">{{ orderDetail.delivery_phone || '—' }}</span>
              </div>
              <div class="flex items-start gap-2.5 text-sm text-gray-500">
                <i class="bx bx-map text-gray-300 flex-shrink-0 mt-0.5"></i>
                <span class="font-medium">{{ orderDetail.delivery_address }}, {{ orderDetail.delivery_city }}</span>
              </div>
            </div>
          </div>

          <!-- Finances -->
          <div class="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm space-y-4">
            <h3 class="text-sm font-black text-[#112830]">{{ t('seller.deliverySummaryTitle') }}</h3>
            <div class="space-y-2.5">
              <div class="flex justify-between text-sm">
                <span class="text-gray-400 font-medium">{{ t('buyer.subtotal') }}</span>
                <span class="font-black text-[#112830]">{{ orderDetail.subtotal }} Ar</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-400 font-medium">Commission SmartSaha</span>
                <span class="font-black text-rose-500">— 0 Ar</span>
              </div>
              <div class="pt-3 border-t border-gray-100 flex justify-between items-center">
                <span class="text-sm font-black text-[#112830]">Net à recevoir</span>
                <span class="text-xl font-black text-[#10b481]">{{ orderDetail.subtotal }} Ar</span>
              </div>
            </div>
            <div v-if="orderDetail.payment_status === 'ESCROWED'"
              class="p-3 bg-emerald-50 text-emerald-600 rounded-xl text-[9px] font-black uppercase text-center tracking-widest border border-emerald-100">
              <i class="bx bx-lock-alt mr-1"></i>
              Fonds en séquestre
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- ===== CONFIRM MODAL ===== -->
    <div v-if="pendingStatus" class="fixed inset-0 z-[100] flex items-center justify-center p-6 backdrop-blur-sm bg-black/20">
      <div class="bg-white w-full max-w-sm rounded-2xl p-8 shadow-2xl space-y-5 border border-gray-100">
        <div class="text-center space-y-3">
          <div class="w-14 h-14 bg-[#112830] rounded-2xl flex items-center justify-center mx-auto">
            <i class="bx bx-check-circle text-2xl text-[#10b481]"></i>
          </div>
          <div>
            <h2 class="text-base font-black text-[#112830]">{{ t('dashboard.confirm') }} ?</h2>
            <p class="text-sm text-gray-400 mt-1">
              {{ t('dashboard.status') }} : <span class="font-bold text-[#112830]">{{ getStatusLabel(pendingStatus) }}</span>.
            </p>
          </div>
        </div>
        <div class="flex gap-3">
          <button @click="pendingStatus = null"
            class="flex-1 py-3 rounded-xl border border-gray-100 text-gray-500 font-bold text-sm hover:bg-gray-50 transition-colors">
            Annuler
          </button>
          <button @click="applyStatusChange" :disabled="updating"
            class="flex-1 py-3 rounded-xl bg-[#112830] text-white font-bold text-sm hover:bg-[#10b481] transition-all disabled:opacity-50 flex items-center justify-center gap-2">
            <div v-if="updating" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            <i v-else class="bx bx-check"></i>
            Confirmer
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
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useMarketplace } from '~/composables/useMarketplace';

const { t } = useI18n();
definePageMeta({ layout: 'dashboard' });

const route  = useRoute();
const { orderDetail, loading, fetchOrderDetail, updateOrderStatus } = useMarketplace();

const updating     = ref(false);
const pendingStatus = ref<string | null>(null);
const toast = ref({ visible: false, message: '', type: 'success' as 'success' | 'error' });

onMounted(() => {
  if (route.params.id) fetchOrderDetail(route.params.id as string);
});

function showToast(message: string, type: 'success' | 'error' = 'success') {
  toast.value = { visible: true, message, type };
  setTimeout(() => (toast.value.visible = false), 3000);
}

function confirmStatusChange(status: string) {
  pendingStatus.value = status;
}

async function applyStatusChange() {
  if (!pendingStatus.value || !orderDetail.value) return;
  updating.value = true;
  try {
    await updateOrderStatus(orderDetail.value.id, pendingStatus.value);
    orderDetail.value.status = pendingStatus.value;
    showToast(`${t('seller.statusConfirmed')} : ${getStatusLabel(pendingStatus.value)}`);
  } catch {
    showToast(t('seller.updateStatusError'), 'error');
  } finally {
    updating.value = false;
    pendingStatus.value = null;
  }
}

function printOrder() {
  window.print();
}

const formatDate = (d: string) => {
  if (!d) return '';
  return new Date(d).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' });
};

const getStatusLabel = (status: string) => {
  const map: Record<string, string> = {
    PENDING: 'En attente', PAID: 'Payée', CONFIRMED: 'Confirmée',
    SHIPPED: 'Expédiée', DELIVERED: 'Livrée', CANCELLED: 'Annulée',
  };
  return map[status] || status;
};

const getStatusClass = (status: string) => {
  switch (status) {
    case 'PAID':      return 'bg-emerald-50 text-emerald-600';
    case 'CONFIRMED': return 'bg-blue-50 text-blue-600';
    case 'SHIPPED':   return 'bg-indigo-50 text-indigo-600';
    case 'DELIVERED': return 'bg-emerald-100 text-emerald-700';
    case 'CANCELLED': return 'bg-rose-50 text-rose-500';
    default:          return 'bg-gray-100 text-gray-500';
  }
};

const getNextActionText = (status: string) => {
  const map: Record<string, string> = {
    PENDING:   t('seller.statusPending'),
    PAID:      t('seller.confirmOrderBtn'),
    CONFIRMED: t('seller.markShipped'),
    SHIPPED:   t('seller.confirmDeliveryBtn'),
  };
  return map[status] || t('seller.requiredAction');
};
</script>

<style scoped>
.slide-up-enter-active, .slide-up-leave-active { transition: all 0.3s ease; }
.slide-up-enter-from, .slide-up-leave-to { opacity: 0; transform: translate(-50%, 1rem); }
</style>