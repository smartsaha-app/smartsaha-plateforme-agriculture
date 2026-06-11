<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8 space-y-6">

    <!-- ===== HEADER ===== -->
    <PageHeader :title="t('buyer.productsTitle')">
      <template #subtitle>
        <i class="bx bx-store"></i>
        {{ t('buyer.productsDesc') }}
      </template>
      <template #breadcrumb>
        <NuxtLink to="/buyer/dashboard" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
          <span>Accueil</span>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">Produits</span>
      </template>
    </PageHeader>

    <!-- ===== FILTERS BAR ===== -->
    <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-3 flex items-center gap-2 overflow-x-auto">
      <!-- Recherche -->
      <div class="flex-1 min-w-[160px] relative">
        <i class="bx bx-search absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-base pointer-events-none"></i>
        <input v-model="searchQuery" type="text" :placeholder="t('seller.searchProduct')"
          class="w-full pl-9 pr-8 py-2.5 bg-gray-50 border border-gray-100 rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/30 transition-all font-medium text-[#112830]" />
        <button v-if="searchQuery" @click="searchQuery = ''" class="absolute right-2.5 top-1/2 -translate-y-1/2 text-gray-300 hover:text-gray-500">
          <i class="bx bx-x"></i>
        </button>
      </div>

      <div class="hidden md:block w-px h-7 bg-gray-100 flex-shrink-0"></div>

      <!-- Catégorie -->
      <div class="relative flex-shrink-0">
        <i class="bx bx-category absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-sm pointer-events-none"></i>
        <select v-model="selectedCategory"
          class="pl-8 pr-7 py-2.5 bg-gray-50 border border-gray-100 rounded-xl text-xs font-bold text-[#112830] outline-none focus:ring-2 focus:ring-[#10b481]/20 appearance-none cursor-pointer transition-all"
          :class="selectedCategory ? 'border-[#10b481]/40 bg-emerald-50 text-[#10b481]' : ''">
          <option :value="null">{{ t('buyer.allCategories') }}</option>
          <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
        </select>
        <i class="bx bx-chevron-down absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none text-xs"></i>
      </div>

      <!-- Tri -->
      <div class="relative flex-shrink-0">
        <i class="bx bx-sort absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-sm pointer-events-none"></i>
        <select v-model="sortBy"
          class="pl-8 pr-7 py-2.5 bg-gray-50 border border-gray-100 rounded-xl text-xs font-bold text-[#112830] outline-none focus:ring-2 focus:ring-[#10b481]/20 appearance-none cursor-pointer transition-all"
          :class="sortBy ? 'border-[#10b481]/40 bg-emerald-50 text-[#10b481]' : ''">
          <option value="">{{ t('seller.sortLabel') }}</option>
          <option value="price_asc">{{ t('buyer.sortPriceAsc') }}</option>
          <option value="price_desc">{{ t('buyer.sortPriceDesc') }}</option>
          <option value="name_asc">{{ t('buyer.sortNameAsc') }}</option>
          <option value="stock_desc">{{ t('buyer.sortStockDesc') }}</option>
        </select>
        <i class="bx bx-chevron-down absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none text-xs"></i>
      </div>

      <!-- Reset -->
      <button v-if="searchQuery || selectedCategory || sortBy" @click="resetFilters"
        class="flex items-center gap-1 px-3 py-2.5 rounded-xl bg-rose-50 border border-rose-100 text-rose-500 text-xs font-bold hover:bg-rose-100 transition-colors flex-shrink-0">
        <i class="bx bx-x-circle text-sm"></i>
        Réinitialiser
      </button>

      <span class="ml-auto text-xs font-bold text-gray-400 whitespace-nowrap flex-shrink-0">
        {{ displayedProducts.length }} produit{{ displayedProducts.length !== 1 ? 's' : '' }}
      </span>
    </div>

    <!-- ===== LOADING ===== -->
    <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
      <div v-for="i in 8" :key="i" class="h-72 bg-white rounded-2xl border border-gray-100 animate-pulse"></div>
    </div>

    <!-- ===== EMPTY ===== -->
    <div v-else-if="displayedProducts.length === 0" class="bg-white py-20 rounded-2xl border border-gray-100 text-center space-y-5 shadow-sm">
      <div class="w-20 h-20 bg-gray-50 rounded-2xl flex items-center justify-center mx-auto">
        <i class="bx bx-package text-4xl text-gray-200"></i>
      </div>
      <div>
        <h3 class="text-base font-black text-[#112830]">Aucun produit trouvé</h3>
        <p class="text-sm text-gray-400 mt-1">Essayez d'ajuster votre recherche ou vos filtres.</p>
      </div>
    </div>

    <!-- ===== GRID ===== -->
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
      <div v-for="product in displayedProducts" :key="product.id"
        class="group bg-white rounded-2xl border border-gray-100 shadow-sm hover:shadow-lg hover:border-[#10b481]/20 transition-all duration-300 overflow-hidden flex flex-col">

        <!-- Image -->
        <div @click="navigateTo(`/buyer/products/${product.id}`)"
          class="relative h-48 overflow-hidden bg-gray-50 cursor-pointer">
          <img :src="product.image_url || '/images/placeholder-product.jpg'"
            class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
          <div class="absolute top-3 left-3">
            <span v-if="product.stock > 0"
              class="px-2.5 py-1 bg-[#112830]/75 backdrop-blur-sm text-white rounded-full text-[8px] font-black uppercase tracking-widest">
              En Stock
            </span>
            <span v-else class="px-2.5 py-1 bg-rose-500 text-white rounded-full text-[8px] font-black uppercase tracking-widest">
              Rupture
            </span>
          </div>
        </div>

        <!-- Content -->
        <div class="p-4 flex-1 flex flex-col gap-3">
          <div @click="navigateTo(`/buyer/products/${product.id}`)" class="cursor-pointer space-y-0.5">
            <p class="text-[9px] font-black text-gray-400 uppercase tracking-widest">{{ product.category_name || 'Général' }}</p>
            <h3 class="text-sm font-black text-[#112830] group-hover:text-[#10b481] transition-colors line-clamp-2 leading-tight">
              {{ product.name }}
            </h3>
          </div>

          <div class="flex items-center justify-between mt-auto pt-3 border-t border-gray-50">
            <div>
              <p class="text-[9px] font-black text-gray-400 uppercase tracking-widest mb-0.5">Prix</p>
              <p class="text-lg font-black text-[#112830]">{{ product.price }} <span class="text-[9px] text-gray-400">Ar / {{ product.unit }}</span></p>
            </div>
            <button @click="handleAdd(product)" :disabled="product.stock <= 0 || addingId === product.id"
              :class="product.stock > 0 ? 'bg-[#112830] text-white hover:bg-[#10b481] shadow-sm' : 'bg-gray-100 text-gray-300 cursor-not-allowed'"
              class="w-10 h-10 rounded-xl flex items-center justify-center transition-all hover:-translate-y-0.5 disabled:hover:translate-y-0">
              <div v-if="addingId === product.id" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              <i v-else class="bx bx-plus text-lg"></i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- ===== TOAST ===== -->
    <transition name="slide-up">
      <div v-if="toast.visible"
        class="fixed bottom-6 left-1/2 -translate-x-1/2 z-[100] px-5 py-3 rounded-2xl shadow-xl flex items-center gap-3 text-sm font-bold bg-[#112830] text-white">
        <i class="bx bx-check-circle text-[#10b481] text-lg"></i>
        {{ toast.message }}
      </div>
    </transition>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useMarketplace } from '~/composables/useMarketplace';

