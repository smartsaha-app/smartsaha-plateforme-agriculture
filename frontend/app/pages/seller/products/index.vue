<template>
  <div class="space-y-8 pb-20">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-3xl font-black text-[#112830]">Mes Produits</h1>
        <p class="text-gray-500 font-medium">Gérez votre catalogue et vos stocks en temps réel.</p>
      </div>
      <button @click="navigateTo('/seller/products/new')" class="px-6 py-3 bg-[#112830] text-white rounded-2xl font-black text-[10px] uppercase tracking-widest shadow-lg shadow-[#112830]/10 hover:bg-[#10b481] transition-all flex items-center gap-2">
        <i class="bx bx-plus text-lg"></i>
        Ajouter un produit
      </button>
    </div>

    <!-- Filters & Search -->
    <div class="flex flex-wrap gap-4 items-center bg-white p-4 rounded-3xl border border-gray-50 shadow-sm">
      <div class="flex-1 min-w-[200px] relative">
        <i class="bx bx-search absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 text-xl"></i>
        <input v-model="search" type="text" placeholder="Rechercher un produit..." class="w-full pl-12 pr-4 py-3 bg-gray-50 border-none rounded-2xl focus:ring-2 focus:ring-[#10b481]/20 outline-none font-medium text-sm text-[#112830]">
      </div>
      <div class="flex gap-2">
        <button v-for="cat in categories" :key="cat" @click="filterCategory = cat" :class="filterCategory === cat ? 'bg-[#10b481] text-white' : 'bg-gray-50 text-gray-400'" class="px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all">
          {{ cat }}
        </button>
      </div>
    </div>

    <!-- Products Grid -->
    <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-pulse">
      <div v-for="i in 6" :key="i" class="h-80 bg-white rounded-[2.5rem] border border-gray-50 shadow-sm"></div>
    </div>

    <div v-else-if="filteredProducts.length === 0" class="bg-white py-24 rounded-[3rem] border border-gray-100 text-center space-y-6 shadow-sm">
      <div class="w-24 h-24 bg-gray-50 rounded-full flex items-center justify-center mx-auto text-gray-200">
        <i class="bx bx-store text-5xl"></i>
      </div>
      <div class="space-y-2">
        <h3 class="text-xl font-black text-[#112830]">Aucun produit trouvé</h3>
        <p class="text-gray-400 max-w-sm mx-auto">Vous n'avez pas encore de produits correspondant à cette recherche.</p>
      </div>
      <button @click="navigateTo('/seller/products/new')" class="inline-flex items-center gap-2 px-8 py-4 bg-[#10b481] text-white rounded-2xl font-black text-xs uppercase tracking-widest shadow-lg shadow-[#10b481]/20 hover:scale-105 transition-all">
        Créer mon premier produit
      </button>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      <div v-for="product in filteredProducts" :key="product.id" class="group bg-white rounded-[2.5rem] border border-gray-50 shadow-sm hover:shadow-xl transition-all duration-500 overflow-hidden flex flex-col">
        <!-- Product Image -->
        <div class="relative h-48 bg-gray-50 overflow-hidden">
          <img :src="product.image_url" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700" />
          <div class="absolute top-4 left-4 flex gap-2">
            <span :class="product.is_active ? 'bg-[#10b481] text-white' : 'bg-rose-500 text-white'" class="px-3 py-1 rounded-full text-[8px] font-black uppercase tracking-widest shadow-sm">
              {{ product.is_active ? 'Actif' : 'Masqué' }}
            </span>
          </div>
          <div class="absolute top-4 right-4">
             <button @click="navigateTo('/seller/products/edit/' + product.id)" class="w-10 h-10 bg-white/90 backdrop-blur-md rounded-xl flex items-center justify-center text-[#112830] shadow-sm hover:bg-[#112830] hover:text-white transition-all">
               <i class="bx bx-edit-alt text-lg"></i>
             </button>
          </div>
        </div>

        <!-- Product Details -->
        <div class="p-6 flex-1 flex flex-col gap-4">
          <div class="flex justify-between items-start">
            <div>
              <h4 class="text-lg font-black text-[#112830] group-hover:text-[#10b481] transition-colors">{{ product.name }}</h4>
              <p class="text-[10px] font-black text-gray-300 uppercase tracking-widest">{{ product.category_name || 'Général' }}</p>
            </div>
            <p class="text-xl font-black text-[#112830]">{{ product.price }} <span class="text-[10px] text-gray-400 uppercase">Ar</span></p>
          </div>

          <div class="grid grid-cols-2 gap-4 py-2">
            <div class="p-3 bg-gray-50 rounded-2xl flex items-center gap-3">
              <i class="bx bx-package text-xl text-[#10b481]"></i>
              <div>
                <p class="text-[8px] font-black text-gray-400 uppercase tracking-widest leading-none mb-1">Stock</p>
                <p class="text-sm font-black text-[#112830] leading-none">{{ product.stock }} {{ product.unit }}</p>
              </div>
            </div>
            <div class="p-3 bg-gray-50 rounded-2xl flex items-center gap-3">
              <i class="bx bx-cart text-xl text-blue-500"></i>
              <div>
                <p class="text-[8px] font-black text-gray-400 uppercase tracking-widest leading-none mb-1">Ventes</p>
                <p class="text-sm font-black text-[#112830] leading-none">{{ product.sales_count || 0 }}</p>
              </div>
            </div>
          </div>

          <div class="mt-auto pt-4 flex gap-2">
            <button @click="toggleStatus(product)" class="flex-1 py-3 bg-gray-50 text-gray-400 hover:text-[#112830] rounded-xl font-black text-[9px] uppercase tracking-widest transition-all">
              {{ product.is_active ? 'Désactiver' : 'Activer' }}
            </button>
            <button @click="navigateTo(`/seller/products/edit/${product.id}`)" class="flex-1 py-3 bg-[#112830] text-white rounded-xl font-black text-[9px] uppercase tracking-widest hover:bg-[#10b481] transition-all">
              Détails
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';

definePageMeta({
  layout: 'dashboard'
});

const { apiFetch } = useApi();

const products = ref<any[]>([]);
const loading = ref(true);
const search = ref('');
const filterCategory = ref('Tous');
const categories = ['Tous', 'Agriculture', 'Matériel', 'Semences', 'Engrais'];

onMounted(async () => {
  try {
    const data = await apiFetch('/api/catalogue/products/?seller=me');
    products.value = data.results || data;
  } catch (err) {
    console.error('Failed to load products', err);
  } finally {
    loading.value = false;
  }
});

const filteredProducts = computed(() => {
  return products.value.filter(p => {
    const matchSearch = p.name.toLowerCase().includes(search.value.toLowerCase());
    const matchCat = filterCategory.value === 'Tous' || p.category_name === filterCategory.value;
    return matchSearch && matchCat;
  });
});

const toggleStatus = async (product: any) => {
  try {
    await apiFetch(`/api/catalogue/products/${product.id}/`, {
      method: 'PATCH',
      body: { is_active: !product.is_active }
    });
    product.is_active = !product.is_active;
  } catch (err) {
    console.error('Failed to toggle status', err);
  }
};
</script>
