<template>
  <div class="space-y-8 pb-20">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-3xl font-black text-[#112830]">{{ $t('buyer.cartTitle') }}</h1>
        <p class="text-gray-500 font-medium">{{ $t('buyer.cartDesc') }}</p>
      </div>
    </div>

    <div v-if="loading" class="grid grid-cols-1 lg:grid-cols-3 gap-12 animate-pulse">
      <div class="lg:col-span-2 space-y-4">
        <div v-for="i in 3" :key="i" class="h-40 bg-white rounded-[2.5rem] border border-gray-100"></div>
      </div>
      <div class="h-96 bg-white rounded-[2.5rem] border border-gray-100"></div>
    </div>

    <div v-else-if="!cart || cart.items?.length === 0" class="bg-white py-24 rounded-[3rem] border border-gray-100 text-center space-y-6 shadow-sm">
      <div class="w-24 h-24 bg-gray-50 rounded-full flex items-center justify-center mx-auto text-gray-200">
        <i class="bx bx-shopping-bag text-5xl"></i>
      </div>
      <div class="space-y-2">
        <h3 class="text-xl font-black text-[#112830]">{{ $t('buyer.emptyCart') }}</h3>
        <p class="text-gray-400 max-w-sm mx-auto">{{ $t('buyer.emptyCartDesc') }}</p>
      </div>
      <NuxtLink to="/buyer/products" class="inline-flex items-center gap-2 px-8 py-4 bg-[#10b481] text-white rounded-2xl font-black text-xs uppercase tracking-widest shadow-lg shadow-[#10b481]/20 hover:scale-105 transition-all">
        {{ $t('buyer.discoverProducts') }}
      </NuxtLink>
    </div>

    <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-12">
      <!-- Items List -->
      <div class="lg:col-span-2 space-y-6">
        <div 
          v-for="item in cart.items" 
          :key="item.id"
          class="bg-white p-8 rounded-[2.5rem] border border-gray-100 shadow-sm hover:shadow-md transition-all flex flex-col md:flex-row gap-8 relative group"
        >
          <!-- Product Image -->
          <div class="w-32 h-32 bg-gray-50 rounded-[2rem] overflow-hidden flex-shrink-0 border border-gray-100">
            <img v-if="item.product_image" :src="item.product_image" class="w-full h-full object-cover" />
            <div v-else class="w-full h-full flex items-center justify-center text-gray-300">
              <i class="bx bx-image text-4xl"></i>
            </div>
          </div>

          <!-- Info & Controls -->
          <div class="flex-1 space-y-4">
            <div class="flex justify-between items-start">
              <div>
                <h4 class="text-xl font-black text-[#112830]">{{ item.product_name }}</h4>
                <p class="text-xs font-bold text-gray-400 uppercase tracking-widest">{{ $t('buyer.unitPrice') }}: {{ item.price }} Ar</p>
              </div>
              <button @click="handleRemove(item.id)" class="w-10 h-10 rounded-xl bg-rose-50 text-rose-500 flex items-center justify-center hover:bg-rose-500 hover:text-white transition-all">
                <i class="bx bx-trash text-xl"></i>
              </button>
            </div>

            <div class="flex flex-wrap items-center justify-between gap-6 pt-2">
              <div class="flex items-center bg-gray-50 rounded-xl p-1 border border-gray-100">
                <button 
                  @click="updateQuantity(item, -1)"
                  :disabled="item.quantity <= 1"
                  class="w-10 h-10 flex items-center justify-center text-gray-400 hover:text-[#112830] disabled:opacity-30"
                >
                  <i class="bx bx-minus"></i>
                </button>
                <span class="w-12 text-center font-black text-[#112830]">{{ item.quantity }}</span>
                <button 
                  @click="updateQuantity(item, 1)"
                  class="w-10 h-10 flex items-center justify-center text-gray-400 hover:text-[#112830]"
                >
                  <i class="bx bx-plus"></i>
                </button>
              </div>

              <div class="text-right">
                <p class="text-[10px] font-black text-gray-300 uppercase tracking-widest mb-1">{{ $t('buyer.subtotal') }}</p>
                <p class="text-xl font-black text-[#10b481]">{{ item.subtotal }} Ar</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Order Summary -->
      <div class="space-y-6 lg:sticky lg:top-24 h-fit">
        <div class="bg-[#112830] text-white p-10 rounded-[3rem] shadow-xl relative overflow-hidden">
          <h3 class="text-xl font-black mb-10 relative z-10">{{ $t('buyer.orderSummary') }}</h3>
          
          <div class="space-y-6 relative z-10">
            <div class="flex justify-between items-center text-white/60">
              <span class="font-bold">{{ $t('buyer.items') }} ({{ cart.items_count }})</span>
              <span class="font-black text-white">{{ cart.total }} Ar</span>
            </div>
            <div class="flex justify-between items-center text-white/60">
              <span class="font-bold">{{ $t('buyer.delivery') }}</span>
              <span class="font-black text-white italic">{{ $t('buyer.calculatedNextStep') }}</span>
            </div>
            
            <div class="h-px bg-white/10 my-4"></div>
            
            <div class="flex justify-between items-center text-2xl">
              <span class="font-black">{{ $t('buyer.total') }}</span>
              <span class="text-[#10b481] font-black">{{ cart.total }} Ar</span>
            </div>

            <button 
              @click="navigateTo('/buyer/checkout')"
              class="w-full py-5 bg-[#10b481] hover:bg-white hover:text-[#112830] text-white rounded-2xl font-black text-xs uppercase tracking-widest transition-all mt-6 shadow-lg shadow-[#10b481]/20 flex items-center justify-center gap-3"
            >
              {{ $t('buyer.orderNow') }}
              <i class="bx bx-right-arrow-alt text-xl"></i>
            </button>
          </div>

          <!-- Decor -->
          <i class="bx bxs-shopping-bags absolute bottom-[-10%] right-[-10%] text-white/5 text-[12rem]"></i>
        </div>

        <div class="bg-white p-8 rounded-[2.5rem] border border-gray-100 shadow-sm flex items-center gap-4">
          <div class="w-12 h-12 bg-emerald-50 text-[#10b481] rounded-2xl flex items-center justify-center text-2xl flex-shrink-0">
            <i class="bx bx-shield-quarter"></i>
          </div>
          <p class="text-[11px] text-gray-500 font-bold leading-relaxed">
            {{ $t('buyer.securePayment') }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useMarketplace } from '~/composables/useMarketplace';

definePageMeta({
  layout: 'dashboard'
});

const { cart, loading, fetchCart, addToCart, removeFromCart } = useMarketplace();

onMounted(() => {
  fetchCart();
});

const updateQuantity = async (item: any, delta: number) => {
  try {
    const productId = typeof item.product === 'object' ? item.product.id : item.product;
    await addToCart(productId, delta);
    await fetchCart();
  } catch (err: any) {
    const msg = err.data?.error || "Erreur lors de la mise à jour de la quantité.";
    alert(msg);
    console.error('Update quantity failed', err);
  }
};

const handleRemove = async (itemId: number) => {
  try {
    await removeFromCart(itemId);
  } catch (err) {
    console.error('Remove failed', err);
  }
};
</script>
