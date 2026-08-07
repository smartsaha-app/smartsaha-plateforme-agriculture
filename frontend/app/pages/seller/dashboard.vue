<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8 space-y-6">

<!-- ===== BANNIÈRE DE BIENVENUE VENDEUR ===== -->
<div class="relative overflow-hidden rounded-3xl bg-gradient-to-br from-[#112830] via-[#163540] to-[#10b481] p-6 md:p-8 text-white shadow-xl mb-8">
  <!-- Cercles décoratifs en arrière-plan -->
  <div class="absolute -right-10 -bottom-10 w-48 h-48 rounded-full bg-[#10b481]/20 blur-2xl pointer-events-none"></div>
  <div class="absolute right-1/3 -top-10 w-32 h-32 rounded-full bg-emerald-400/10 blur-xl pointer-events-none"></div>

  <div class="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
    <!-- Message de bienvenue -->
    <div class="space-y-2 max-w-xl">
      <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 backdrop-blur-md text-emerald-300 text-xs font-semibold">
        <span>Espace Vendeur</span>
      </div>
      
      <h1 class="text-2xl md:text-3xl font-black tracking-tight">
        Bienvenue, <span class="text-[#10b481]">{{ useAuthStore().firstName }}</span>
      </h1>
      
      <p class="text-gray-300 text-sm md:text-base leading-relaxed">
        {{ t('seller.dashboardDesc') || 'Gérez vos offres, suivez vos ventes en temps réel et développez votre activité.' }}
      </p>
    </div>

    <!-- Actions principales -->
    <div class="flex flex-wrap sm:flex-nowrap items-center gap-3">
      <NuxtLink 
        to="/seller/orders"
        class="inline-flex items-center justify-center gap-2 px-5 py-3 bg-[#10b481] hover:bg-[#0ea072] text-white rounded-2xl font-bold text-xs transition-all duration-200 shadow-lg shadow-[#10b481]/20 hover:scale-[1.02] active:scale-[0.98] w-full sm:w-auto"
      >
        <i class="bx bx-shopping-bag text-base"></i>
        <span>{{ t('seller.dashboardBtn') }}</span>
      </NuxtLink>
    </div>
  </div>
