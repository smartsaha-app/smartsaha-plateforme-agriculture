<template>
  <div class="space-y-8">
    <!-- Header -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <h1 class="text-3xl font-black text-[#112830]">{{ $t('buyer.dashboardTitle') }}</h1>
        <p class="text-gray-500 font-medium">{{ $t('buyer.dashboardDesc') }}</p>
      </div>
      <NuxtLink 
        to="/buyer/products"
        class="px-6 py-3 bg-[#10b481] text-white rounded-2xl font-black text-xs uppercase tracking-widest shadow-lg shadow-[#10b481]/20 hover:scale-105 transition-all flex items-center gap-2"
      >
        <i class="bx bx-plus text-lg"></i>
        {{ $t('buyer.newPurchase') }}
      </NuxtLink>
    </div>

    <!-- Stats Grid -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div v-for="stat in stats" :key="stat.label" class="bg-white p-8 rounded-[2.5rem] border border-gray-100 shadow-sm hover:shadow-md transition-all group">
        <div class="flex items-center justify-between mb-4">
          <div :class="[stat.color, 'w-12 h-12 rounded-2xl flex items-center justify-center text-2xl group-hover:scale-110 transition-transform']">
            <i :class="stat.icon"></i>
          </div>
          <span class="text-[10px] font-black uppercase tracking-widest text-gray-400">{{ $t('buyer.total') }}</span>
        </div>
        <div class="space-y-1">
          <h3 class="text-3xl font-black text-[#112830]">{{ stat.value }}</h3>
          <p class="text-sm font-bold text-gray-400">{{ stat.label }}</p>
        </div>
      </div>
    </div>

    <!-- Main Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Recent Orders -->
      <div class="lg:col-span-2 space-y-6">
        <div class="flex items-center justify-between">
          <h2 class="text-xl font-black text-[#112830]">{{ $t('buyer.recentOrders') }}</h2>
          <NuxtLink to="/buyer/orders" class="text-xs font-black text-[#10b481] uppercase tracking-widest hover:underline">{{ $t('buyer.seeAll') }}</NuxtLink>
        </div>

        <div v-if="loading" class="space-y-4">
          <div v-for="i in 3" :key="i" class="h-24 bg-white rounded-3xl border border-gray-100 animate-pulse"></div>
        </div>

        <div v-else-if="orders.length === 0" class="bg-white py-16 rounded-[2.5rem] border border-gray-100 text-center space-y-4">
          <div class="w-20 h-20 bg-gray-50 rounded-full flex items-center justify-center mx-auto">
            <i class="bx bx-shopping-bag text-4xl text-gray-300"></i>
          </div>
          <div class="space-y-2">
            <h4 class="text-lg font-black text-[#112830]">{{ $t('buyer.noOrders') }}</h4>
            <p class="text-gray-400 text-sm max-w-xs mx-auto">{{ $t('buyer.noOrdersDesc') }}</p>
          </div>
          <NuxtLink to="/buyer/products" class="inline-block text-sm font-black text-[#10b481] hover:underline">{{ $t('buyer.goToShop') }}</NuxtLink>
        </div>

        <div v-else class="space-y-4">
          <div 
            v-for="order in orders.slice(0, 5)" 
            :key="order.id"
            @click="navigateTo(`/buyer/orders/${order.id}`)"
            class="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm hover:shadow-md hover:border-[#10b481]/30 transition-all cursor-pointer flex items-center gap-6 group"
          >
            <div class="w-14 h-14 bg-gray-50 rounded-2xl flex items-center justify-center text-[#112830] group-hover:bg-emerald-50 group-hover:text-[#10b481] transition-colors">
              <i class="bx bx-package text-2xl"></i>
            </div>
            <div class="flex-1">
              <div class="flex justify-between items-start mb-1">
                <h4 class="font-black text-[#112830]">{{ order.order_number }}</h4>
                <span class="text-[#10b481] font-black">{{ order.total }} Ar</span>
              </div>
              <div class="flex items-center gap-4 text-xs font-bold text-gray-400">
                <span class="flex items-center gap-1">
                  <i class="bx bx-calendar"></i>
                  {{ formatDate(order.created_at) }}
                </span>
                <span :class="getStatusClass(order.status)" class="px-2 py-0.5 rounded-full text-[10px] uppercase tracking-tighter">
                  {{ getStatusLabel(order.status) }}
                </span>
              </div>
            </div>
            <i class="bx bx-chevron-right text-gray-300 text-xl group-hover:translate-x-1 transition-transform"></i>
          </div>
        </div>
      </div>

      <!-- Quick Actions / Sidebar -->
      <div class="space-y-6">
        <div class="bg-[#112830] p-8 rounded-[2.5rem] text-white relative overflow-hidden shadow-xl shadow-[#112830]/10">
          <div class="relative z-10 space-y-4">
            <h3 class="text-xl font-black">{{ $t('buyer.needHelp') }}</h3>
            <p class="text-white/60 text-sm font-medium leading-relaxed">{{ $t('buyer.helpDesc') }}</p>
            <div class="flex flex-col gap-3 pt-2">
              <NuxtLink to="/support" class="flex items-center gap-3 text-sm font-bold text-white hover:text-[#10b481] transition-colors">
                <i class="bx bx-help-circle"></i>
                {{ $t('buyer.helpCenter') }}
              </NuxtLink>
              <NuxtLink to="/contact" class="flex items-center gap-3 text-sm font-bold text-white hover:text-[#10b481] transition-colors">
                <i class="bx bx-message-rounded-detail"></i>
                {{ $t('buyer.contactSupport') }}
              </NuxtLink>
            </div>
          </div>
          <i class="bx bx-support absolute bottom-[-10%] right-[-10%] text-white/5 text-[10rem]"></i>
        </div>

        <div class="bg-white p-8 rounded-[2.5rem] border border-gray-100 shadow-sm space-y-6">
          <h3 class="text-lg font-black text-[#112830]">{{ $t('buyer.quickSettings') }}</h3>
          <div class="space-y-2">
            <button class="w-full flex items-center justify-between p-4 rounded-2xl hover:bg-gray-50 transition-colors group">
              <span class="flex items-center gap-3 text-sm font-bold text-gray-600 group-hover:text-[#112830]">
                <i class="bx bx-map-pin text-xl text-gray-400 group-hover:text-[#10b481]"></i>
                {{ $t('buyer.deliveryAddresses') }}
              </span>
              <i class="bx bx-chevron-right text-gray-300"></i>
            </button>
            <button class="w-full flex items-center justify-between p-4 rounded-2xl hover:bg-gray-50 transition-colors group">
              <span class="flex items-center gap-3 text-sm font-bold text-gray-600 group-hover:text-[#112830]">
                <i class="bx bx-credit-card text-xl text-gray-400 group-hover:text-[#10b481]"></i>
                {{ $t('buyer.paymentMethods') }}
              </span>
              <i class="bx bx-chevron-right text-gray-300"></i>
            </button>
            <button class="w-full flex items-center justify-between p-4 rounded-2xl hover:bg-gray-50 transition-colors group">
              <span class="flex items-center gap-3 text-sm font-bold text-gray-600 group-hover:text-[#112830]">
                <i class="bx bx-bell text-xl text-gray-400 group-hover:text-[#10b481]"></i>
                {{ $t('buyer.notifications') }}
              </span>
              <i class="bx bx-chevron-right text-gray-300"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue';
