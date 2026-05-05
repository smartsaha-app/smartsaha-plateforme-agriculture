<template>
  <div class="group bg-white rounded-3xl border border-gray-100 overflow-hidden shadow-sm hover:shadow-xl transition-all duration-500 hover:-translate-y-1">
    <!-- Image Header -->
    <div class="relative h-48 bg-gray-100 overflow-hidden">
      <img 
        v-if="productImage" 
        :src="productImage" 
        class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
      />
      <div v-else class="w-full h-full flex items-center justify-center text-gray-300">
        <i class="bx bx-image text-5xl"></i>
      </div>
      
      <!-- Badges -->
      <div class="absolute top-4 left-4 flex gap-2">
        <span class="px-3 py-1 bg-white/90 backdrop-blur-md text-[#112830] text-[10px] font-black uppercase tracking-widest rounded-full shadow-sm">
          {{ product.source_type === 'HARVEST' ? 'Récolte' : 'Revente' }}
        </span>
        <span v-if="!product.is_active" class="px-3 py-1 bg-red-500 text-white text-[10px] font-black uppercase tracking-widest rounded-full shadow-sm">
          Inactif
        </span>
      </div>
    </div>

    <!-- Content -->
    <div class="p-6">
      <div class="flex justify-between items-start mb-2">
        <h3 class="text-lg font-black text-[#112830] truncate pr-2 group-hover:text-[#10b481] transition-colors">
          {{ product.name }}
        </h3>
        <div class="text-right">
          <p class="text-xl font-black text-[#10b481] whitespace-nowrap">
            {{ product.price }} <span class="text-[10px] text-gray-400 uppercase tracking-widest">Ar</span>
          </p>
          <p class="text-[10px] font-bold text-gray-400">par {{ product.unit }}</p>
        </div>
      </div>

      <div class="flex items-center gap-2 mb-4 text-xs font-bold text-gray-400">
        <i class="bx bx-package text-[#10b481]"></i>
        <span>Stock: {{ product.stock }} {{ product.unit }}</span>
        <span class="text-gray-200">|</span>
        <i class="bx bx-store text-[#10b481]"></i>
        <span class="truncate">{{ product.seller_details?.username || 'Vendeur' }}</span>
      </div>

      <p class="text-gray-500 text-sm line-clamp-2 mb-6 h-10 font-medium">
        {{ product.category_name || 'Sans catégorie' }}
      </p>

      <!-- Actions -->
      <div class="flex gap-2">
        <button 
          v-if="isOwner"
          @click="$emit('edit', product)"
          class="flex-1 flex items-center justify-center gap-2 py-3 bg-[#112830] text-white rounded-2xl font-black text-[10px] uppercase tracking-widest hover:bg-[#112830]/90 transition-all shadow-lg shadow-[#112830]/10"
        >
          <i class="bx bx-edit-alt text-lg"></i>
          Modifier
        </button>
        <button 
          v-else
          @click="$emit('add-to-cart', product)"
          class="flex-1 flex items-center justify-center gap-2 py-3 bg-[#10b481] text-white rounded-2xl font-black text-[10px] uppercase tracking-widest hover:bg-[#0e9a6e] transition-all shadow-lg shadow-[#10b481]/10"
        >
          <i class="bx bx-cart-add text-lg"></i>
          Ajouter au panier
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  product: any,
  isOwner?: boolean
}>();

defineEmits(['edit', 'add-to-cart']);

const productImage = computed(() => {
  if (props.product.images && props.product.images.length > 0) {
    return props.product.images[0].image;
  }
  return props.product.image_url;
});
</script>
