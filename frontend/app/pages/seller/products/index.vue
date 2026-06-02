<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8 space-y-6">

    <!-- ===== HEADER ===== -->
    <PageHeader :title="t('seller.productsTitle')">
      <template #subtitle>
        <i class="bx bx-store"></i>
        {{ t('seller.productsDesc') }}
      </template>
      <template #breadcrumb>
        <NuxtLink to="/seller/dashboard" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
          <span>{{ t('dashboard.home') }}</span>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">{{ t('dashboard.myProducts') }}</span>
      </template>
    </PageHeader>

    <div class="flex justify-end -mt-2">
      <NuxtLink to="/seller/products/new"
        class="flex items-center gap-2 px-4 py-2.5 bg-[#112830] text-white rounded-xl text-sm font-bold hover:bg-[#10b481] transition-all shadow-sm">
        <i class="bx bx-plus text-base"></i>
        {{ t('seller.addProduct') }}
      </NuxtLink>
    </div>

    <!-- ===== FILTERS ===== -->
    <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-3 flex items-center gap-2 overflow-x-auto">
      <!-- Recherche -->
      <div class="flex-1 min-w-[160px] relative">
        <i class="bx bx-search absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-base pointer-events-none"></i>
        <input v-model="search" type="text" :placeholder="t('seller.searchProduct')"
          class="w-full pl-9 pr-8 py-2.5 bg-gray-50 border border-gray-100 rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/30 transition-all font-medium text-[#112830]" />
        <button v-if="search" @click="search = ''" class="absolute right-2.5 top-1/2 -translate-y-1/2 text-gray-300 hover:text-gray-500">
          <i class="bx bx-x"></i>
        </button>
      </div>

      <div class="hidden md:block w-px h-7 bg-gray-100 flex-shrink-0"></div>

      <!-- Catégorie -->
      <div class="relative flex-shrink-0">
        <i class="bx bx-category absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-sm pointer-events-none"></i>
        <select v-model="filterCategory"
          class="pl-8 pr-7 py-2.5 bg-gray-50 border border-gray-100 rounded-xl text-xs font-bold text-[#112830] outline-none focus:ring-2 focus:ring-[#10b481]/20 appearance-none cursor-pointer transition-all"
          :class="filterCategory ? 'border-[#10b481]/40 bg-emerald-50 text-[#10b481]' : ''">
          <option value="">{{ t('seller.category') }}</option>
          <option v-for="cat in dynamicCategories" :key="cat" :value="cat">{{ cat }}</option>
        </select>
        <i class="bx bx-chevron-down absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none text-xs"></i>
      </div>

      <!-- Statut -->
      <div class="relative flex-shrink-0">
        <i class="bx bx-toggle-right absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-sm pointer-events-none"></i>
        <select v-model="filterStatus"
          class="pl-8 pr-7 py-2.5 bg-gray-50 border border-gray-100 rounded-xl text-xs font-bold text-[#112830] outline-none focus:ring-2 focus:ring-[#10b481]/20 appearance-none cursor-pointer transition-all"
          :class="filterStatus ? 'border-[#10b481]/40 bg-emerald-50 text-[#10b481]' : ''">
          <option value="">{{ t('dashboard.status') }}</option>
          <option value="active">{{ t('seller.filterActive') }}</option>
          <option value="inactive">{{ t('seller.filterInactive') }}</option>
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
          <option value="name_asc">{{ t('seller.sortName_asc') }}</option>
          <option value="name_desc">{{ t('seller.sortName_desc') }}</option>
          <option value="price_asc">{{ t('seller.sortPrice_asc') }}</option>
          <option value="price_desc">{{ t('seller.sortPrice_desc') }}</option>
          <option value="stock_desc">{{ t('seller.sortStock_desc') }}</option>
        </select>
        <i class="bx bx-chevron-down absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none text-xs"></i>
      </div>

      <!-- Reset -->
      <button v-if="search || filterCategory || filterStatus || sortBy" @click="resetFilters"
        class="flex items-center gap-1 px-3 py-2.5 rounded-xl bg-rose-50 border border-rose-100 text-rose-500 text-xs font-bold hover:bg-rose-100 transition-colors flex-shrink-0">
        <i class="bx bx-x-circle text-sm"></i>
        {{ t('seller.reset') }}
      </button>

      <span class="ml-auto text-xs font-bold text-gray-400 whitespace-nowrap flex-shrink-0">
        {{ filteredProducts.length }} produit{{ filteredProducts.length !== 1 ? 's' : '' }}
      </span>
    </div>

    <!-- ===== LOADING ===== -->
    <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="i in 6" :key="i" class="h-72 bg-white rounded-2xl border border-gray-100 animate-pulse"></div>
    </div>

    <!-- ===== EMPTY ===== -->
    <div v-else-if="filteredProducts.length === 0" class="bg-white py-24 rounded-2xl border border-gray-100 text-center space-y-5 shadow-sm">
      <div class="w-20 h-20 bg-gray-50 rounded-2xl flex items-center justify-center mx-auto">
        <i class="bx bx-store text-4xl text-gray-200"></i>
      </div>
      <div>
        <h3 class="text-base font-black text-[#112830]">
          {{ search || filterCategory || filterStatus ? t('seller.noResults') : t('seller.noProducts') }}
        </h3>
        <p class="text-sm text-gray-400 mt-1 max-w-xs mx-auto">
          {{ search || filterCategory || filterStatus ? t('seller.noResultsDesc') : t('seller.noProductsDesc') }}
        </p>
      </div>
      <NuxtLink v-if="!search && !filterCategory && !filterStatus" to="/seller/products/new"
        class="inline-flex items-center gap-2 px-5 py-2.5 bg-[#112830] text-white rounded-xl font-bold text-sm hover:bg-[#10b481] transition-all shadow-sm">
        <i class="bx bx-plus"></i>
        {{ t('seller.createProduct') }}
      </NuxtLink>
    </div>

    <!-- ===== GRID ===== -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="product in filteredProducts" :key="product.id"
        class="group bg-white rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-all duration-300 overflow-hidden flex flex-col">

        <!-- Image -->
        <div class="relative h-44 bg-gray-50 overflow-hidden">
          <img :src="product.image_url" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
          <div class="absolute top-3 left-3">
            <span :class="product.is_active ? 'bg-[#10b481] text-white' : 'bg-rose-500 text-white'"
              class="px-2.5 py-1 rounded-full text-[8px] font-black uppercase tracking-widest">
              {{ product.is_active ? t('seller.statusActive') : t('seller.statusHidden') }}
            </span>
          </div>
          <div class="absolute top-3 right-3 flex gap-1.5">
            <NuxtLink :to="`/seller/products/edit/${product.id}`"
              class="w-8 h-8 bg-white/90 backdrop-blur-sm rounded-lg flex items-center justify-center text-[#112830] hover:bg-[#112830] hover:text-white transition-all shadow-sm">
              <i class="bx bx-edit-alt text-sm"></i>
            </NuxtLink>
            <button @click.stop="openDeleteModal(product)"
              class="w-8 h-8 bg-white/90 backdrop-blur-sm rounded-lg flex items-center justify-center text-rose-400 hover:bg-rose-500 hover:text-white transition-all shadow-sm">
              <i class="bx bx-trash text-sm"></i>
            </button>
          </div>
        </div>

        <!-- Infos -->
        <div class="p-5 flex-1 flex flex-col gap-3">
          <div class="flex justify-between items-start">
            <div class="min-w-0">
              <h4 class="text-sm font-black text-[#112830] group-hover:text-[#10b481] transition-colors truncate">{{ product.name }}</h4>
              <p class="text-[9px] font-black text-gray-300 uppercase tracking-widest">{{ product.category_name || 'Général' }}</p>
            </div>
            <p class="text-base font-black text-[#112830] flex-shrink-0 ml-2">{{ product.price }} <span class="text-[9px] text-gray-400">Ar</span></p>
          </div>

          <div class="grid grid-cols-2 gap-2">
            <div class="p-2.5 bg-gray-50 rounded-xl flex items-center gap-2">
              <i class="bx bx-package text-[#10b481] text-base"></i>
              <div>
                <p class="text-[7px] font-black text-gray-400 uppercase tracking-widest leading-none">{{ t('seller.stock') }}</p>
                <p class="text-xs font-black text-[#112830]">{{ product.stock }} {{ product.unit }}</p>
              </div>
            </div>
            <div class="p-2.5 bg-gray-50 rounded-xl flex items-center gap-2">
              <i class="bx bx-cart text-blue-500 text-base"></i>
              <div>
                <p class="text-[7px] font-black text-gray-400 uppercase tracking-widest leading-none">{{ t('seller.sales') }}</p>
                <p class="text-xs font-black text-[#112830]">{{ product.sales_count || 0 }}</p>
              </div>
            </div>
          </div>

          <div class="mt-auto flex gap-2">
            <button @click="toggleStatus(product)"
              class="flex-1 py-2 bg-gray-50 border border-gray-100 text-gray-400 hover:text-[#112830] rounded-xl font-black text-[9px] uppercase tracking-widest transition-all hover:bg-gray-100">
              {{ product.is_active ? t('seller.deactivate') : t('seller.activate') }}
            </button>
            <NuxtLink :to="`/seller/products/edit/${product.id}`"
              class="flex-1 py-2 bg-[#112830] text-white rounded-xl font-black text-[9px] uppercase tracking-widest hover:bg-[#10b481] transition-all text-center">
              {{ t('seller.editProduct') }}
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>

    <!-- ===== DELETE MODAL ===== -->
    <div v-if="productToDelete" class="fixed inset-0 z-[100] flex items-center justify-center p-6 backdrop-blur-sm bg-black/20">
      <div class="bg-white w-full max-w-sm rounded-2xl p-8 shadow-2xl space-y-5 border border-gray-100">
        <div class="text-center space-y-3">
          <div class="w-14 h-14 bg-rose-50 rounded-2xl flex items-center justify-center mx-auto">
            <i class="bx bx-trash text-2xl text-rose-500"></i>
          </div>
          <div>
            <h2 class="text-base font-black text-[#112830]">{{ t('seller.deleteProduct') }}</h2>
            <p class="text-sm text-gray-400 mt-1">
              "<span class="font-bold text-[#112830]">{{ productToDelete.name }}</span>" {{ t('seller.deleteProductPermanent') }}
            </p>
          </div>
        </div>
        <div class="flex gap-3">
          <button @click="productToDelete = null"
            class="flex-1 py-3 rounded-xl border border-gray-100 text-gray-500 font-bold text-sm hover:bg-gray-50 transition-colors">
            {{ t('dashboard.cancel') }}
          </button>
          <button @click="confirmDelete" :disabled="isDeleting"
            class="flex-1 py-3 rounded-xl bg-rose-500 text-white font-bold text-sm hover:bg-rose-600 transition-colors disabled:opacity-50 flex items-center justify-center gap-2">
            <div v-if="isDeleting" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            <i v-else class="bx bx-trash"></i>
            {{ t('dashboard.delete') }}
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';

definePageMeta({ layout: 'dashboard' });
const { t } = useI18n();

const { apiFetch } = useApi();

const products       = ref<any[]>([]);
const loading        = ref(true);
const search         = ref('');
const filterCategory = ref('');
const filterStatus   = ref('');
const sortBy         = ref('');
const productToDelete = ref<any>(null);
const isDeleting      = ref(false);

onMounted(async () => {
  try {
    const data = await apiFetch('/api/catalogue/products/?seller=me');
    products.value = data.results || data;
  } catch (err) {
    console.error('Erreur chargement produits', err);
  } finally {
    loading.value = false;
  }
});

const dynamicCategories = computed(() => {
  const cats = new Set<string>();
  products.value.forEach(p => { if (p.category_name) cats.add(p.category_name); });
  return [...cats].sort();
});

const filteredProducts = computed(() => {
  let list = products.value.filter(p => {
    const q = search.value.toLowerCase();
    const matchSearch   = !q || p.name?.toLowerCase().includes(q) || p.category_name?.toLowerCase().includes(q);
    const matchCategory = !filterCategory.value || p.category_name === filterCategory.value;
    const matchStatus   = !filterStatus.value
      || (filterStatus.value === 'active'   &&  p.is_active)
      || (filterStatus.value === 'inactive' && !p.is_active);
    return matchSearch && matchCategory && matchStatus;
  });
  if (sortBy.value === 'name_asc')   list = [...list].sort((a, b) => a.name.localeCompare(b.name));
  if (sortBy.value === 'name_desc')  list = [...list].sort((a, b) => b.name.localeCompare(a.name));
  if (sortBy.value === 'price_asc')  list = [...list].sort((a, b) => Number(a.price) - Number(b.price));
  if (sortBy.value === 'price_desc') list = [...list].sort((a, b) => Number(b.price) - Number(a.price));
  if (sortBy.value === 'stock_desc') list = [...list].sort((a, b) => Number(b.stock) - Number(a.stock));
  return list;
});

function resetFilters() {
  search.value = ''; filterCategory.value = ''; filterStatus.value = ''; sortBy.value = '';
}

function openDeleteModal(product: any) { productToDelete.value = product; }

async function confirmDelete() {
  if (!productToDelete.value) return;
  isDeleting.value = true;
  try {
    await apiFetch(`/api/catalogue/products/${productToDelete.value.id}/`, { method: 'DELETE' });
    products.value = products.value.filter(p => p.id !== productToDelete.value.id);
    productToDelete.value = null;
  } catch (err) { console.error('Erreur suppression', err); }
  finally { isDeleting.value = false; }
}

const toggleStatus = async (product: any) => {
  try {
    await apiFetch(`/api/catalogue/products/${product.id}/`, {
      method: 'PATCH', body: { is_active: !product.is_active },
    });
    product.is_active = !product.is_active;
  } catch (err) { console.error('Erreur toggle statut', err); }
};
</script>