import { useMarketplace } from '~/composables/useMarketplace';

const { t } = useI18n();

definePageMeta({
  layout: 'dashboard'
});

const { orders, loading, fetchOrders } = useMarketplace();

onMounted(() => {
  fetchOrders();
});

const stats = computed(() => [
  { 
    label: t('buyer.totalOrders'), 
    value: orders.value?.length || 0, 
    icon: 'bx bx-shopping-bag', 
    color: 'bg-blue-50 text-blue-500' 
  },
  { 
    label: t('buyer.totalAmount'), 
    value: `${(orders.value || []).reduce((acc: number, curr: any) => acc + parseFloat(curr.total), 0).toLocaleString()} Ar`, 
    icon: 'bx bx-wallet', 
    color: 'bg-emerald-50 text-[#10b481]' 
  },
  { 
    label: t('buyer.pending'), 
    value: (orders.value || []).filter((o: any) => o.status === 'PENDING').length, 
    icon: 'bx bx-time-five', 
    color: 'bg-amber-50 text-amber-500' 
  }
]);

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleDateString('fr-FR', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  });
};

const getStatusLabel = (status: string) => {
  const statuses: Record<string, string> = {
    'PENDING': t('buyer.pending'),
    'PAID': t('buyer.statusPaid'),
    'CONFIRMED': t('buyer.statusConfirmed'),
    'SHIPPED': t('buyer.statusShipped'),
    'DELIVERED': t('buyer.statusDelivered'),
    'CANCELLED': t('buyer.statusCancelled')
  };
  return statuses[status] || status;
};

const getStatusClass = (status: string) => {
  switch (status) {
    case 'DELIVERED': return 'bg-emerald-100 text-emerald-600';
    case 'PENDING': return 'bg-amber-100 text-amber-600';
    case 'CANCELLED': return 'bg-rose-100 text-rose-600';
    case 'SHIPPED': return 'bg-blue-100 text-blue-600';
    default: return 'bg-gray-100 text-gray-600';
  }
};
</script>
