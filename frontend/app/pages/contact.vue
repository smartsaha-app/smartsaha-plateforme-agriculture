<template>
  <div class="p-6 flex flex-col h-full space-y-6">
    <h2 class="text-3xl font-extrabold text-[#222831]">Contact</h2>

    <div class="flex-1 border rounded-2xl overflow-hidden shadow-sm">
      <iframe
        :src="formUrl"
        class="w-full h-full min-h-[600px]"
        frameborder="0"
        scrolling="yes"
      ></iframe>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: "dashboard",
});

const formUrl =
  "https://docs.google.com/forms/d/e/1FAIpQLSenvw7yEIAhICjvzzaxT9DGoipfVE5acYNFFQM9xog_ZNTZgg/viewform?usp=sf_link";
</script>

<style scoped>
div::-webkit-scrollbar {
  width: 6px;
}

div::-webkit-scrollbar-thumb {
  background-color: #d0d0d0;
  border-radius: 10px;
}

div::-webkit-scrollbar-thumb:hover {
  background-color: #a0a0a0;
}
</style>
