<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8 space-y-6">

    <!-- ===== HEADER ===== -->
    <PageHeader :title="orderDetail ? `Commande ${orderDetail.order_number}` : 'Détail commande'">
      <template #subtitle v-if="orderDetail">
        <span :class="getStatusClass(orderDetail.status)"
          class="px-2.5 py-1 rounded-lg text-[9px] font-black uppercase tracking-widest">
          {{ getStatusLabel(orderDetail.status) }}
        </span>
        <span class="text-gray-400">· {{ formatDate(orderDetail.created_at) }}</span>
      </template>
      <template #breadcrumb>
        <NuxtLink to="/buyer/dashboard" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
          <span>{{ t('dashboard.home') }}</span>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <NuxtLink to="/buyer/orders" class="hover:text-[#10b481] transition-colors">{{ t('buyer.ordersTitle') }}</NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">{{ t('buyer.orderDetailTitle') }}</span>
      </template>
    </PageHeader>

    <!-- Actions header -->
    <div v-if="orderDetail" class="flex justify-end -mt-2 gap-3">
      <button @click="printPage"
        class="flex items-center gap-2 px-4 py-2.5 bg-white border border-gray-100 rounded-xl text-sm font-bold text-[#112830] hover:bg-gray-50 transition-all shadow-sm">
        <i class="bx bx-printer text-base"></i>
        Facture
      </button>
      <NuxtLink to="/buyer/help"
        class="flex items-center gap-2 px-4 py-2.5 bg-[#112830] text-white rounded-xl text-sm font-bold hover:bg-[#10b481] transition-all shadow-sm">
        <i class="bx bx-support text-base"></i>
        Aide
      </NuxtLink>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="grid grid-cols-1 lg:grid-cols-3 gap-6 animate-pulse">
      <div class="lg:col-span-2 space-y-4">
        <div class="h-48 bg-white rounded-2xl border border-gray-100"></div>
        <div class="h-64 bg-white rounded-2xl border border-gray-100"></div>
      </div>
      <div class="h-[400px] bg-white rounded-2xl border border-gray-100"></div>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="bg-white p-10 rounded-2xl border border-rose-100 text-center space-y-4 shadow-sm">
      <i class="bx bx-error-circle text-4xl text-rose-500"></i>
      <h2 class="text-base font-black text-[#112830]">{{ t('buyer.errorOccurred') }}</h2>
      <p class="text-sm text-gray-400">{{ error }}</p>
      <button @click="fetchOrderDetail(route.params.id as string)"
        class="px-5 py-2.5 bg-[#112830] text-white rounded-xl font-bold text-sm hover:bg-[#10b481] transition-all">
        {{ t('buyer.retryBtn') }}
      </button>
    </div>

    <!-- Not found -->
    <div v-else-if="!orderDetail" class="bg-white p-10 rounded-2xl border border-gray-100 text-center space-y-4 shadow-sm">
      <i class="bx bx-search text-4xl text-gray-200"></i>
      <h2 class="text-base font-black text-[#112830]">{{ t('buyer.orderNotFound') }}</h2>
    </div>

    <template v-else-if="orderDetail">

      <!-- ===== TIMELINE ===== -->
      <div class="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
        <h3 class="text-sm font-black text-[#112830] mb-6">{{ t('buyer.orderTracking') }}</h3>
        <div class="flex justify-between relative">
          <div class="absolute top-5 left-0 w-full h-1 bg-gray-100 z-0 rounded-full"></div>
          <div class="absolute top-5 left-0 h-1 bg-[#10b481] z-0 transition-all duration-700 rounded-full"
            :style="{ width: getProgressWidth(orderDetail.status) + '%' }"></div>

          <div v-for="step in statusSteps" :key="step.key" class="relative z-10 flex flex-col items-center gap-2">
            <div :class="[
              'w-10 h-10 rounded-xl flex items-center justify-center text-base transition-all shadow-sm',
              isStepCompleted(step.key, orderDetail.status) ? 'bg-[#10b481] text-white' :
              isStepActive(step.key, orderDetail.status) ? 'bg-white border-2 border-[#10b481] text-[#10b481]' :
              'bg-white border-2 border-gray-100 text-gray-200'
            ]">
              <i :class="step.icon"></i>
            </div>
            <div class="text-center">
              <p class="text-[8px] font-black uppercase tracking-widest text-[#112830] leading-tight max-w-[60px]">{{ step.label }}</p>
              <p v-if="isStepCompleted(step.key, orderDetail.status)" class="text-[8px] font-bold text-[#10b481]">✓</p>
            </div>
          </div>
        </div>
      </div>

      <!-- ===== CONTENT GRID ===== -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

        <!-- Left: articles + action -->
        <div class="lg:col-span-2 space-y-4">

          <!-- Articles -->
          <div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
            <div class="px-6 py-4 border-b border-gray-50 flex items-center justify-between">
              <h3 class="text-sm font-black text-[#112830]">{{ t('buyer.orderedItems') }}</h3>
              <span class="px-2.5 py-1 bg-gray-50 rounded-lg text-[9px] font-black text-gray-400 uppercase tracking-widest">
                {{ orderDetail.items?.length }} article{{ (orderDetail.items?.length || 0) > 1 ? 's' : '' }}
              </span>
            </div>
            <div class="divide-y divide-gray-50">
              <div v-for="item in orderDetail.items" :key="item.id"
                class="p-5 flex gap-4 hover:bg-gray-50/50 transition-colors">
                <div class="w-16 h-16 bg-gray-50 rounded-xl overflow-hidden flex-shrink-0 border border-gray-100">
                  <img v-if="item.product_image" :src="item.product_image" class="w-full h-full object-cover" />
                  <div v-else class="w-full h-full flex items-center justify-center text-gray-300">
                    <i class="bx bx-image text-xl"></i>
                  </div>
                </div>
                <div class="flex-1 min-w-0">
                  <div class="flex justify-between items-start gap-2 mb-1">
                    <div class="min-w-0">
                      <h4 class="text-sm font-black text-[#112830] truncate">{{ item.product_name }}</h4>
                      <p class="text-xs text-gray-400 font-medium">
                        {{ t('buyer.soldBy') }} <span class="text-[#10b481] font-bold">{{ item.seller_name }}</span>
                      </p>
                    </div>
                    <p class="text-sm font-black text-[#112830] flex-shrink-0">{{ item.subtotal }} Ar</p>
                  </div>
                  <div class="flex items-center gap-4 text-xs text-gray-400 font-bold">
                    <span>{{ t('buyer.qtyLabel') }} {{ item.quantity }}</span>
                    <span>{{ item.price }} Ar/unité</span>
                  </div>
                </div>
                <div v-if="orderDetail.status === 'DELIVERED'" class="flex items-center flex-shrink-0">
                  <button class="px-3 py-1.5 bg-emerald-50 text-[#10b481] rounded-xl text-[9px] font-black uppercase tracking-widest hover:bg-[#10b481] hover:text-white transition-all border border-emerald-100">
                    Donner un avis
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Action buttons (contextual) -->
          <div v-if="orderDetail.status === 'PENDING'" class="bg-white p-5 rounded-2xl border border-amber-100 shadow-sm flex items-center justify-between gap-4">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-amber-50 rounded-xl flex items-center justify-center flex-shrink-0">
                <i class="bx bx-credit-card text-amber-500 text-lg"></i>
              </div>
              <div>
                <p class="text-sm font-black text-[#112830]">{{ t('buyer.pendingPayment') }}</p>
                <p class="text-xs text-gray-400">{{ t('buyer.pendingPaymentDesc') }}</p>
              </div>
            </div>
            <NuxtLink :to="`/buyer/payments/checkout/${orderDetail.id}`"
              class="flex-shrink-0 px-5 py-2.5 bg-[#112830] text-white rounded-xl font-bold text-xs uppercase tracking-widest hover:bg-[#10b481] transition-all shadow-sm flex items-center gap-2">
              <i class="bx bx-credit-card"></i>
              Payer maintenant
            </NuxtLink>
          </div>

          <div v-if="orderDetail.status === 'SHIPPED'" class="bg-white p-5 rounded-2xl border border-[#10b481]/20 shadow-sm flex items-center justify-between gap-4">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-emerald-50 rounded-xl flex items-center justify-center flex-shrink-0">
                <i class="bx bx-package text-[#10b481] text-lg"></i>
              </div>
              <div>
                <p class="text-sm font-black text-[#112830]">{{ t('buyer.packageInTransit') }}</p>
                <p class="text-xs text-gray-400">{{ t('buyer.packageInTransitDesc') }}</p>
              </div>
            </div>
            <button @click="openConfirmModal" :disabled="loading"
              class="flex-shrink-0 px-5 py-2.5 bg-[#10b481] text-white rounded-xl font-bold text-xs uppercase tracking-widest hover:bg-emerald-400 transition-all shadow-sm flex items-center gap-2">
              <i class="bx bx-check-circle"></i>
              Confirmer la réception
            </button>
          </div>
        </div>

        <!-- Right: livraison + paiement -->
        <div class="space-y-4">

          <!-- Adresse de livraison -->
          <div class="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm space-y-4">
            <div class="flex items-center gap-3">
              <div class="w-9 h-9 bg-blue-50 text-blue-500 rounded-xl flex items-center justify-center flex-shrink-0">
                <i class="bx bx-map text-base"></i>
              </div>
              <h3 class="text-sm font-black text-[#112830]">{{ t('buyer.deliveryTitle') }}</h3>
            </div>
            <div class="space-y-3 text-sm">
              <div>
                <p class="text-[9px] font-black text-gray-300 uppercase tracking-widest mb-0.5">{{ t('buyer.recipientLabel') }}</p>
                <p class="font-black text-[#112830]">{{ orderDetail.delivery_name }}</p>
                <p class="text-gray-400 font-medium">{{ orderDetail.delivery_phone }}</p>
              </div>
              <div class="pt-2 border-t border-gray-50">
                <p class="text-[9px] font-black text-gray-300 uppercase tracking-widest mb-0.5">{{ t('buyer.addressLabel') }}</p>
                <p class="text-gray-600 font-medium leading-relaxed">
                  {{ orderDetail.delivery_address }}<br />
                  {{ orderDetail.delivery_city }}, {{ orderDetail.delivery_region }}
                </p>
              </div>
              <div v-if="orderDetail.delivery_notes" class="p-3 bg-amber-50 rounded-xl">
                <p class="text-[9px] font-black text-amber-600 uppercase tracking-widest mb-0.5">Notes</p>
                <p class="text-xs font-bold text-amber-700 italic">{{ orderDetail.delivery_notes }}</p>
              </div>
            </div>
          </div>

          <!-- Résumé paiement -->
          <div class="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm space-y-4">
            <div class="flex items-center gap-3">
              <div class="w-9 h-9 bg-emerald-50 text-[#10b481] rounded-xl flex items-center justify-center flex-shrink-0">
                <i class="bx bx-credit-card text-base"></i>
              </div>
              <h3 class="text-sm font-black text-[#112830]">{{ t('buyer.paymentTitle') }}</h3>
            </div>
            <div class="space-y-2.5 text-sm">
              <div class="flex justify-between">
                <span class="text-gray-400 font-medium">{{ t('buyer.methodLabel') }}</span>
                <span class="font-black text-[#112830]">{{ orderDetail.payment_method || '—' }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-400 font-medium">{{ t('buyer.paymentStatusLabel') }}</span>
                <span class="font-black" :class="orderDetail.payment_status === 'PAID' ? 'text-emerald-500' : 'text-amber-500'">
                  {{ orderDetail.payment_status === 'PAID' ? t('buyer.paidLabel') : t('buyer.pending') }}
                </span>
              </div>
              <div class="h-px bg-gray-50 my-1"></div>
              <div class="flex justify-between">
                <span class="text-gray-400 font-medium">{{ t('buyer.subtotal') }}</span>
                <span class="font-black text-[#112830]">{{ orderDetail.subtotal }} Ar</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-400 font-medium">{{ t('buyer.delivery') }}</span>
                <span class="font-black text-[#112830]">{{ orderDetail.delivery_fee || 0 }} Ar</span>
              </div>
              <div class="flex justify-between pt-2 border-t border-gray-50">
                <span class="font-black text-[#112830]">{{ t('buyer.total') }}</span>
                <span class="text-lg font-black text-[#10b481]">{{ orderDetail.total }} Ar</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- ===== CONFIRM MODAL ===== -->
    <div v-if="showConfirmModal" class="fixed inset-0 z-[100] flex items-center justify-center p-6 backdrop-blur-sm bg-black/20">
      <div class="bg-white w-full max-w-sm rounded-2xl p-8 shadow-2xl space-y-5 border border-gray-100">
        <div class="text-center space-y-3">
          <div class="w-14 h-14 bg-emerald-50 rounded-2xl flex items-center justify-center mx-auto">
            <i class="bx bx-check-circle text-2xl text-[#10b481]"></i>
          </div>
          <div>
            <h2 class="text-base font-black text-[#112830]">{{ t('buyer.confirmReceiptModal') }}</h2>
            <p class="text-sm text-gray-400 mt-1">{{ t('buyer.confirmReceiptDesc') }}</p>
          </div>
        </div>
        <div class="flex gap-3">
          <button @click="showConfirmModal = false"
            class="flex-1 py-3 rounded-xl border border-gray-100 text-gray-500 font-bold text-sm hover:bg-gray-50 transition-colors">
            Annuler
          </button>
          <button @click="handleConfirmReceipt" :disabled="loading"
            class="flex-1 py-3 rounded-xl bg-[#10b481] text-white font-bold text-sm hover:bg-emerald-400 transition-all disabled:opacity-50 flex items-center justify-center gap-2">
            <div v-if="loading" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
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
        <i :class="toast.type === 'success' ? 'bx bx-check-circle' : 'bx bx-error-circle'" class="text-lg"
          :style="toast.type === 'success' ? 'color: #10b481' : ''"></i>
        {{ toast.message }}
      </div>
    </transition>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useMarketplace } from '~/composables/useMarketplace';

