<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8 space-y-6">

    <!-- ===== HEADER ===== -->
    <PageHeader :title="product ? product.name : 'Produit'">
      <template #subtitle v-if="product">
        <span class="px-2.5 py-1 bg-gray-50 border border-gray-100 rounded-lg text-[9px] font-black uppercase tracking-widest text-gray-500">
          {{ product.category_name || 'Agriculture' }}
        </span>
        <span v-if="product.stock > 0" class="px-2.5 py-1 bg-emerald-50 border border-emerald-100 rounded-lg text-[9px] font-black uppercase tracking-widest text-[#10b481]">
          En stock
        </span>
        <span v-else class="px-2.5 py-1 bg-rose-50 border border-rose-100 rounded-lg text-[9px] font-black uppercase tracking-widest text-rose-500">
          Rupture
        </span>
      </template>
      <template #breadcrumb>
        <NuxtLink to="/buyer/dashboard" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
          <span>{{ t('dashboard.home') }}</span>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <NuxtLink to="/buyer/products" class="hover:text-[#10b481] transition-colors">{{ t('buyer.productsTitle') }}</NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481] truncate max-w-[120px]">{{ product?.name || 'Détail' }}</span>
      </template>
    </PageHeader>

    <!-- Loading -->
    <div v-if="loading && !product" class="grid grid-cols-1 lg:grid-cols-2 gap-8 animate-pulse">
      <div class="aspect-square bg-white rounded-2xl border border-gray-100"></div>
      <div class="space-y-4">
        <div class="h-10 w-3/4 bg-white rounded-xl"></div>
        <div class="h-6 w-1/4 bg-white rounded-xl"></div>
        <div class="h-36 bg-white rounded-xl"></div>
        <div class="h-14 w-full bg-white rounded-xl"></div>
      </div>
    </div>

    <!-- Content -->
    <div v-else-if="product" class="grid grid-cols-1 lg:grid-cols-2 gap-8">

      <!-- ===== IMAGE GALLERY ===== -->
      <div class="space-y-4">
        <div class="aspect-square bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden group relative">
          <img :src="activeImage || product.image_url"
            class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105" />
          <div class="absolute top-4 left-4">
            <span v-if="product.stock > 0"
              class="px-3 py-1.5 bg-white/90 backdrop-blur-sm rounded-xl text-[9px] font-black uppercase tracking-widest shadow-sm border border-gray-100 text-[#112830]">
              {{ product.category_name || 'Agriculture' }}
            </span>
          </div>
        </div>
        <div v-if="product.images?.length > 0" class="flex gap-3 overflow-x-auto pb-1">
          <div v-for="img in product.images" :key="img.id" @click="activeImage = img.image"
            :class="activeImage === img.image ? 'ring-2 ring-[#10b481] border-[#10b481]' : 'border-gray-100'"
            class="w-20 h-20 rounded-xl border-2 overflow-hidden cursor-pointer bg-white flex-shrink-0 transition-all">
            <img :src="img.image" class="w-full h-full object-cover" />
          </div>
        </div>
      </div>

      <!-- ===== PRODUCT INFO ===== -->
      <div class="space-y-6">

        <!-- Prix + stock -->
        <div class="flex items-center gap-4 flex-wrap">
          <p class="text-3xl font-black text-[#10b481]">
            {{ product.price }} Ar
            <span class="text-sm text-gray-400 font-bold">/ {{ product.unit }}</span>
          </p>
          <span v-if="product.stock > 0" class="px-3 py-1 bg-emerald-50 text-[#10b481] rounded-lg text-[9px] font-black uppercase tracking-widest border border-emerald-100">
            En Stock
          </span>
          <span v-else class="px-3 py-1 bg-rose-50 text-rose-500 rounded-lg text-[9px] font-black uppercase tracking-widest border border-rose-100">
            Rupture de stock
          </span>
        </div>

        <!-- Vendeur + description -->
        <div class="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm space-y-5">
          <div class="flex items-center gap-4 pb-4 border-b border-gray-50">
            <div class="w-10 h-10 bg-gray-50 rounded-xl flex items-center justify-center text-[#112830] flex-shrink-0">
              <i class="bx bx-store text-xl"></i>
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-[9px] font-black text-gray-400 uppercase tracking-widest">{{ t('buyer.soldByLabel') }}</p>
              <p class="text-sm font-black text-[#112830] truncate">{{ product.seller_name || 'Producteur Local' }}</p>
            </div>
            <NuxtLink to="/buyer/products"
              class="text-xs font-black text-[#10b481] uppercase tracking-widest hover:underline flex-shrink-0">
              Voir boutique
            </NuxtLink>
          </div>

          <p class="text-sm text-gray-500 leading-relaxed font-medium">
            {{ product.description || t('buyer.noDescription') }}
          </p>

          <div class="grid grid-cols-2 gap-3">
            <div class="p-3 bg-gray-50 rounded-xl">
              <p class="text-[8px] font-black text-gray-400 uppercase tracking-widest mb-0.5">{{ t('buyer.sourceTypeLabel') }}</p>
              <p class="text-xs font-black text-[#112830]">{{ product.source_type === 'HARVEST' ? t('buyer.directHarvest') : t('buyer.resale') }}</p>
            </div>
            <div class="p-3 bg-gray-50 rounded-xl">
              <p class="text-[8px] font-black text-gray-400 uppercase tracking-widest mb-0.5">{{ t('buyer.unitLabel') }}</p>
              <p class="text-xs font-black text-[#112830]">{{ product.unit }}</p>
            </div>
          </div>
        </div>

        <!-- Sélecteur quantité + bouton panier -->
        <div class="flex gap-3">
          <div class="flex items-center bg-white rounded-xl border border-gray-100 p-1 shadow-sm">
            <button @click="quantity > 1 ? quantity-- : null"
              class="w-10 h-10 flex items-center justify-center text-gray-400 hover:text-[#112830] transition-colors rounded-lg">
              <i class="bx bx-minus text-lg"></i>
            </button>
            <input v-model.number="quantity" type="number"
              class="w-14 text-center font-black text-[#112830] bg-transparent border-none outline-none text-sm" />
            <button @click="quantity++"
              class="w-10 h-10 flex items-center justify-center text-gray-400 hover:text-[#112830] transition-colors rounded-lg">
              <i class="bx bx-plus text-lg"></i>
            </button>
          </div>

          <button @click="handleAddToCart" :disabled="adding || product.stock <= 0"
            class="flex-1 py-3 bg-[#112830] text-white rounded-xl font-bold text-sm hover:bg-[#10b481] transition-all shadow-sm disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2">
            <div v-if="adding" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            <i v-else class="bx bx-shopping-bag text-base"></i>
            {{ adding ? t('buyer.addingToCart') : t('buyer.addToCart') }}
          </button>
        </div>

        <!-- Trust badges -->
        <div class="grid grid-cols-3 gap-3 pt-2 border-t border-gray-100">
          <div class="text-center space-y-1.5">
            <i class="bx bx-shield-check text-xl text-emerald-500"></i>
            <p class="text-[8px] font-black text-gray-400 uppercase tracking-widest">{{ t('buyer.securePaymentBadge') }}</p>
          </div>
          <div class="text-center space-y-1.5">
            <i class="bx bx-refresh text-xl text-blue-500"></i>
            <p class="text-[8px] font-black text-gray-400 uppercase tracking-widest">{{ t('buyer.easyReturns') }}</p>
          </div>
          <div class="text-center space-y-1.5">
            <i class="bx bx-timer text-xl text-amber-500"></i>
            <p class="text-[8px] font-black text-gray-400 uppercase tracking-widest">{{ t('buyer.fastDelivery') }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Toast -->
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
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useMarketplace } from '~/composables/useMarketplace';
import { useApi } from '~/composables/useApi';

