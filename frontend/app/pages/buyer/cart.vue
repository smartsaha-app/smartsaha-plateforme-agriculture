<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8 space-y-6">

    <!-- ===== HEADER ===== -->
    <PageHeader :title="$t('buyer.cartTitle')">
      <template #subtitle>
        <i class="bx bx-cart"></i>
        {{ $t('buyer.cartDesc') }}
      </template>
      <template #breadcrumb>
        <NuxtLink to="/buyer/dashboard" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
          <span>Accueil</span>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">Panier</span>
      </template>
    </PageHeader>

    <!-- Loading -->
    <div v-if="loading" class="grid grid-cols-1 lg:grid-cols-3 gap-6 animate-pulse">
      <div class="lg:col-span-2 space-y-4">
        <div v-for="i in 3" :key="i" class="h-32 bg-white rounded-2xl border border-gray-100"></div>
      </div>
      <div class="h-80 bg-white rounded-2xl border border-gray-100"></div>
    </div>

    <!-- Empty cart -->
    <div v-else-if="!cart || cart.items?.length === 0" class="bg-white py-20 rounded-2xl border border-gray-100 text-center space-y-5 shadow-sm">
      <div class="w-20 h-20 bg-gray-50 rounded-2xl flex items-center justify-center mx-auto">
        <i class="bx bx-shopping-bag text-4xl text-gray-200"></i>
      </div>
      <div>
        <h3 class="text-base font-black text-[#112830]">{{ $t('buyer.emptyCart') }}</h3>
        <p class="text-sm text-gray-400 mt-1">{{ $t('buyer.emptyCartDesc') }}</p>
      </div>
      <NuxtLink to="/buyer/products"
        class="inline-flex items-center gap-2 px-6 py-3 bg-[#10b481] text-white rounded-xl font-bold text-sm shadow-sm hover:bg-emerald-400 transition-all">
        <i class="bx bx-store"></i>
        {{ $t('buyer.discoverProducts') }}
      </NuxtLink>
    </div>

    <!-- Cart content -->
    <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-6">

      <!-- Items -->
      <div class="lg:col-span-2 space-y-4">
        <div v-for="item in cart.items" :key="item.id"
          class="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-all flex gap-5 relative group">

          <!-- Image -->
          <div class="w-24 h-24 bg-gray-50 rounded-xl overflow-hidden flex-shrink-0 border border-gray-100">
            <img v-if="item.product_image" :src="item.product_image" class="w-full h-full object-cover" />
            <div v-else class="w-full h-full flex items-center justify-center text-gray-300">
              <i class="bx bx-image text-3xl"></i>
            </div>
          </div>

          <!-- Info -->
          <div class="flex-1 min-w-0 space-y-3">
            <div class="flex items-start justify-between gap-2">
              <div class="min-w-0">
                <h4 class="text-sm font-black text-[#112830] truncate">{{ item.product_name }}</h4>
                <p class="text-xs font-bold text-gray-400">{{ $t('buyer.unitPrice') }}: {{ item.price }} Ar</p>
              </div>
              <button @click="handleRemove(item.id)"
                class="w-8 h-8 rounded-lg bg-rose-50 text-rose-400 flex items-center justify-center hover:bg-rose-500 hover:text-white transition-all flex-shrink-0">
                <i class="bx bx-trash text-sm"></i>
              </button>
            </div>

            <div class="flex items-center justify-between gap-4 flex-wrap">
              <div class="flex items-center bg-gray-50 rounded-xl p-1 border border-gray-100">
                <button @click="updateQuantity(item, -1)" :disabled="item.quantity <= 1"
                  class="w-8 h-8 flex items-center justify-center text-gray-400 hover:text-[#112830] disabled:opacity-30 transition-colors rounded-lg">
                  <i class="bx bx-minus text-sm"></i>
                </button>
                <span class="w-10 text-center font-black text-sm text-[#112830]">{{ item.quantity }}</span>
                <button @click="updateQuantity(item, 1)"
                  class="w-8 h-8 flex items-center justify-center text-gray-400 hover:text-[#112830] transition-colors rounded-lg">
                  <i class="bx bx-plus text-sm"></i>
                </button>
              </div>

              <div class="text-right">
                <p class="text-[9px] font-black text-gray-300 uppercase tracking-widest mb-0.5">{{ $t('buyer.subtotal') }}</p>
                <p class="text-base font-black text-[#10b481]">{{ item.subtotal }} Ar</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Continue shopping -->
        <NuxtLink to="/buyer/products"
          class="flex items-center gap-2 text-xs font-bold text-gray-400 hover:text-[#10b481] transition-colors pt-1">
          <i class="bx bx-left-arrow-alt text-base"></i>
          Continuer mes achats
        </NuxtLink>
      </div>

      <!-- Summary -->
      <div class="space-y-4 lg:sticky lg:top-24 h-fit">
        <div class="bg-[#112830] text-white p-7 rounded-2xl shadow-xl relative overflow-hidden">
          <i class="bx bxs-shopping-bags absolute bottom-[-10%] right-[-10%] text-white/5 text-[10rem] pointer-events-none"></i>
          <h3 class="text-sm font-black mb-6 relative z-10">{{ $t('buyer.orderSummary') }}</h3>

          <div class="space-y-4 relative z-10">
            <div class="flex justify-between items-center text-white/60 text-sm">
              <span class="font-medium">{{ $t('buyer.items') }} ({{ cart.items_count }})</span>
              <span class="font-black text-white">{{ cart.total }} Ar</span>
            </div>
            <div class="flex justify-between items-center text-white/60 text-sm">
              <span class="font-medium">{{ $t('buyer.delivery') }}</span>
              <span class="font-medium italic text-xs">{{ $t('buyer.calculatedNextStep') }}</span>
            </div>
            <div class="h-px bg-white/10"></div>
            <div class="flex justify-between items-center">
              <span class="text-base font-black">{{ $t('buyer.total') }}</span>
              <span class="text-xl font-black text-[#10b481]">{{ cart.total }} Ar</span>
            </div>

            <NuxtLink to="/buyer/checkout"
              class="w-full py-3.5 bg-[#10b481] hover:bg-emerald-400 text-white rounded-xl font-bold text-sm transition-all mt-2 shadow-sm flex items-center justify-center gap-2 text-center">
              {{ $t('buyer.orderNow') }}
              <i class="bx bx-right-arrow-alt text-lg"></i>
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>

    <!-- Toast pour erreurs -->
    <transition name="slide-up">
      <div v-if="toast.visible"
        class="fixed bottom-6 left-1/2 -translate-x-1/2 z-[100] px-5 py-3 rounded-2xl shadow-xl flex items-center gap-3 text-sm font-bold"
        :class="toast.type === 'error' ? 'bg-rose-500 text-white' : 'bg-[#112830] text-white'">
        <i :class="toast.type === 'error' ? 'bx bx-error-circle' : 'bx bx-check-circle text-[#10b481]'" class="text-lg"></i>
        {{ toast.message }}
      </div>
    </transition>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useMarketplace } from '~/composables/useMarketplace';

definePageMeta({ layout: 'dashboard' });

const { cart, loading, fetchCart, addToCart, removeFromCart } = useMarketplace();

const toast = ref({ visible: false, message: '', type: 'success' as 'success' | 'error' });

function showToast(message: string, type: 'success' | 'error' = 'success') {
  toast.value = { visible: true, message, type };
  setTimeout(() => (toast.value.visible = false), 3000);
}

onMounted(() => fetchCart());

async function updateQuantity(item: any, delta: number) {
  try {
    const productId = typeof item.product === 'object' ? item.product.id : item.product;
    await addToCart(productId, delta);
    await fetchCart();
  } catch (err: any) {
    const msg = err.data?.error || 'Erreur lors de la mise à jour de la quantité.';
    showToast(msg, 'error');
  }
}

async function handleRemove(itemId: number) {
  try {
    await removeFromCart(itemId);
  } catch {
    showToast('Impossible de supprimer l\'article.', 'error');
  }
}
</script>

<style scoped>
.slide-up-enter-active, .slide-up-leave-active { transition: all 0.3s ease; }
.slide-up-enter-from, .slide-up-leave-to { opacity: 0; transform: translate(-50%, 1rem); }
</style>