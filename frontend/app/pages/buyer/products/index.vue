<template>
  <div class="space-y-8">
    <!-- Header -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <h1 class="text-3xl font-black text-[#112830]">Catalogue des Produits</h1>
        <p class="text-gray-500 font-medium">Découvrez les produits frais de nos coopératives.</p>
      </div>
      <div class="flex gap-3 w-full md:w-auto">
        <div class="relative group flex-1 md:flex-none">
          <i class="bx bx-search absolute left-4 top-1/2 -translate-y-1/2 text-gray-300 group-focus-within:text-[#10b481] transition-colors"></i>
          <input 
            v-model="searchQuery"
            @input="onSearch"
            type="text" 
            placeholder="Rechercher un produit..." 
            class="pl-12 pr-6 py-3 bg-white border border-gray-100 rounded-2xl outline-none focus:ring-2 focus:ring-[#10b481]/50 transition-all text-sm font-medium w-full md:w-64 shadow-sm"
          />
        </div>
      </div>
    </div>

    <!-- Categories Filter (Wrapping) -->
    <div class="flex flex-wrap gap-2 md:gap-3">
      <button 
        @click="selectedCategory = null"
        :class="[!selectedCategory ? 'bg-[#112830] text-white shadow-lg shadow-[#112830]/10' : 'bg-white text-gray-400 hover:bg-gray-50 border-gray-100']"
        class="px-5 py-2.5 md:px-6 md:py-3 rounded-2xl whitespace-nowrap font-black text-[10px] uppercase tracking-widest transition-all border shadow-sm"
      >
        Toutes les catégories
      </button>
      <button 
        v-for="cat in categories" 
        :key="cat.id"
        @click="selectedCategory = cat.id"
        :class="[selectedCategory === cat.id ? 'bg-[#112830] text-white shadow-lg shadow-[#112830]/10' : 'bg-white text-gray-400 hover:bg-gray-50 border-gray-100']"
        class="px-5 py-2.5 md:px-6 md:py-3 rounded-2xl whitespace-nowrap font-black text-[10px] uppercase tracking-widest transition-all border shadow-sm"
      >
        {{ cat.name }}
      </button>
    </div>

    <!-- Products Grid -->
    <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      <div v-for="i in 8" :key="i" class="h-80 bg-white rounded-[2.5rem] border border-gray-100 animate-pulse"></div>
    </div>

    <div v-else-if="products.length === 0" class="bg-white py-24 rounded-[3rem] border border-gray-100 text-center space-y-6 shadow-sm">
      <div class="w-24 h-24 bg-gray-50 rounded-full flex items-center justify-center mx-auto text-gray-200">
        <i class="bx bx-package text-5xl"></i>
      </div>
      <div class="space-y-2">
        <h3 class="text-xl font-black text-[#112830]">Aucun produit trouvé</h3>
        <p class="text-gray-400 max-w-sm mx-auto">Essayez d'ajuster votre recherche ou de changer de catégorie.</p>
      </div>
    </div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      <div 
        v-for="product in products" 
        :key="product.id"
        class="group bg-white rounded-[2.5rem] border border-gray-100 shadow-sm hover:shadow-xl hover:border-[#10b481]/30 transition-all duration-500 overflow-hidden flex flex-col"
      >
        <!-- Card Image -->
        <div 
          @click="navigateTo(`/buyer/products/${product.id}`)"
          class="relative h-60 overflow-hidden bg-gray-50 cursor-pointer"
        >
          <img 
            :src="product.image_url || '/images/placeholder-product.jpg'" 
            class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
          />
          <div class="absolute top-4 left-4 flex gap-2">
            <span v-if="product.stock > 0" class="px-3 py-1 bg-[#112830]/80 backdrop-blur-md text-white rounded-full text-[8px] font-black uppercase tracking-widest shadow-sm">En Stock</span>
            <span v-else class="px-3 py-1 bg-rose-500 text-white rounded-full text-[8px] font-black uppercase tracking-widest shadow-sm">Rupture</span>
          </div>
          <div class="absolute inset-0 bg-gradient-to-t from-[#112830]/40 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
        </div>

        <!-- Card Content -->
        <div class="p-6 flex-1 flex flex-col gap-4">
          <div @click="navigateTo(`/buyer/products/${product.id}`)" class="cursor-pointer space-y-1">
            <p class="text-[9px] font-black text-gray-400 uppercase tracking-[0.2em]">{{ product.category_name || 'Général' }}</p>
            <h3 class="text-lg font-black text-[#112830] group-hover:text-[#10b481] transition-colors line-clamp-1 leading-tight">{{ product.name }}</h3>
          </div>

          <div class="flex items-center justify-between mt-auto pt-4 border-t border-gray-50">
            <div>
              <p class="text-[9px] font-black text-gray-400 uppercase tracking-widest mb-0.5">Prix</p>
              <p class="text-xl font-black text-[#112830]">{{ product.price }} <span class="text-[10px] text-gray-400 ml-0.5">Ar</span></p>
            </div>
            
            <button 
              @click="handleAdd(product)"
              :disabled="product.stock <= 0"
              :class="product.stock > 0 ? 'bg-gray-50 text-[#112830] hover:bg-[#112830] hover:text-white shadow-sm' : 'bg-gray-50 text-gray-200 cursor-not-allowed'"
              class="w-12 h-12 rounded-2xl flex items-center justify-center transition-all hover:-translate-y-1 active:scale-95"
            >
              <i class="bx bx-plus text-xl"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { useMarketplace } from '~/composables/useMarketplace';

definePageMeta({ layout: 'dashboard' });

const { 
  products, categories, cart, loading, 
  fetchProducts, fetchCategories, fetchCart, addToCart 
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
    await fetchCart();
  } catch (err) {
    console.error('Add to cart failed', err);
  }
};

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