const { t } = useI18n();
definePageMeta({ layout: 'dashboard' });

const route  = useRoute();
const router = useRouter();
const { addToCart, fetchCart } = useMarketplace();
const { apiFetch } = useApi();

const product     = ref<any>(null);
const loading     = ref(true);
const adding      = ref(false);
const activeImage = ref('');
const quantity    = ref(1);
const toast = ref({ visible: false, message: '' });

onMounted(async () => {
  try {
    const response = await apiFetch(`/api/catalogue/products/${route.params.id}/`);
    product.value = response;
    if (product.value.image_url) activeImage.value = product.value.image_url;
  } catch {
    router.push('/buyer/products');
  } finally {
    loading.value = false;
  }
});

function showToast(msg: string) {
  toast.value = { visible: true, message: msg };
  setTimeout(() => (toast.value.visible = false), 2500);
}

async function handleAddToCart() {
  if (!product.value) return;
  adding.value = true;
  try {
    await addToCart(product.value.id, quantity.value);
    await fetchCart();
    showToast(`"${product.value.name}" ${t('buyer.addedToCart')}`);
  } catch {
    console.error('Add to cart failed');
  } finally {
    adding.value = false;
  }
}
</script>

<style scoped>
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button { -webkit-appearance: none; margin: 0; }
.slide-up-enter-active, .slide-up-leave-active { transition: all 0.3s ease; }
.slide-up-enter-from, .slide-up-leave-to { opacity: 0; transform: translate(-50%, 1rem); }
</style>