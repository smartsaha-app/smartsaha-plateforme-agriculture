<template>
  <ClientOnly>
    <div class="p-1 sm:p-6 space-y-8 mb-10">
      <!-- ===== EN-TÊTE ===== -->
      <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
        <div>
          <h2 class="text-3xl sm:text-4xl font-black text-[#112830] tracking-tight mb-2">
            {{ t("marketplace") }}
          </h2>
          <p class="text-gray-500 font-medium text-sm flex items-center gap-2">
            <i class="bx bx-store text-[#10b481]"></i>
            Gérez votre boutique et vos transactions
          </p>
        </div>
        
        <NuxtLink 
          to="/farmer/marketplace/new"
          class="flex items-center gap-2 px-6 py-3 bg-[#112830] text-white rounded-2xl hover:bg-[#112830]/90 transition-all font-black text-xs uppercase tracking-widest shadow-lg shadow-[#112830]/20"
        >
          <i class="bx bx-plus text-lg"></i>
          {{ t("newProduct") }}
        </NuxtLink>
      </div>

      <!-- ===== KPI CARDS ===== -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <div class="group relative flex items-center gap-4 p-6 rounded-3xl border border-white bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] hover:shadow-[0_20px_40px_rgb(16,180,129,0.08)] transition-all duration-500 hover:-translate-y-1">
          <div class="w-14 h-14 rounded-2xl flex items-center justify-center text-white flex-shrink-0 bg-[#10b481] shadow-lg shadow-[#10b481]/20 group-hover:scale-110 transition-transform">
            <i class="bx bx-list-check text-2xl"></i>
          </div>
          <div class="min-w-0">
            <p class="text-[10px] font-black uppercase tracking-widest text-gray-400 mb-1">Produits Actifs</p>
            <p class="text-3xl font-black text-[#112830] leading-none">{{ activeProductsCount }}</p>
          </div>
        </div>

        <div class="group relative flex items-center gap-4 p-6 rounded-3xl border border-white bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] hover:shadow-[0_20px_40px_rgb(244,162,97,0.08)] transition-all duration-500 hover:-translate-y-1">
          <div class="w-14 h-14 rounded-2xl flex items-center justify-center text-white flex-shrink-0 bg-[#f4a261] shadow-lg shadow-[#f4a261]/20 group-hover:scale-110 transition-transform">
            <i class="bx bx-cart text-2xl"></i>
          </div>
          <div class="min-w-0">
            <p class="text-[10px] font-black uppercase tracking-widest text-gray-400 mb-1">Commandes Reçues</p>
            <p class="text-3xl font-black text-[#112830] leading-none">{{ orders.length }}</p>
          </div>
        </div>

        <div class="group relative flex items-center gap-4 p-6 rounded-3xl border border-white bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] hover:shadow-[0_20px_40px_rgb(37,99,235,0.08)] transition-all duration-500 hover:-translate-y-1">
          <div class="w-14 h-14 rounded-2xl flex items-center justify-center text-white flex-shrink-0 bg-blue-600 shadow-lg shadow-blue-600/20 group-hover:scale-110 transition-transform">
            <i class="bx bx-dollar-circle text-2xl"></i>
          </div>
          <div class="min-w-0">
            <p class="text-[10px] font-black uppercase tracking-widest text-gray-400 mb-1">Revenu Total</p>
            <p class="text-3xl font-black text-[#112830] leading-none">
              {{ totalRevenue }} <span class="text-sm font-bold text-gray-400">Ar</span>
            </p>
          </div>
        </div>
      </div>

      <!-- ===== TABS ===== -->
      <div class="flex items-center gap-2 p-1 bg-gray-100 rounded-2xl w-fit">
        <button 
          @click="activeTab = 'products'"
          class="px-6 py-2.5 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all"
          :class="activeTab === 'products' ? 'bg-white text-[#112830] shadow-sm' : 'text-gray-400 hover:text-gray-600'"
        >
          {{ t("myProducts") }}
        </button>
        <button 
          @click="activeTab = 'orders'"
          class="px-6 py-2.5 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all"
          :class="activeTab === 'orders' ? 'bg-white text-[#112830] shadow-sm' : 'text-gray-400 hover:text-gray-600'"
        >
          {{ t("receivedOrders") }}
        </button>
      </div>

      <!-- ===== CONTENT ===== -->
      <div v-show="activeTab === 'products'">
        <div v-if="pendingProducts" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          <div v-for="i in 3" :key="i" class="h-80 bg-gray-50 rounded-3xl animate-pulse"></div>
        </div>
        <div v-else-if="products.length === 0" class="bg-white rounded-3xl p-12 text-center border-2 border-dashed border-gray-100">
          <div class="w-20 h-20 bg-gray-50 rounded-full flex items-center justify-center mx-auto mb-6">
            <i class="bx bx-store-alt text-4xl text-gray-300"></i>
          </div>
          <h3 class="text-xl font-black text-[#112830] mb-2">Aucun produit</h3>
          <p class="text-gray-500 mb-8 max-w-xs mx-auto">Commencez à vendre vos produits sur le marché SmartSaha en ajoutant votre premier article.</p>
          <NuxtLink to="/farmer/marketplace/new" class="inline-flex items-center gap-2 px-6 py-3 bg-[#10b481] text-white rounded-2xl font-black text-[10px] uppercase tracking-widest shadow-lg shadow-[#10b481]/20">
            {{ t("newProduct") }}
          </NuxtLink>
        </div>
        <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          <MarketProductCard 
            v-for="prod in products" 
            :key="prod.id" 
            :product="prod"
            :is-owner="true"
            @edit="editProduct"
          />
        </div>
      </div>

      <div v-show="activeTab === 'orders'">
        <div v-if="pendingOrders" class="space-y-4">
          <div v-for="i in 3" :key="i" class="h-24 bg-gray-50 rounded-2xl animate-pulse"></div>
        </div>
        <div v-else-if="orders.length === 0" class="bg-white rounded-3xl p-12 text-center border-2 border-dashed border-gray-100">
          <div class="w-20 h-20 bg-gray-50 rounded-full flex items-center justify-center mx-auto mb-6">
            <i class="bx bx-shopping-bag text-4xl text-gray-300"></i>
          </div>
          <h3 class="text-xl font-black text-[#112830] mb-2">Aucune commande</h3>
          <p class="text-gray-500">Dès qu'un acheteur sera intéressé par vos produits, ses commandes apparaîtront ici.</p>
        </div>
        <div v-else class="bg-white rounded-3xl border border-gray-100 overflow-hidden shadow-sm">
          <table class="w-full">
            <thead class="bg-gray-50 border-b border-gray-100">
              <tr>
                <th class="px-6 py-4 text-left text-[10px] font-black text-gray-400 uppercase tracking-widest italic">Acheteur</th>
                <th class="px-6 py-4 text-left text-[10px] font-black text-gray-400 uppercase tracking-widest italic">Article</th>
                <th class="px-6 py-4 text-left text-[10px] font-black text-gray-400 uppercase tracking-widest italic">Quantité</th>
                <th class="px-6 py-4 text-left text-[10px] font-black text-gray-400 uppercase tracking-widest italic">Total</th>
                <th class="px-6 py-4 text-left text-[10px] font-black text-gray-400 uppercase tracking-widest italic">Statut</th>
                <th class="px-6 py-4 text-right text-[10px] font-black text-gray-400 uppercase tracking-widest italic">Action</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-50">
              <tr v-for="order in orders" :key="order.uuid" class="hover:bg-gray-50/50 transition-colors">
                <td class="px-6 py-4">
                  <div class="flex items-center gap-3">
                    <div class="w-8 h-8 rounded-full bg-[#10b481]/10 flex items-center justify-center text-[#10b481]">
                      <i class="bx bxs-user"></i>
                    </div>
                    <div>
                      <p class="text-sm font-bold text-[#112830]">{{ order.buyer_details.username }}</p>
                      <p class="text-[10px] text-gray-400">{{ order.buyer_details.email }}</p>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 text-sm font-medium text-[#112830] text-pretty">
                  {{ order.items?.[0]?.product_name || 'N/A' }} 
                  <span v-if="order.items?.length > 1" class="text-[10px] text-gray-400 font-bold ml-1">+{{ order.items.length - 1 }} autres</span>
                </td>
                <td class="px-6 py-4 text-sm font-bold text-[#112830]">{{ order.items?.[0]?.quantity || 0 }}</td>
                <td class="px-6 py-4 text-sm font-black text-[#10b481] whitespace-nowrap">{{ order.total }} Ar</td>
                <td class="px-6 py-4">
                  <span 
                    class="px-3 py-1 rounded-full text-[9px] font-black uppercase tracking-widest"
                    :class="{
                      'bg-yellow-50 text-yellow-600': order.status === 'PENDING',
                      'bg-green-50 text-green-600': order.status === 'CONFIRMED',
                      'bg-blue-50 text-blue-600': order.status === 'DELIVERED',
                    }"
                  >
                    {{ order.status }}
                  </span>
                </td>
                <td class="px-6 py-4 text-right">
                  <button class="p-2 hover:bg-gray-100 rounded-xl transition-colors">
                    <i class="bx bx-dots-vertical-rounded text-xl text-gray-400"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </ClientOnly>
