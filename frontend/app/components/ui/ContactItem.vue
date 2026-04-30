<template>
  <li class="flex items-center space-x-3">
    <div
      class="w-8 h-8 flex items-center justify-center bg-[#10b481] text-white rounded-full"
    >
      <i :class="['bx', icon, 'text-lg']"></i>
    </div>
    <template v-if="href">
      <a :href="href" class="text-[#10b481] font-medium hover:underline">{{
        text
      }}</a>
    </template>
    <template v-else>
      <span class="text-gray-700 font-medium">{{ text }}</span>
    </template>
  </li>
</template>

<script setup lang="ts">
defineProps<{
  icon: string;
  text: string;
  href?: string;
}>();
</script>
