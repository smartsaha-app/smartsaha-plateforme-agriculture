<template>
  <div class="flex items-center justify-between gap-4 py-4 px-2">
    <!-- Info Section -->
    <div class="hidden sm:block">
      <p class="text-xs font-bold text-gray-400 uppercase tracking-widest">
        {{ t('showing') }} 
        <span class="text-[#112830]">{{ startItem }} - {{ endItem }}</span> 
        {{ t('of') }} 
        <span class="text-[#10b481]">{{ totalCount }}</span>
      </p>
    </div>

    <!-- Controls Section -->
    <div class="flex items-center gap-2">
      <!-- Previous -->
      <button 
        @click="changePage(currentPage - 1)"
        :disabled="currentPage === 1"
        class="w-10 h-10 rounded-xl bg-white border border-gray-100 flex items-center justify-center text-[#112830] hover:bg-gray-50 disabled:opacity-30 disabled:hover:bg-white transition shadow-sm"
      >
        <i class="bx bx-chevron-left text-xl"></i>
      </button>

      <!-- Pages -->
      <div class="flex items-center gap-1">
        <template v-for="page in visiblePages" :key="page">
          <button 
            v-if="page !== '...'"
            @click="changePage(page as number)"
            :class="[
              'w-10 h-10 rounded-xl text-xs font-black transition-all duration-300',
              currentPage === page 
                ? 'bg-[#112830] text-white shadow-lg shadow-[#112830]/20' 
                : 'bg-white border border-gray-100 text-[#112830] hover:bg-gray-50'
            ]"
          >
            {{ page }}
          </button>
          <span v-else class="w-10 h-10 flex items-center justify-center text-gray-300 font-bold">
            ...
          </span>
        </template>
      </div>

      <!-- Next -->
      <button 
        @click="changePage(currentPage + 1)"
        :disabled="currentPage === totalPages"
        class="w-10 h-10 rounded-xl bg-white border border-gray-100 flex items-center justify-center text-[#112830] hover:bg-gray-50 disabled:opacity-30 disabled:hover:bg-white transition shadow-sm"
      >
        <i class="bx bx-chevron-right text-xl"></i>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
interface Props {
  totalCount: number;
  perPage: number;
  currentPage: number;
}

const props = defineProps<Props>();
const emit = defineEmits(['change-page']);

const { t: nuxtT } = useI18n();
const t = (key: string) => nuxtT(`dashboard.${key}`);

const totalPages = computed(() => Math.ceil(props.totalCount / props.perPage));

const startItem = computed(() => ((props.currentPage - 1) * props.perPage) + 1);
const endItem = computed(() => Math.min(props.currentPage * props.perPage, props.totalCount));

const visiblePages = computed(() => {
  const pages: (number | string)[] = [];
  const maxPages = 5;

  if (totalPages.value <= maxPages) {
    for (let i = 1; i <= totalPages.value; i++) pages.push(i);
  } else {
    pages.push(1);
    if (props.currentPage > 3) pages.push('...');
    
    let start = Math.max(2, props.currentPage - 1);
    let end = Math.min(totalPages.value - 1, props.currentPage + 1);
    
    if (props.currentPage <= 3) end = 4;
    if (props.currentPage >= totalPages.value - 2) start = totalPages.value - 3;

    for (let i = start; i <= end; i++) pages.push(i);
    
    if (props.currentPage < totalPages.value - 2) pages.push('...');
    pages.push(totalPages.value);
  }
  return pages;
});

function changePage(page: number) {
  if (page >= 1 && page <= totalPages.value) {
    emit('change-page', page);
  }
}
</script>
