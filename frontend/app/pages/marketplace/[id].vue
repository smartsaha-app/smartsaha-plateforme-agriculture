<template>
  <div class="min-h-screen bg-gray-50/50 pt-24 pb-20 px-6">
    <div class="max-w-[1400px] mx-auto">
      <!-- Breadcrumbs & Back -->
      <button @click="router.back()" class="flex items-center gap-2 text-gray-400 hover:text-[#112830] transition-colors mb-8 font-black text-xs uppercase tracking-widest">
        <i class="bx bx-left-arrow-alt text-xl"></i>
        Retour aux produits
      </button>

      <div v-if="loading && !product" class="grid grid-cols-1 lg:grid-cols-2 gap-12 animate-pulse">
        <div class="aspect-square bg-white rounded-[3rem] border border-gray-100"></div>
        <div class="space-y-6">
          <div class="h-12 w-3/4 bg-white rounded-2xl"></div>
          <div class="h-6 w-1/4 bg-white rounded-2xl"></div>
          <div class="h-40 bg-white rounded-2xl"></div>
          <div class="h-16 w-full bg-white rounded-2xl"></div>
        </div>
      </div>

      <div v-else-if="product" class="grid grid-cols-1 lg:grid-cols-2 gap-12">
        <!-- Image Gallery -->
        <div class="space-y-6">
          <div class="aspect-square bg-white rounded-[3rem] border border-gray-100 shadow-sm overflow-hidden group relative">
            <img 
              :src="activeImage || product.image_url" 
              class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
            />
            <div class="absolute top-6 left-6">
              <span class="px-4 py-2 bg-white/90 backdrop-blur-md rounded-2xl text-[10px] font-black uppercase tracking-widest shadow-sm border border-gray-100">
                {{ product.category_name || 'Agriculture' }}
              </span>
            </div>
          </div>
          
          <div v-if="product.images?.length > 0" class="flex gap-4 overflow-x-auto pb-2 no-scrollbar">
            <div 
              v-for="img in product.images" 
              :key="img.id"
              @click="activeImage = img.image"
              :class="[activeImage === img.image ? 'border-[#10b481] ring-2 ring-[#10b481]/10' : 'border-gray-100']"
              class="w-24 h-24 rounded-2xl border-2 overflow-hidden cursor-pointer bg-white flex-shrink-0 transition-all"
            >
              <img :src="img.image" class="w-full h-full object-cover" />
            </div>
          </div>
        </div>

        <!-- Product Info -->
        <div class="space-y-10">
          <div class="space-y-4">
            <div class="flex items-center gap-2 text-[#10b481]">
              <i class="bx bxs-star text-lg"></i>
              <span class="text-sm font-black uppercase tracking-widest">Produit Certifié</span>
            </div>
            <h1 class="text-4xl md:text-5xl font-black text-[#112830] leading-tight">{{ product.name }}</h1>
            <div class="flex items-center gap-6">
              <div class="text-3xl font-black text-[#10b481]">{{ product.price }} Ar <span class="text-sm text-gray-400 font-bold">/ {{ product.unit }}</span></div>
              <div v-if="product.stock > 0" class="px-3 py-1 bg-emerald-50 text-[#10b481] rounded-lg text-[10px] font-black uppercase tracking-widest border border-[#10b481]/10">En Stock</div>
              <div v-else class="px-3 py-1 bg-rose-50 text-rose-500 rounded-lg text-[10px] font-black uppercase tracking-widest border border-rose-500/10">Rupture</div>
            </div>
          </div>

          <div class="p-8 bg-white rounded-[2.5rem] border border-gray-100 shadow-sm space-y-6">
            <div class="flex items-center gap-4 border-b border-gray-50 pb-6">
               <div class="w-12 h-12 bg-gray-50 rounded-2xl flex items-center justify-center text-[#112830]">
                 <i class="bx bx-store text-2xl"></i>
               </div>
               <div>
                 <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest">Vendu par</p>
                 <p class="font-black text-[#112830]">{{ product.seller_name || 'Producteur Local' }}</p>
               </div>
               <button class="ml-auto text-xs font-black text-[#10b481] uppercase tracking-widest hover:underline">Voir profil</button>
            </div>

            <div class="space-y-4">
              <p class="text-gray-500 leading-relaxed font-medium">
                {{ product.description || 'Aucune description disponible pour ce produit.' }}
              </p>
            </div>

            <div class="grid grid-cols-2 gap-4 pt-4">
              <div class="p-4 bg-gray-50 rounded-2xl space-y-1">
                <p class="text-[9px] font-black text-gray-400 uppercase tracking-widest">Type de source</p>
                <p class="text-sm font-black text-[#112830]">{{ product.source_type === 'HARVEST' ? 'Récolte Directe' : 'Revente' }}</p>
              </div>
              <div class="p-4 bg-gray-50 rounded-2xl space-y-1">
                <p class="text-[9px] font-black text-gray-400 uppercase tracking-widest">Unité</p>
                <p class="text-sm font-black text-[#112830]">{{ product.unit }}</p>
              </div>
            </div>
          </div>

          <div class="flex flex-col sm:flex-row gap-4">
            <div class="flex items-center bg-white rounded-2xl border border-gray-100 p-2 shadow-sm">
              <button 
                @click="quantity > 1 ? quantity-- : null"
                class="w-12 h-12 flex items-center justify-center text-gray-400 hover:text-[#112830] transition-colors"
              >
                <i class="bx bx-minus text-xl"></i>
              </button>
              <input 
                v-model.number="quantity"
                type="number" 
                class="w-16 text-center font-black text-[#112830] bg-transparent border-none outline-none"
              />
              <button 
                @click="quantity++"
                class="w-12 h-12 flex items-center justify-center text-gray-400 hover:text-[#112830] transition-colors"
              >
                <i class="bx bx-plus text-xl"></i>
              </button>
            </div>

            <button 
              @click="handleAddToCart"
              :disabled="adding || product.stock <= 0"
              class="flex-1 py-5 bg-[#112830] text-white rounded-2xl font-black text-xs uppercase tracking-widest shadow-xl shadow-[#112830]/10 hover:bg-[#10b481] transition-all flex items-center justify-center gap-3"
            >
              <i v-if="adding" class="bx bx-loader-alt animate-spin text-xl"></i>
              <i v-else class="bx bx-shopping-bag text-xl"></i>
              Ajouter au panier
            </button>
          </div>

          <!-- Trust Badges -->
          <div class="grid grid-cols-3 gap-4 border-t border-gray-100 pt-8">
            <div class="text-center space-y-2">
              <i class="bx bx-shield-check text-2xl text-emerald-500"></i>
              <p class="text-[9px] font-black text-gray-400 uppercase tracking-widest">Paiement Sécurisé</p>
            </div>
            <div class="text-center space-y-2">
              <i class="bx bx-refresh text-2xl text-blue-500"></i>
              <p class="text-[9px] font-black text-gray-400 uppercase tracking-widest">Retours Faciles</p>
            </div>
            <div class="text-center space-y-2">
              <i class="bx bx-timer text-2xl text-amber-500"></i>
              <p class="text-[9px] font-black text-gray-400 uppercase tracking-widest">Livraison Rapide</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useMarketplace } from '~/composables/useMarketplace';
import { useApi } from '~/composables/useApi';

const route = useRoute();
const router = useRouter();
const { addToCart, fetchCart } = useMarketplace();
const { apiFetch } = useApi();

const product = ref<any>(null);
const loading = ref(true);
const adding = ref(false);
const activeImage = ref('');
const quantity = ref(1);

onMounted(async () => {
  try {
    const id = route.params.id;
    const response = await apiFetch(`/api/catalogue/products/${id}/`);
    product.value = response;
    if (product.value.image_url) activeImage.value = product.value.image_url;
  } catch (err) {
    console.error('Failed to fetch product', err);
    navigateTo('/marketplace');
  } finally {
    loading.value = false;
  }
});

const handleAddToCart = async () => {
  if (!product.value) return;
  adding.value = true;
  try {
    await addToCart(product.value.id, quantity.value);
    await fetchCart();
    // Success notification could go here
  } catch (err) {
    console.error('Add to cart failed', err);
  } finally {
    adding.value = false;
  }
};
</script>

<style scoped>
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
