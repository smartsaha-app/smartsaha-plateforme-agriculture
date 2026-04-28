<script setup lang="ts">
defineProps<{ label: string; value: string | number }>();
</script>

<template #DetailItem="{ label, value }">
  <div class="flex flex-col gap-1">
    <span class="font-semibold text-[#212121]">{{ label }}</span>
    <span class="text-gray-700">{{ value }}</span>
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