</template>

<script setup lang="ts">
import MarketProductCard from '~/components/marketplace/MarketProductCard.vue';
import { ref, computed } from 'vue';
import { useApi } from "~/composables/useApi";

definePageMeta({ layout: "dashboard" });

const { t: nuxtT } = useI18n();
const t = (key: string) => nuxtT(`dashboard.${key}`);
const { apiFetch } = useApi();

const activeTab = ref<'products' | 'orders'>('products');

// FETCH DATA
const { data: postsData, pending: pendingProducts, refresh: refreshProducts } = await useLazyAsyncData(
  'farmer-products',
  () => apiFetch('/api/marketplace/products/?my_products=true'), 
  { server: false, default: () => [] }
);

const { data: ordersData, pending: pendingOrders } = await useLazyAsyncData(
  'farmer-received-orders',
  () => apiFetch('/api/marketplace/orders/?as_seller=true'),
  { server: false, default: () => [] }
);

const products = computed(() => {
  const data = postsData.value;
  if (Array.isArray(data)) return data;
  if (data && typeof data === 'object' && Array.isArray((data as any).results)) {
    return (data as any).results;
  }
  return [];
});

const orders = computed(() => {
  const data = ordersData.value;
  if (Array.isArray(data)) return data;
  if (data && typeof data === 'object' && Array.isArray((data as any).results)) {
    return (data as any).results;
  }
  return [];
});

const activeProductsCount = computed(() => products.value.filter((p: any) => p.is_active).length);
const totalRevenue = computed(() => {
  if (!Array.isArray(orders.value)) return "0";
  const total = orders.value.reduce((sum: number, o: any) => {
    const price = parseFloat(o.total) || 0;
    return sum + price;
  }, 0);
  return total.toLocaleString();
});

// ACTIONS
function editProduct(post: any) {
  navigateTo(`/farmer/marketplace/edit/${post.id}`);
}
</script>
