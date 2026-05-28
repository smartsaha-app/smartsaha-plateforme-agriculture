<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8">

    <!-- ===== HEADER ===== -->
    <PageHeader title="Mes ventes">
      <template #subtitle>
        <i class="bx bx-store"></i>
        Gérez vos annonces et stocks en vente sur le marketplace
      </template>
      <template #breadcrumb>
        <NuxtLink to="/farmer/dashboard" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
          <span>Accueil</span>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-gray-400">Marketplace</span>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]"> Produits</span>
      </template>
    </PageHeader>
    <div class="flex justify-end -mt-2 mb-6">
      <NuxtLink
        to="/farmer/marketplace/products/new"
        class="px-5 py-2.5 bg-[#013b28] text-white rounded-xl text-[13px] font-semibold hover:bg-[#10b481] transition-colors shadow-sm flex items-center gap-2"
      >
        <i class="bx bx-plus"></i>
        Mettre en vente
      </NuxtLink>
    </div>

    <!-- ===== SEARCH & FILTERS ===== -->
    <div class="bg-white rounded-2xl border border-gray-100 shadow-sm mb-6 p-3 flex items-center gap-2 overflow-x-auto">

      <!-- Recherche -->
      <div class="flex-1 min-w-[160px] relative">
        <i class="bx bx-search absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-base pointer-events-none"></i>
        <input
          v-model="search"
          type="text"
          placeholder="Rechercher un produit..."
          class="w-full pl-9 pr-8 py-2.5 bg-gray-50 border border-gray-100 rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/30 transition-all font-medium text-[#112830]"
        />
        <button v-if="search" @click="search = ''" class="absolute right-2.5 top-1/2 -translate-y-1/2 text-gray-300 hover:text-gray-500">
          <i class="bx bx-x"></i>
        </button>
      </div>

      <!-- Séparateur vertical -->
      <div class="hidden md:block w-px h-7 bg-gray-100"></div>

      <!-- Catégorie -->
      <div class="relative">
        <i class="bx bx-category absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-sm pointer-events-none"></i>
        <select
          v-model="filterCategory"
          class="pl-8 pr-7 py-2.5 bg-gray-50 border border-gray-100 rounded-xl text-xs font-bold text-[#112830] outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/30 transition-all appearance-none cursor-pointer"
          :class="filterCategory ? 'border-[#10b481]/40 bg-emerald-50 text-[#10b481]' : ''"
        >
          <option value="">Catégorie</option>
          <option v-for="cat in dynamicCategories" :key="cat" :value="cat">{{ cat }}</option>
        </select>
        <i class="bx bx-chevron-down absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none text-xs"></i>
      </div>

      <!-- Statut -->
      <div class="relative">
        <i class="bx bx-toggle-right absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-sm pointer-events-none"></i>
        <select
          v-model="filterStatus"
          class="pl-8 pr-7 py-2.5 bg-gray-50 border border-gray-100 rounded-xl text-xs font-bold text-[#112830] outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/30 transition-all appearance-none cursor-pointer"
          :class="filterStatus ? 'border-[#10b481]/40 bg-emerald-50 text-[#10b481]' : ''"
        >
          <option value="">Statut</option>
          <option value="active">Actifs</option>
          <option value="inactive">Masqués</option>
        </select>
        <i class="bx bx-chevron-down absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none text-xs"></i>
      </div>

      <!-- Tri -->
      <div class="relative">
        <i class="bx bx-sort absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-sm pointer-events-none"></i>
        <select
          v-model="sortBy"
          class="pl-8 pr-7 py-2.5 bg-gray-50 border border-gray-100 rounded-xl text-xs font-bold text-[#112830] outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/30 transition-all appearance-none cursor-pointer"
          :class="sortBy ? 'border-[#10b481]/40 bg-emerald-50 text-[#10b481]' : ''"
        >
          <option value="">Trier</option>
          <option value="name_asc">Nom A → Z</option>
          <option value="name_desc">Nom Z → A</option>
          <option value="price_asc">Prix ↑</option>
          <option value="price_desc">Prix ↓</option>
          <option value="stock_desc">Stock ↓</option>
        </select>
        <i class="bx bx-chevron-down absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none text-xs"></i>
      </div>

      <!-- Reset -->
      <button
        v-if="filterCategory || filterStatus || sortBy || search"
        @click="resetFilters"
        class="flex items-center gap-1 px-3 py-2.5 rounded-xl bg-rose-50 border border-rose-100 text-rose-500 text-xs font-bold hover:bg-rose-100 transition-colors"
      >
        <i class="bx bx-x-circle text-sm"></i>
        Réinitialiser
      </button>

      <!-- Compteur -->
      <span class="ml-auto text-xs font-bold text-gray-400 whitespace-nowrap">
        {{ filteredProducts.length }} produit{{ filteredProducts.length !== 1 ? 's' : '' }}
      </span>
    </div>

    <!-- ===== PRODUCTS GRID ===== -->
    <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-pulse">
      <div v-for="i in 6" :key="i" class="h-80 bg-white rounded-2xl border border-gray-100 shadow-sm"></div>
    </div>

    <div v-else-if="filteredProducts.length === 0" class="bg-white py-24 rounded-2xl border border-gray-100 text-center space-y-6 shadow-sm">
      <div class="w-24 h-24 bg-gray-50 rounded-full flex items-center justify-center mx-auto text-gray-200">
        <i class="bx bx-store text-5xl"></i>
      </div>
      <div class="space-y-2">
        <h3 class="text-xl font-black text-[#112830]">Aucun produit en vente</h3>
        <p class="text-gray-400 max-w-sm mx-auto">Publiez votre premier article pour commencer à vendre sur le marketplace SmartSaha.</p>
      </div>
      <NuxtLink
        to="/farmer/marketplace/products/new"
        class="inline-flex items-center gap-2 px-6 py-3 bg-[#10b481] text-white rounded-xl font-semibold text-[13px] shadow-sm"
      >
        Mettre en vente
      </NuxtLink>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="product in filteredProducts"
        :key="product.id"
        class="group bg-white rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-all duration-300 overflow-hidden flex flex-col"
      >
        <!-- Image -->
        <div class="relative h-48 bg-gray-50 overflow-hidden">
          <img :src="product.image_url" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
          <div class="absolute top-3 left-3 flex gap-2">
            <span
              :class="product.is_active ? 'bg-[#10b481] text-white' : 'bg-rose-500 text-white'"
              class="px-2.5 py-1 rounded-full text-[8px] font-black uppercase tracking-widest"
            >{{ product.is_active ? 'Actif' : 'Masqué' }}</span>
          </div>
          <div class="absolute top-3 right-3">
            <NuxtLink
              :to="`/farmer/marketplace/products/edit/${product.id}`"
              class="w-9 h-9 bg-white/90 backdrop-blur-md rounded-xl flex items-center justify-center text-[#112830] shadow-sm hover:bg-[#013b28] hover:text-white transition-all"
            >
              <i class="bx bx-edit-alt text-base"></i>
            </NuxtLink>
          </div>
        </div>

        <!-- Details -->
        <div class="p-5 flex-1 flex flex-col gap-3">
          <div class="flex justify-between items-start">
            <div>
              <h4 class="text-base font-black text-[#112830] group-hover:text-[#10b481] transition-colors">{{ product.name }}</h4>
              <p class="text-[10px] font-black text-gray-300 uppercase tracking-widest">{{ product.category_name || 'Général' }}</p>
            </div>
            <p class="text-lg font-black text-[#112830]">{{ product.price }} <span class="text-[10px] text-gray-400">Ar</span></p>
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div class="p-3 bg-gray-50 rounded-xl flex items-center gap-2.5">
              <i class="bx bx-package text-lg text-[#10b481]"></i>
              <div>
                <p class="text-[8px] font-black text-gray-400 uppercase tracking-widest leading-none mb-0.5">Stock</p>
                <p class="text-sm font-black text-[#112830] leading-none">{{ product.stock }} {{ product.unit }}</p>
              </div>
            </div>
            <div class="p-3 bg-gray-50 rounded-xl flex items-center gap-2.5">
              <i class="bx bx-cart text-lg text-blue-500"></i>
              <div>
                <p class="text-[8px] font-black text-gray-400 uppercase tracking-widest leading-none mb-0.5">Ventes</p>
                <p class="text-sm font-black text-[#112830] leading-none">{{ product.sales_count || 0 }}</p>
              </div>
            </div>
          </div>

          <div class="mt-auto pt-3 flex gap-2">
            <button @click="toggleStatus(product)" class="flex-1 py-2.5 bg-gray-50 text-gray-400 hover:text-[#112830] rounded-xl font-black text-[9px] uppercase tracking-widest transition-all">
              {{ product.is_active ? 'Désactiver' : 'Activer' }}
            </button>
            <NuxtLink :to="`/farmer/marketplace/products/edit/${product.id}`" class="flex-1 py-2.5 bg-[#013b28] text-white rounded-xl font-black text-[9px] uppercase tracking-widest hover:bg-[#10b481] transition-all text-center">
              Modifier
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useApi } from '~/composables/useApi'

