<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8 space-y-6">

    <!-- ===== BANNIÈRE DE BIENVENUE ===== -->
    <div class="relative overflow-hidden rounded-3xl bg-gradient-to-br from-[#112830] via-[#163540] to-[#10b481] p-6 md:p-8 text-white shadow-xl mb-8">
      <!-- Cercles décoratifs en arrière-plan -->
      <div class="absolute -right-10 -bottom-10 w-48 h-48 rounded-full bg-[#10b481]/20 blur-2xl pointer-events-none"></div>
      <div class="absolute right-1/3 -top-10 w-32 h-32 rounded-full bg-emerald-400/10 blur-xl pointer-events-none"></div>

      <div class="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
        <!-- Message de bienvenue -->
        <div class="space-y-2 max-w-xl">
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 backdrop-blur-md text-emerald-300 text-xs font-semibold">
            <span>Espace Acheteur</span>
          </div>
          
          <h1 class="text-2xl md:text-3xl font-black tracking-tight">
            Bienvenue, <span class="text-[#10b481]">{{ useAuthStore().firstName }}</span>
          </h1>
          
          <p class="text-gray-300 text-sm md:text-base leading-relaxed">
            {{ $t('buyer.dashboardDesc')}}
          </p>
        </div>

        <!-- Action principale -->
        <div class="flex items-center gap-3">
          <NuxtLink 
            to="/buyer/products"
            class="inline-flex items-center justify-center gap-2 px-5 py-3.5 bg-[#10b481] hover:bg-[#0ea072] text-white rounded-2xl font-bold text-sm transition-all duration-200 shadow-lg shadow-[#10b481]/20 hover:scale-[1.02] active:scale-[0.98] w-full sm:w-auto"
          >
            <i class="bx bx-shopping-bag text-lg"></i>
            <span>{{ $t('buyer.newPurchase') }}</span>
          </NuxtLink>
        </div>
      </div>
    </div>

    <!-- ===== STATS ===== -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <div v-for="stat in stats" :key="stat.label"
        class="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-all group">
        <div class="flex items-center justify-between mb-3">
          <div :class="[stat.color, 'w-10 h-10 rounded-xl flex items-center justify-center text-lg group-hover:scale-110 transition-transform']">
            <i :class="stat.icon"></i>
          </div>
          <span class="text-[9px] font-black uppercase tracking-widest text-gray-300">{{ $t('buyer.total') }}</span>
        </div>
        <p class="text-2xl font-black text-[#112830]">{{ stat.value }}</p>
        <p class="text-xs font-bold text-gray-400 mt-0.5">{{ stat.label }}</p>
      </div>
    </div>

    <!-- ===== MAIN GRID ===== -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

      <!-- Commandes récentes -->
      <div class="lg:col-span-2 space-y-4">
        <div class="flex items-center justify-between">
          <h2 class="text-sm font-black text-[#112830]">{{ $t('buyer.recentOrders') }}</h2>
          <NuxtLink to="/buyer/orders" class="text-[10px] font-black text-[#10b481] uppercase tracking-widest hover:underline">
            {{ $t('buyer.seeAll') }}
          </NuxtLink>
        </div>

        <div v-if="loading" class="space-y-3">
          <div v-for="i in 3" :key="i" class="h-20 bg-white rounded-2xl border border-gray-100 animate-pulse"></div>
        </div>

        <div v-else-if="orders.length === 0" class="bg-white py-16 rounded-2xl border border-gray-100 text-center space-y-4 shadow-sm">
          <div class="w-16 h-16 bg-gray-50 rounded-2xl flex items-center justify-center mx-auto">
            <i class="bx bx-shopping-bag text-3xl text-gray-200"></i>
          </div>
          <div>
            <h4 class="text-sm font-black text-[#112830]">{{ $t('buyer.noOrders') }}</h4>
            <p class="text-xs text-gray-400 mt-1">{{ $t('buyer.noOrdersDesc') }}</p>
          </div>
          <NuxtLink to="/buyer/products" class="inline-block text-xs font-black text-[#10b481] hover:underline">
            {{ $t('buyer.goToShop') }}
          </NuxtLink>
        </div>

        <div v-else class="space-y-3">
          <div v-for="order in orders.slice(0, 5)" :key="order.id"
            @click="navigateTo(`/buyer/orders/${order.id}`)"
            class="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md hover:border-[#10b481]/20 transition-all cursor-pointer flex items-center gap-4 group">
            <div class="w-11 h-11 bg-gray-50 rounded-xl flex items-center justify-center text-[#112830] group-hover:bg-emerald-50 group-hover:text-[#10b481] transition-colors flex-shrink-0">
              <i class="bx bx-package text-xl"></i>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex justify-between items-center mb-0.5">
                <h4 class="text-sm font-black text-[#112830] truncate">{{ order.order_number }}</h4>
                <span class="text-sm font-black text-[#10b481] flex-shrink-0 ml-2">{{ order.total }} Ar</span>
              </div>
              <div class="flex items-center gap-3 text-xs text-gray-400 font-medium">
                <span>{{ formatDate(order.created_at) }}</span>
                <span :class="getStatusClass(order.status)" class="px-2 py-0.5 rounded-lg text-[9px] font-black uppercase tracking-tight">
                  {{ getStatusLabel(order.status) }}
                </span>
              </div>
            </div>
            <i class="bx bx-chevron-right text-gray-300 text-lg group-hover:translate-x-0.5 transition-transform flex-shrink-0"></i>
          </div>
        </div>
      </div>

      <!-- Colonne droite -->
      <div class="space-y-4">

        <!-- Aide -->
        <div class="bg-[#112830] p-6 rounded-2xl text-white relative overflow-hidden shadow-lg">
          <i class="bx bx-support absolute bottom-[-10%] right-[-10%] text-white/5 text-[8rem] pointer-events-none"></i>
          <div class="relative z-10 space-y-4">
            <div class="w-10 h-10 bg-[#10b481] rounded-xl flex items-center justify-center">
              <i class="bx bx-help-circle text-white text-lg"></i>
            </div>
            <h3 class="text-sm font-black">{{ $t('buyer.needHelp') }}</h3>
            <p class="text-white/60 text-xs leading-relaxed">{{ $t('buyer.helpDesc') }}</p>
            <div class="flex flex-col gap-2 pt-1">
              <NuxtLink to="/buyer/help" class="flex items-center gap-2 text-xs font-bold text-white hover:text-[#10b481] transition-colors">
                <i class="bx bx-message-rounded-detail text-sm"></i>
                {{ $t('buyer.contactSupport') }}
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue';
import { useMarketplace } from '~/composables/useMarketplace';

definePageMeta({ layout: 'dashboard' });

const { t } = useI18n();
const { orders, loading, fetchOrders } = useMarketplace();

onMounted(() => fetchOrders());

const stats = computed(() => [
  {
    label: t('buyer.totalOrders'),
    value: orders.value?.length || 0,
    icon: 'bx bx-shopping-bag',
    color: 'bg-blue-50 text-blue-500',
  },
  {
    label: t('buyer.totalAmount'),
    value: `${(orders.value || []).reduce((acc: number, curr: any) => acc + parseFloat(curr.total || 0), 0).toLocaleString('fr-MG')} Ar`,
    icon: 'bx bx-wallet',
    color: 'bg-emerald-50 text-[#10b481]',
  },
  {
    label: t('buyer.pending'),
    value: (orders.value || []).filter((o: any) => o.status === 'PENDING').length,
    icon: 'bx bx-time-five',
    color: 'bg-amber-50 text-amber-500',
  },
]);

const formatDate = (d: string) =>
  new Date(d).toLocaleDateString('fr-FR', { day: 'numeric', month: 'short', year: 'numeric' });

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