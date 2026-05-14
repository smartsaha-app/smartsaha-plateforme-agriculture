<template>
  <div class="space-y-10 pb-20">
    <!-- Header -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
      <div>
        <h1 class="text-4xl font-black text-[#112830] tracking-tight">Espace Vendeur</h1>
        <p class="text-gray-500 font-medium mt-1">Gérez vos produits, suivez vos ventes et boostez votre activité.</p>
      </div>
      <div class="flex gap-4">
        <button @click="navigateTo('/seller/products')" class="px-6 py-4 bg-white border border-gray-100 rounded-2xl font-black text-xs uppercase tracking-widest hover:shadow-md transition-all">
          Mes Produits
        </button>
        <button @click="navigateTo('/seller/products/new')" class="px-6 py-4 bg-[#112830] text-white rounded-2xl font-black text-xs uppercase tracking-widest shadow-xl shadow-[#112830]/10 hover:bg-[#10b481] transition-all flex items-center gap-2">
          <i class="bx bx-plus text-lg"></i>
          Nouveau Produit
        </button>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div v-for="stat in stats" :key="stat.label" class="bg-white p-8 rounded-[2.5rem] border border-gray-50 shadow-sm hover:shadow-md transition-all group">
        <div :class="stat.bgClass" class="w-14 h-14 rounded-2xl flex items-center justify-center text-2xl mb-6 transition-transform group-hover:scale-110">
          <i :class="stat.icon"></i>
        </div>
        <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest mb-1">{{ stat.label }}</p>
        <p class="text-3xl font-black text-[#112830]">{{ stat.value }}</p>
        <div v-if="stat.trend" class="mt-4 flex items-center gap-2">
          <span :class="stat.trend > 0 ? 'text-emerald-500 bg-emerald-50' : 'text-rose-500 bg-rose-50'" class="text-[10px] font-black px-2 py-1 rounded-lg">
            {{ stat.trend > 0 ? '+' : '' }}{{ stat.trend }}%
          </span>
          <span class="text-[10px] text-gray-400 font-bold uppercase tracking-widest">vs mois dernier</span>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-10">
      <!-- Recent Orders Table -->
      <div class="lg:col-span-2 bg-white rounded-[3rem] border border-gray-50 shadow-sm overflow-hidden">
        <div class="p-8 border-b border-gray-50 flex justify-between items-center">
          <h3 class="text-xl font-black text-[#112830]">Commandes Récentes</h3>
          <button @click="navigateTo('/seller/orders')" class="text-xs font-black text-[#10b481] uppercase tracking-widest hover:underline">Voir tout</button>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-left">
            <thead>
              <tr class="bg-gray-50/50">
                <th class="px-8 py-5 text-[10px] font-black text-gray-400 uppercase tracking-widest">Acheteur</th>
                <th class="px-8 py-5 text-[10px] font-black text-gray-400 uppercase tracking-widest">Total</th>
                <th class="px-8 py-5 text-[10px] font-black text-gray-400 uppercase tracking-widest">Statut</th>
                <th class="px-8 py-5"></th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-50">
              <tr v-for="order in recentOrders" :key="order.id" class="hover:bg-gray-50/50 transition-colors cursor-pointer" @click="navigateTo(`/seller/orders/${order.id}`)">
                <td class="px-8 py-6">
                  <div class="flex items-center gap-3">
                    <div class="w-10 h-10 bg-[#112830] rounded-xl flex items-center justify-center text-white font-black text-xs">
                      {{ order.buyer_name?.charAt(0).toUpperCase() }}
                    </div>
                    <div>
                      <p class="font-black text-[#112830]">{{ order.buyer_name }}</p>
                      <p class="text-[10px] text-gray-400 font-bold">{{ order.order_number }}</p>
                    </div>
                  </div>
                </td>
                <td class="px-8 py-6">
                  <p class="font-black text-[#10b481]">{{ order.total }} Ar</p>
                </td>
                <td class="px-8 py-6">
                  <span :class="getStatusClass(order.status)" class="px-3 py-1.5 rounded-xl text-[9px] font-black uppercase tracking-widest">
                    {{ order.status }}
                  </span>
                </td>
                <td class="px-8 py-6 text-right">
                  <i class="bx bx-chevron-right text-2xl text-gray-300"></i>
                </td>
              </tr>
            </tbody>
          </table>
          <div v-if="recentOrders.length === 0" class="p-20 text-center space-y-4">
             <i class="bx bx-shopping-bag text-5xl text-gray-200"></i>
             <p class="text-gray-400 font-bold uppercase tracking-widest text-xs">Aucune commande reçue</p>
          </div>
        </div>
      </div>

      <!-- Inventory Alert -->
      <div class="space-y-6">
        <div class="bg-[#112830] text-white p-10 rounded-[3rem] shadow-xl relative overflow-hidden">
          <h3 class="text-xl font-black mb-8 relative z-10">Alertes Stock</h3>
          <div v-if="lowStockProducts.length > 0" class="space-y-4 relative z-10">
            <div v-for="prod in lowStockProducts" :key="prod.id" class="flex items-center justify-between p-4 bg-white/5 rounded-2xl border border-white/10">
              <div>
                <p class="font-bold text-sm">{{ prod.name }}</p>
                <p class="text-[10px] text-white/50 uppercase tracking-widest">Reste: {{ prod.stock }} {{ prod.unit }}</p>
              </div>
              <button @click="navigateTo(`/seller/products/edit/${prod.id}`)" class="w-8 h-8 bg-white/10 rounded-lg flex items-center justify-center hover:bg-[#10b481] transition-all">
                <i class="bx bx-plus text-lg"></i>
              </button>
            </div>
          </div>
          <div v-else class="text-center py-10 relative z-10">
             <i class="bx bx-check-circle text-5xl text-[#10b481] mb-4"></i>
             <p class="text-sm font-bold text-white/70">Tout vos stocks sont à jour !</p>
          </div>
          <!-- Decor -->
          <i class="bx bx-package absolute bottom-[-10%] right-[-10%] text-white/5 text-[12rem]"></i>
        </div>

        <div class="bg-white p-8 rounded-[2.5rem] border border-gray-50 shadow-sm flex items-center gap-6 group hover:border-[#10b481] transition-all cursor-pointer">
          <div class="w-16 h-16 bg-blue-50 text-blue-600 rounded-[1.5rem] flex items-center justify-center text-3xl flex-shrink-0 group-hover:bg-blue-600 group-hover:text-white transition-all">
            <i class="bx bx-bar-chart-square"></i>
          </div>
          <div>
            <h4 class="font-black text-[#112830] uppercase tracking-widest text-[11px] mb-1">Rapport de Ventes</h4>
            <p class="text-xs text-gray-400 font-medium">Téléchargez votre bilan mensuel.</p>
          </div>
          <i class="bx bx-download text-2xl ml-auto text-gray-300"></i>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useMarketplace } from '~/composables/useMarketplace';