</div>

    <!-- ===== STATS ===== -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <div v-for="stat in stats" :key="stat.label"
        class="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-all group">
        <div class="flex items-center justify-between mb-3">
          <div :class="stat.bgClass" class="w-10 h-10 rounded-xl flex items-center justify-center text-lg">
            <i :class="stat.icon"></i>
          </div>
          <span v-if="stat.trend !== null" :class="stat.trend >= 0 ? 'text-emerald-600 bg-emerald-50' : 'text-rose-500 bg-rose-50'"
            class="text-[9px] font-black px-2 py-0.5 rounded-lg">
            {{ stat.trend >= 0 ? '+' : '' }}{{ stat.trend }}%
          </span>
        </div>
        <p class="text-[9px] font-black text-gray-400 uppercase tracking-widest mb-1">{{ stat.label }}</p>
        <p class="text-xl font-black text-[#112830]">{{ stat.value }}</p>
        <p class="text-[9px] text-gray-400 font-medium mt-1">{{ t('seller.vsLastMonth') }}</p>
      </div>
    </div>

    <!-- ===== MAIN GRID ===== -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

      <!-- Commandes récentes -->
      <div class="lg:col-span-2 bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-50 flex items-center justify-between">
          <h3 class="text-sm font-black text-[#112830]">{{ t('seller.recentOrders') }}</h3>
          <NuxtLink to="/seller/orders"
            class="text-[10px] font-black text-[#10b481] uppercase tracking-widest hover:underline">
            {{ t('seller.seeAll') }}
          </NuxtLink>
        </div>

        <div v-if="loadingOrders" class="p-8 flex justify-center">
          <div class="w-8 h-8 border-2 border-[#10b481] border-t-transparent rounded-full animate-spin"></div>
        </div>

        <div v-else-if="recentOrders.length === 0" class="p-16 text-center">
          <i class="bx bx-shopping-bag text-4xl text-gray-200 mb-3"></i>
          <p class="text-xs font-bold text-gray-400 uppercase tracking-widest">{{ t('seller.noOrders') }}</p>
        </div>

        <div v-else class="overflow-x-auto">
          <table class="w-full text-left">
            <thead>
              <tr class="bg-gray-50/70 border-b border-gray-100">
                <th class="px-5 py-3 text-[9px] font-black text-gray-400 uppercase tracking-widest">{{ t('seller.colBuyer') }}</th>
                <th class="px-5 py-3 text-[9px] font-black text-gray-400 uppercase tracking-widest">{{ t('seller.colTotal') }}</th>
                <th class="px-5 py-3 text-[9px] font-black text-gray-400 uppercase tracking-widest">{{ t('dashboard.status') }}</th>
                <th class="px-5 py-3"></th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-50">
              <tr v-for="order in recentOrders" :key="order.id"
                class="hover:bg-gray-50/50 transition-colors cursor-pointer"
                @click="navigateTo(`/seller/orders/${order.id}`)">
                <td class="px-5 py-4">
                  <div class="flex items-center gap-3">
                    <div class="w-8 h-8 bg-[#112830] rounded-lg flex items-center justify-center text-white font-black text-xs flex-shrink-0">
                      {{ (order.buyer_name || order.buyer_details?.username || 'C')?.charAt(0).toUpperCase() }}
                    </div>
                    <div>
                      <p class="text-sm font-black text-[#112830]">{{ order.buyer_name || order.buyer_details?.username || 'Client' }}</p>
                      <p class="text-[9px] text-gray-400 font-bold">{{ order.order_number }}</p>
                    </div>
                  </div>
                </td>
                <td class="px-5 py-4">
                  <p class="text-sm font-black text-[#10b481]">{{ order.total }} Ar</p>
                </td>
                <td class="px-5 py-4">
                  <span :class="getStatusClass(order.status)"
                    class="px-2.5 py-1 rounded-lg text-[9px] font-black uppercase tracking-widest">
                    {{ getStatusLabel(order.status) }}
                  </span>
                </td>
                <td class="px-5 py-4 text-right">
                  <i class="bx bx-chevron-right text-xl text-gray-300"></i>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Colonne droite -->
      <div class="space-y-5">

        <!-- Alertes stock -->
        <div class="bg-[#112830] text-white p-6 rounded-2xl shadow-lg relative overflow-hidden">
          <i class="bx bx-package absolute bottom-[-15%] right-[-10%] text-white/5 text-[10rem] pointer-events-none"></i>
          <div class="flex items-center justify-between mb-5 relative z-10">
            <h3 class="text-sm font-black">{{ t('seller.stockAlerts') }}</h3>
            <span class="text-[9px] font-black px-2 py-1 bg-white/10 rounded-lg uppercase tracking-widest">
              {{ lowStockProducts.length }} produit{{ lowStockProducts.length !== 1 ? 's' : '' }}
            </span>
          </div>

          <div v-if="lowStockProducts.length > 0" class="space-y-3 relative z-10">
            <div v-for="prod in lowStockProducts" :key="prod.id"
              class="flex items-center justify-between p-3 bg-white/5 border border-white/10 rounded-xl">
              <div class="min-w-0">
                <p class="text-sm font-bold truncate">{{ prod.name }}</p>
                <p class="text-[9px] text-white/50 uppercase tracking-widest">{{ prod.stock }} {{ prod.unit }} restant{{ prod.stock > 1 ? 's' : '' }}</p>
              </div>
              <NuxtLink :to="`/seller/products/edit/${prod.id}`"
                class="w-8 h-8 bg-white/10 rounded-lg flex items-center justify-center hover:bg-[#10b481] transition-all flex-shrink-0 ml-3">
                <i class="bx bx-edit text-sm"></i>
              </NuxtLink>
            </div>
          </div>
          <div v-else class="text-center py-6 relative z-10">
            <i class="bx bx-check-circle text-4xl text-[#10b481] mb-2"></i>
            <p class="text-sm font-bold text-white/70">{{ t('seller.allStocksOk') }}</p>
          </div>
        </div>

        <!-- Top produits -->
        <div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
          <div class="px-5 py-4 border-b border-gray-50">
            <h3 class="text-sm font-black text-[#112830]">{{ t('seller.topProducts') }}</h3>
          </div>
          <div v-if="topProducts.length === 0" class="p-8 text-center text-gray-400 text-xs font-bold">
            {{ t('seller.noSales') }}
          </div>
          <div v-else class="divide-y divide-gray-50">
            <div v-for="(prod, i) in topProducts" :key="prod.id"
              class="flex items-center gap-3 px-5 py-3.5">
              <span class="text-[10px] font-black text-gray-300 w-4">{{ i + 1 }}</span>
              <div class="w-8 h-8 rounded-lg bg-gray-50 border border-gray-100 overflow-hidden flex-shrink-0">
                <img v-if="prod.image_url" :src="prod.image_url" class="w-full h-full object-cover" />
                <i v-else class="bx bx-image text-gray-300 text-xs m-auto flex items-center justify-center h-full"></i>
              </div>
              <div class="flex-1 min-w-0">
                <p class="text-xs font-black text-[#112830] truncate">{{ prod.name }}</p>
                <p class="text-[9px] text-gray-400">{{ prod.sales_count || 0 }} ventes</p>
              </div>
              <span class="text-xs font-black text-[#10b481]">{{ prod.price }} Ar</span>
            </div>
          </div>
        </div>

        <!-- Rapport -->
        <NuxtLink to="/seller/history"
          class="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm flex items-center gap-4 hover:border-[#10b481] transition-all group cursor-pointer">
          <div class="w-12 h-12 bg-blue-50 text-blue-500 rounded-xl flex items-center justify-center text-xl flex-shrink-0 group-hover:bg-blue-500 group-hover:text-white transition-all">
            <i class="bx bx-bar-chart-square"></i>
          </div>
          <div class="flex-1">
            <p class="text-[10px] font-black text-[#112830] uppercase tracking-widest">{{ t('seller.salesHistoryLink') }}</p>
            <p class="text-xs text-gray-400 font-medium">{{ t('seller.salesHistoryLinkDesc') }}</p>
          </div>
          <i class="bx bx-chevron-right text-xl text-gray-300"></i>
        </NuxtLink>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';

