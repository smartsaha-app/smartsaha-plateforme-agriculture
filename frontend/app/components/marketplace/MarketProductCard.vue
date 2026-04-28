<template>
  <div class="group bg-white rounded-3xl border border-gray-100 overflow-hidden shadow-sm hover:shadow-xl transition-all duration-500 hover:-translate-y-1">
    <!-- Image Header -->
    <div class="relative h-48 bg-gray-100 overflow-hidden">
      <img 
        v-if="product.images && product.images.length > 0" 
        :src="getImageUrl(product.images[0].image)" 
        class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
      />
      <div v-else class="w-full h-full flex items-center justify-center text-gray-300">
        <i class="bx bx-image text-5xl"></i>
      </div>
      
      <!-- Badges -->
      <div class="absolute top-4 left-4 flex gap-2">
        <span class="px-3 py-1 bg-white/90 backdrop-blur-md text-[#112830] text-[10px] font-black uppercase tracking-widest rounded-full shadow-sm">
          {{ product.post_type }}
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
          {{ product.title }}
        </h3>
        <p class="text-xl font-black text-[#10b481] whitespace-nowrap">
          {{ product.price }} <span class="text-[10px] text-gray-400 uppercase tracking-widest">Ar</span>
        </p>
      </div>

      <div class="flex items-center gap-2 mb-4 text-xs font-bold text-gray-400">
        <i class="bx bx-package text-[#10b481]"></i>
        <span>{{ product.quantity }} {{ product.unit }}</span>
        <span class="text-gray-200">|</span>
        <i class="bx bx-map text-[#10b481]"></i>
        <span class="truncate">{{ product.location || 'N/A' }}</span>
      </div>

      <p class="text-gray-500 text-sm line-clamp-2 mb-6 h-10 font-medium">
        {{ product.description }}
      </p>

      <!-- Actions -->
      <div class="flex gap-2">
        <button 
          @click="$emit('edit', product)"
          class="flex-1 flex items-center justify-center gap-2 py-3 bg-[#112830] text-white rounded-2xl font-black text-[10px] uppercase tracking-widest hover:bg-[#112830]/90 transition-all shadow-lg shadow-[#112830]/10"
        >
          <i class="bx bx-edit-alt text-lg"></i>
          Modifier le produit
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const config = useRuntimeConfig();

defineProps<{
  product: any
}>();

defineEmits(['edit', 'toggle']);

const getImageUrl = (path: string) => {
  if (!path) return '';
  if (path.startsWith('http')) return path;
  const baseUrl = config.public.apiBase || 'http://127.0.0.1:8000';
  return `${baseUrl}${path}`;
};
</script>