definePageMeta({ layout: 'dashboard' })

const { apiFetch } = useApi()

const products       = ref<any[]>([])
const loading        = ref(true)
const search         = ref('')
const filterCategory = ref('')
const filterStatus   = ref('')
const sortBy         = ref('')

onMounted(async () => {
  try {
    const data = await apiFetch('/api/catalogue/products/?seller=me')
    products.value = data.results || data
  } catch (err) {
    console.error('Erreur chargement produits', err)
  } finally {
    loading.value = false
  }
})

// Catégories déduites dynamiquement des produits chargés
const dynamicCategories = computed(() => {
  const cats = new Set<string>()
  products.value.forEach(p => { if (p.category_name) cats.add(p.category_name) })
  return [...cats].sort()
})

const filteredProducts = computed(() => {
  let list = products.value.filter(p => {
    const q = search.value.toLowerCase()
    const matchSearch   = !q || p.name?.toLowerCase().includes(q) || p.category_name?.toLowerCase().includes(q)
    const matchCategory = !filterCategory.value || p.category_name === filterCategory.value
    const matchStatus   = !filterStatus.value
      || (filterStatus.value === 'active'   &&  p.is_active)
      || (filterStatus.value === 'inactive' && !p.is_active)
    return matchSearch && matchCategory && matchStatus
  })

  if (sortBy.value === 'name_asc')    list = [...list].sort((a, b) => a.name.localeCompare(b.name))
  if (sortBy.value === 'name_desc')   list = [...list].sort((a, b) => b.name.localeCompare(a.name))
  if (sortBy.value === 'price_asc')   list = [...list].sort((a, b) => Number(a.price) - Number(b.price))
  if (sortBy.value === 'price_desc')  list = [...list].sort((a, b) => Number(b.price) - Number(a.price))
  if (sortBy.value === 'stock_desc')  list = [...list].sort((a, b) => Number(b.stock) - Number(a.stock))

  return list
})

function resetFilters() {
  search.value         = ''
  filterCategory.value = ''
  filterStatus.value   = ''
  sortBy.value         = ''
}

const toggleStatus = async (product: any) => {
  try {
    await apiFetch(`/api/catalogue/products/${product.id}/`, {
      method: 'PATCH',
      body: { is_active: !product.is_active },
    })
    product.is_active = !product.is_active
  } catch (err) {
    console.error('Erreur toggle statut', err)
  }
}
</script>