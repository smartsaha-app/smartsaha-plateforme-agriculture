<script setup lang="ts">
defineProps<{
  number: string | number;
  title: string;
  text: string;
  icon?: string;
}>();
</script>

<template>
  <div
    class="flex items-start gap-4 p-4 rounded border border-gray-200 hover:shadow-lg transition"
  >
    <div
      class="w-10 h-10 bg-[#10b481] p-4 rounded flex items-center justify-center text-white font-bold text-lg"
    >
      <i v-if="icon" :class="['bx', icon, 'text-lg']"></i>
      <template v-else>{{ number }}</template>
    </div>

    <div>
      <p class="font-semibold text-[#212121] mb-1">{{ title }}</p>
      <p class="text-gray-700 text-sm">{{ text }}</p>
    </div>
  </div>
</template>

<style scoped>
@keyframes gradient-slide {
  0% {
    background-position: 0%;
  }
  50% {
    background-position: 100%;
  }
  100% {
    background-position: 0%;
  }
}
.animate-gradient {
  background-size: 200% 200%;
  animation: gradient-slide 3s ease infinite;
}
</style>