definePageMeta({ layout: 'dashboard' });

const { apiFetch } = useApi();
const { t } = useI18n();

const loadingOrders = ref(true);
const recentOrders  = ref<any[]>([]);
const lowStockProducts = ref<any[]>([]);
const topProducts   = ref<any[]>([]);

const stats = ref([
  { label: 'Ventes Totales',  value: '—',    icon: 'bx bx-dollar-circle', bgClass: 'bg-emerald-50 text-emerald-600', trend: null as number | null },
  { label: 'Commandes',       value: '—',    icon: 'bx bx-shopping-bag',  bgClass: 'bg-blue-50 text-blue-600',       trend: null as number | null },
  { label: 'Produits Actifs', value: '—',    icon: 'bx bx-store',         bgClass: 'bg-amber-50 text-amber-600',     trend: null as number | null },
  { label: 'Note Vendeur',    value: '4.8★', icon: 'bx bxs-star',         bgClass: 'bg-rose-50 text-rose-600',       trend: null as number | null },
]);

onMounted(async () => {
  try {
    const [ordersData, productsData] = await Promise.all([
      apiFetch('/api/orders/orders/?as_seller=true'),
      apiFetch('/api/catalogue/products/?seller=me'),
    ]);

    const orders   = ordersData.results  || ordersData  || [];
    const products = productsData.results || productsData || [];

    recentOrders.value     = orders.slice(0, 5);
    lowStockProducts.value = products.filter((p: any) => p.stock < 10).slice(0, 4);
    topProducts.value      = [...products]
      .sort((a: any, b: any) => (b.sales_count || 0) - (a.sales_count || 0))
      .slice(0, 4);

    const totalSales = orders
      .filter((o: any) => o.status !== 'CANCELLED')
      .reduce((sum: number, o: any) => sum + (parseFloat(o.total) || 0), 0);

    if (stats.value[0]) stats.value[0].value = totalSales.toLocaleString('fr-MG') + ' Ar';
    if (stats.value[1]) stats.value[1].value = orders.length.toString();
    if (stats.value[2]) stats.value[2].value = products.filter((p: any) => p.is_active).length.toString();
  } catch (err) {
    console.error('Erreur dashboard vendeur:', err);
  } finally {
    loadingOrders.value = false;
  }
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
    case 'PENDING':   return 'bg-amber-50 text-amber-600';
    case 'PAID':      return 'bg-emerald-50 text-emerald-600';
    case 'CONFIRMED': return 'bg-blue-50 text-blue-600';
    case 'SHIPPED':   return 'bg-indigo-50 text-indigo-600';
    case 'DELIVERED': return 'bg-emerald-100 text-emerald-700';
    case 'CANCELLED': return 'bg-rose-50 text-rose-600';
    default:          return 'bg-gray-50 text-gray-500';
  }
};
</script>