definePageMeta({
  layout: 'dashboard'
});

const { apiFetch } = useApi();

const stats = ref([
  { label: 'Ventes Totales', value: '0 Ar', icon: 'bx bx-dollar-circle', bgClass: 'bg-emerald-50 text-emerald-600', trend: 12 },
  { label: 'Commandes', value: '0', icon: 'bx bx-shopping-bag', bgClass: 'bg-blue-50 text-blue-600', trend: 5 },
  { label: 'Produits Actifs', value: '0', icon: 'bx bx-store', bgClass: 'bg-amber-50 text-amber-600' },
  { label: 'Note Vendeur', value: '4.8/5', icon: 'bx bxs-star', bgClass: 'bg-rose-50 text-rose-600' },
]);

const recentOrders = ref<any[]>([]);
const lowStockProducts = ref<any[]>([]);

onMounted(async () => {
  try {
    // Fetch Seller Stats & Data
    const [ordersData, productsData] = await Promise.all([
      apiFetch('/api/orders/orders/?as_seller=true'),
      apiFetch('/api/catalogue/products/?seller=me')
    ]);

    const orders = ordersData.results || ordersData;
    const products = productsData.results || productsData;

    recentOrders.value = orders.slice(0, 5);
    lowStockProducts.value = products.filter((p: any) => p.stock < 10).slice(0, 3);

    // Calculate stats
    const totalSales = orders.reduce((sum: number, o: any) => sum + (parseFloat(o.total) || 0), 0);
    stats.value[0].value = totalSales.toLocaleString() + ' Ar';
    stats.value[1].value = orders.length.toString();
    stats.value[2].value = products.filter((p: any) => p.is_active).length.toString();

  } catch (err) {
    console.error('Failed to load seller dashboard', err);
  }
});

const getStatusClass = (status: string) => {
  switch (status) {
    case 'PENDING': return 'bg-amber-50 text-amber-600';
    case 'PAID': return 'bg-emerald-50 text-emerald-600';
    case 'SHIPPED': return 'bg-blue-50 text-blue-600';
    case 'CANCELLED': return 'bg-rose-50 text-rose-600';
    default: return 'bg-gray-50 text-gray-600';
  }
};
</script>
