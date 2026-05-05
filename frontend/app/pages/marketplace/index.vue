<template>
  <div class="min-h-screen bg-gray-50/50">
    <!-- Header Hero -->
    <div class="bg-[#112830] text-white pt-24 pb-16 px-6 relative overflow-hidden">
      <div class="max-w-[1400px] mx-auto relative z-10">
        <div class="flex flex-col md:flex-row justify-between items-end gap-8">
          <div class="space-y-4 max-w-2xl">
            <span class="inline-block px-4 py-1.5 bg-[#10b481]/20 text-[#10b481] rounded-full text-[10px] font-black uppercase tracking-[0.2em] border border-[#10b481]/30">Marketplace Directe</span>
            <h1 class="text-4xl md:text-6xl font-black leading-tight">De la terre à votre panier.</h1>
            <p class="text-white/60 text-lg font-medium leading-relaxed">Explorez les meilleurs produits des coopératives locales. Fraîcheur garantie et prix justes pour nos agriculteurs.</p>
          </div>
          
          <!-- Search Bar -->
          <div class="w-full md:w-96 relative group">
            <i class="bx bx-search absolute left-5 top-1/2 -translate-y-1/2 text-white/30 text-xl group-focus-within:text-[#10b481] transition-colors"></i>
            <input 
              v-model="searchQuery"
              @input="onSearch"
              type="text" 
              placeholder="Rechercher un produit..." 
              class="w-full pl-14 pr-6 py-5 bg-white/5 border border-white/10 rounded-3xl outline-none focus:ring-2 focus:ring-[#10b481]/50 focus:bg-white/10 transition-all text-sm font-medium backdrop-blur-md"
            />
          </div>
        </div>
      </div>
      
      <!-- Background Elements -->
      <div class="absolute top-[-10%] right-[-5%] w-96 h-96 bg-[#10b481] rounded-full blur-[120px] opacity-20"></div>
      <div class="absolute bottom-[-20%] left-[10%] w-64 h-64 bg-blue-500 rounded-full blur-[100px] opacity-10"></div>
    </div>

    <div class="max-w-[1400px] mx-auto px-6 py-12 -mt-8 relative z-20">
      <!-- Categories Bar -->
      <div class="flex gap-4 overflow-x-auto pb-8 no-scrollbar">
        <button 
          @click="selectedCategory = null"
          :class="[!selectedCategory ? 'bg-[#10b481] text-white shadow-lg shadow-[#10b481]/20' : 'bg-white text-gray-400 hover:bg-gray-100']"
          class="px-8 py-4 rounded-2xl whitespace-nowrap font-black text-xs uppercase tracking-widest transition-all"
        >
          Tous les produits
        </button>
        <button 
          v-for="cat in categories" 
          :key="cat.id"
          @click="selectedCategory = cat.id"
          :class="[selectedCategory === cat.id ? 'bg-[#10b481] text-white shadow-lg shadow-[#10b481]/20' : 'bg-white text-gray-400 hover:bg-gray-100']"
          class="px-8 py-4 rounded-2xl whitespace-nowrap font-black text-xs uppercase tracking-widest transition-all border border-gray-100"
        >
          {{ cat.name }}
        </button>
      </div>

      <!-- Main Content -->
      <div class="flex flex-col lg:flex-row gap-10">
        <!-- Products Grid -->
        <div class="flex-1 space-y-10">
          <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6 animate-pulse">
            <div v-for="i in 6" :key="i" class="h-[400px] bg-white rounded-3xl border border-gray-100"></div>
          </div>

          <div v-else-if="products.length === 0" class="py-20 text-center bg-white rounded-[3rem] border border-gray-100">
            <i class="bx bx-package text-6xl text-gray-200 mb-4"></i>
            <h3 class="text-xl font-black text-[#112830]">Aucun produit trouvé</h3>
            <p class="text-gray-400">Essayez une autre recherche ou catégorie.</p>
          </div>

          <div v-else class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
            <MarketProductCard 
              v-for="product in products" 
              :key="product.id" 
              :product="product"
              @add-to-cart="handleAdd"
            />
          </div>
        </div>

        <!-- Sidebar Cart Summary (Sticky) -->
        <div class="w-full lg:w-96 space-y-6 lg:sticky lg:top-24 h-fit">
          <div class="bg-white rounded-[2.5rem] border border-gray-100 p-8 shadow-sm">
            <div class="flex items-center justify-between mb-8">
              <h3 class="text-xl font-black text-[#112830]">Votre Panier</h3>
              <div class="w-10 h-10 rounded-xl bg-emerald-50 text-[#10b481] flex items-center justify-center font-bold relative">
                <i class="bx bx-shopping-bag text-xl"></i>
                <span v-if="cart?.items_count" class="absolute -top-2 -right-2 w-5 h-5 bg-[#10b481] text-white text-[10px] flex items-center justify-center rounded-full border-2 border-white">
                  {{ cart.items_count }}
                </span>
              </div>
            </div>

            <!-- Cart Items List -->
            <div v-if="cart?.items?.length" class="space-y-4 mb-8 max-h-[400px] overflow-y-auto pr-2 no-scrollbar">
              <div v-for="item in cart.items" :key="item.id" class="flex items-center gap-4 group">
                <div class="w-14 h-14 rounded-2xl bg-gray-50 flex-shrink-0 overflow-hidden">
                  <img v-if="item.product_image" :src="item.product_image" class="w-full h-full object-cover" />
                  <div v-else class="w-full h-full flex items-center justify-center text-gray-300">
                    <i class="bx bx-image"></i>
                  </div>
                </div>
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-black text-[#112830] truncate">{{ item.product_name }}</p>
                  <p class="text-[10px] font-bold text-gray-400">{{ item.quantity }} x {{ item.price }} Ar</p>
                </div>
                <button @click="handleRemove(item.id)" class="w-8 h-8 rounded-lg hover:bg-rose-50 hover:text-rose-500 text-gray-300 flex items-center justify-center transition-all">
                  <i class="bx bx-trash text-lg"></i>
                </button>
              </div>
            </div>

            <div v-else class="py-12 text-center text-gray-400 text-sm italic border-b border-gray-50 mb-8">
              Votre panier est vide.
            </div>

            <!-- Totals -->
            <div class="space-y-4 pt-6 border-t border-gray-50">
              <div class="flex justify-between items-center text-sm">
                <span class="text-gray-400 font-bold">Sous-total</span>
                <span class="text-[#112830] font-black">{{ cart?.total || 0 }} Ar</span>
              </div>
              <div class="flex justify-between items-center text-lg">
                <span class="text-[#112830] font-black">Total</span>
                <span class="text-[#10b481] font-black">{{ cart?.total || 0 }} Ar</span>
              </div>
            </div>

            <button 
              @click="goToCheckout"
              :disabled="!cart?.items?.length"
              class="w-full py-5 bg-[#112830] hover:bg-[#10b481] disabled:bg-gray-100 disabled:text-gray-300 text-white rounded-2xl font-black text-xs uppercase tracking-widest transition-all mt-8 shadow-xl shadow-[#112830]/10 flex items-center justify-center gap-3"
            >
              Passer la commande
              <i class="bx bx-right-arrow-alt text-xl"></i>
            </button>
          </div>

          <!-- Promo Banner -->
          <div class="bg-gradient-to-br from-[#10b481] to-[#0a8f6e] p-8 rounded-[2.5rem] text-white relative overflow-hidden group cursor-pointer">
            <div class="relative z-10">
              <h4 class="text-lg font-black leading-tight mb-2">Devenir Vendeur ?</h4>
              <p class="text-white/70 text-xs font-medium mb-4">Rejoignez notre réseau de 500+ agriculteurs certifiés.</p>
              <span class="text-[10px] font-black uppercase tracking-widest border-b border-white/30 group-hover:border-white transition-all">En savoir plus</span>
            </div>
            <i class="bx bx-leaf absolute bottom-[-20%] right-[-10%] text-white/10 text-[8rem] group-hover:scale-110 transition-transform"></i>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { useMarketplace } from '~/composables/useMarketplace';
import MarketProductCard from '~/components/marketplace/MarketProductCard.vue';

definePageMeta({ layout: 'dashboard' });

const { 
  products, categories, cart, loading, 
  fetchProducts, fetchCategories, fetchCart, addToCart, removeFromCart 
} = useMarketplace();

const searchQuery = ref('');
const selectedCategory = ref<number | null>(null);

const onSearch = debounce(() => {
  fetchProducts({ search: searchQuery.value, category: selectedCategory.value });
}, 500);

watch(selectedCategory, (newVal) => {
  fetchProducts({ search: searchQuery.value, category: newVal });
});

onMounted(async () => {
  await Promise.all([
    fetchProducts(),
    fetchCategories(),
    fetchCart()
  ]);
});

const handleAdd = async (product: any) => {
  try {
    await addToCart(product.id);
    // Optionnel: Notification succès
  } catch (err) {
    console.error('Add to cart failed', err);
  }
};

const handleRemove = async (itemId: number) => {
  try {
    await removeFromCart(itemId);
  } catch (err) {
    console.error('Remove from cart failed', err);
  }
};

const goToCheckout = () => {
  navigateTo('/marketplace/checkout');
};

// Simple debounce helper
function debounce(fn: Function, delay: number) {
  let timeout: any;
  return (...args: any[]) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn(...args), delay);
  };
}
</script>

<style scoped>
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>