const { t } = useI18n();
definePageMeta({ layout: 'dashboard' });

const { products, categories, loading, fetchProducts, fetchCategories, fetchCart, addToCart } = useMarketplace();

const searchQuery      = ref('');
const selectedCategory = ref<number | null>(null);
const sortBy           = ref('');
const addingId         = ref<number | null>(null);
const toast = ref({ visible: false, message: '' });

// Catégorie sélectionnée → nom pour filtrer côté client
const selectedCategoryName = computed(() => {
  if (!selectedCategory.value) return null;
  return (categories.value || []).find((c: any) => c.id === selectedCategory.value)?.name ?? null;
});

// Tout le filtrage et tri est côté client sur les produits déjà chargés
const displayedProducts = computed(() => {
  let list = [...(products.value || [])];

  // Filtre texte
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.trim().toLowerCase();
    list = list.filter(p =>
      p.name?.toLowerCase().includes(q) ||
      p.category_name?.toLowerCase().includes(q) ||
      p.description?.toLowerCase().includes(q)
    );
  }

  // Filtre catégorie
  if (selectedCategoryName.value) {
    list = list.filter(p => p.category_name === selectedCategoryName.value);
  }

  // Tri
  if (sortBy.value === 'price_asc')  list = [...list].sort((a, b) => Number(a.price) - Number(b.price));
  if (sortBy.value === 'price_desc') list = [...list].sort((a, b) => Number(b.price) - Number(a.price));
  if (sortBy.value === 'name_asc')   list = [...list].sort((a, b) => a.name.localeCompare(b.name));
  if (sortBy.value === 'stock_desc') list = [...list].sort((a, b) => Number(b.stock) - Number(a.stock));

  return list;
});

// Les handlers de la barre de filtre ne font rien d'explicite —
// tout est réactif via le computed ci-dessus
function onSearch() { /* réactif via displayedProducts */ }
function onCategoryChange() { /* réactif via displayedProducts */ }
function applySort()  { /* réactif via displayedProducts */ }

function resetFilters() {
  searchQuery.value = '';
  selectedCategory.value = null;
  sortBy.value = '';
}

function showToast(msg: string) {
  toast.value = { visible: true, message: msg };
  setTimeout(() => (toast.value.visible = false), 2500);
}

onMounted(async () => {
  await Promise.all([fetchProducts(), fetchCategories(), fetchCart()]);
});

async function handleAdd(product: any) {
  addingId.value = product.id;
  try {
    await addToCart(product.id);
    await fetchCart();
    showToast(`"${product.name}" ajouté au panier !`);
  } catch (err) {
    console.error('Add to cart failed', err);
  } finally {
    addingId.value = null;
  }
}
</script>

<style scoped>
.slide-up-enter-active, .slide-up-leave-active { transition: all 0.3s ease; }
.slide-up-enter-from, .slide-up-leave-to { opacity: 0; transform: translate(-50%, 1rem); }
</style>