const { t } = useI18n();
definePageMeta({ layout: 'dashboard' });

const route = useRoute();
const { orderDetail, loading, error, fetchOrderDetail, updateOrderStatus } = useMarketplace();

const showConfirmModal = ref(false);
const toast = ref({ visible: false, message: '', type: 'success' as 'success' | 'error' });

onMounted(() => {
  if (route.params.id) fetchOrderDetail(route.params.id as string);
});

function showToast(message: string, type: 'success' | 'error' = 'success') {
  toast.value = { visible: true, message, type };
  setTimeout(() => (toast.value.visible = false), 3000);
}

function printPage() { if (process.client) window.print(); }
function openConfirmModal() { showConfirmModal.value = true; }

async function handleConfirmReceipt() {
  try {
    await updateOrderStatus(orderDetail.value.id, 'DELIVERED');
    showConfirmModal.value = false;
    showToast(t('buyer.orderConfirmedToast'));
  } catch {
    showToast(t('buyer.errorOccurred'), 'error');
  }
}

const statusSteps = computed(() => [
  { key: 'PENDING',   label: t('buyer.stepOrdered'),   icon: 'bx bx-time'          },
  { key: 'PAID',      label: t('buyer.stepPayment'),   icon: 'bx bx-credit-card'   },
  { key: 'CONFIRMED', label: t('buyer.stepPreparing'), icon: 'bx bx-check-double'  },
  { key: 'SHIPPED',   label: t('buyer.stepDelivery'),  icon: 'bx bx-package'       },
  { key: 'DELIVERED', label: t('buyer.stepDelivered'), icon: 'bx bx-home-heart'    },
]);

