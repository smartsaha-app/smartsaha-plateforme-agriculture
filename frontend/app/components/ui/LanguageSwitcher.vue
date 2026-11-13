<template>
  <div ref="root" class="relative">
    <button
      type="button"
      @click="isOpen = !isOpen"
      class="flex items-center gap-2 px-3 py-2 bg-white/80 hover:bg-white border border-gray-100 rounded-xl shadow-sm transition-all text-xs font-black uppercase tracking-widest text-[#112830]"
      :aria-label="$t('layoutsVitrine.changeLanguage')"
      :aria-expanded="isOpen"
    >
      <i class="bx bx-globe text-base text-[#10b481]"></i>
      {{ locale.toUpperCase() }}
      <i class="bx bx-chevron-down text-sm transition-transform" :class="{ 'rotate-180': isOpen }"></i>
    </button>
    <div
      v-if="isOpen"
      class="absolute top-full right-0 mt-2 w-40 bg-white border border-gray-100 rounded-2xl shadow-2xl p-2 z-[200] overflow-hidden"
    >
      <button
        v-for="l in locales"
        :key="l.code"
        type="button"
        @click="select(l.code)"
        class="w-full flex items-center gap-3 px-4 py-3 hover:bg-[#10b481]/5 text-left transition-all rounded-xl group"
        :class="{ 'bg-[#10b481]/10 text-[#10b481]': locale === l.code }"
      >
        <div class="w-1.5 h-1.5 rounded-full transition-all" :class="locale === l.code ? 'bg-[#10b481]' : 'bg-gray-200 group-hover:bg-[#10b481]/30'"></div>
        <span class="text-xs font-black uppercase tracking-widest">{{ l.name }}</span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const { locale, locales, setLocale } = useI18n()

const isOpen = ref(false)
const root = ref<HTMLElement | null>(null)

const select = async (code: string) => {
  isOpen.value = false
  if (code !== locale.value) await setLocale(code as any)
}

// Close when clicking outside
const onClickOutside = (e: MouseEvent) => {
  if (root.value && !root.value.contains(e.target as Node)) isOpen.value = false
}
onMounted(() => document.addEventListener('click', onClickOutside))
onUnmounted(() => document.removeEventListener('click', onClickOutside))
</script>