const formatDate = (d?: string) => {
  if (!d) return '';
  return new Date(d).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' });
};

const getStatusLabel = (status?: string) => {
  const map: Record<string, string> = {
    PENDING: 'En attente', PAID: 'Payée', CONFIRMED: 'Confirmée',
    SHIPPED: 'Expédiée', DELIVERED: 'Livrée', CANCELLED: 'Annulée',
  };
  return map[status || ''] || status || '';
};

const getStatusClass = (status?: string) => {
  switch (status) {
    case 'DELIVERED': return 'bg-emerald-100 text-emerald-600';
    case 'PENDING':   return 'bg-amber-100 text-amber-600';
    case 'CANCELLED': return 'bg-rose-100 text-rose-600';
    case 'SHIPPED':   return 'bg-blue-100 text-blue-600';
    default:          return 'bg-gray-100 text-gray-600';
  }
};

function isStepCompleted(key: string, current: string) {
  const order = ['PENDING', 'PAID', 'CONFIRMED', 'SHIPPED', 'DELIVERED'];
  return order.indexOf(key) < order.indexOf(current) && order.indexOf(key) !== -1;
}
function isStepActive(key: string, current: string) { return key === current; }
function getProgressWidth(current: string) {
  const order = ['PENDING', 'PAID', 'CONFIRMED', 'SHIPPED', 'DELIVERED'];
  const idx = order.indexOf(current);
  return idx === -1 ? 0 : (idx / (order.length - 1)) * 100;
}
</script>

<style scoped>
.slide-up-enter-active, .slide-up-leave-active { transition: all 0.3s ease; }
.slide-up-enter-from, .slide-up-leave-to { opacity: 0; transform: translate(-50%, 1rem); }
</style>