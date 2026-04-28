<template>
  <div class="animate-pulse space-y-6 max-w-full overflow-hidden">
    <!-- Header Skeleton -->
    <div class="flex items-center justify-between">
      <div class="h-10 w-48 bg-gray-200 rounded-lg"></div>
      <div class="h-6 w-32 bg-gray-100 rounded-lg"></div>
    </div>

    <!-- KPI Cards Skeleton -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
      <div v-for="i in 4" :key="i" class="p-5 rounded-xl border border-gray-100 bg-white shadow-sm flex items-start gap-4">
        <div class="w-12 h-12 bg-gray-200 rounded-xl"></div>
        <div class="flex-1 space-y-2">
          <div class="h-4 w-16 bg-gray-100 rounded"></div>
          <div class="h-7 w-12 bg-gray-200 rounded"></div>
        </div>
      </div>
    </div>

    <!-- Charts Row Skeleton -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-5">
      <div class="lg:col-span-2 bg-white rounded-xl border border-gray-100 p-6 h-[400px]">
        <div class="flex justify-between items-start mb-6">
          <div class="space-y-2">
            <div class="h-5 w-48 bg-gray-200 rounded"></div>
            <div class="h-3 w-32 bg-gray-100 rounded"></div>
          </div>
          <div class="h-8 w-40 bg-gray-100 rounded"></div>
        </div>
        <div class="h-[280px] w-full bg-gray-50 rounded-lg"></div>
      </div>
      
      <div class="bg-white rounded-xl border border-gray-100 p-6 h-[400px]">
        <div class="flex justify-between items-start mb-6">
          <div class="space-y-2">
            <div class="h-5 w-32 bg-gray-200 rounded"></div>
            <div class="h-3 w-24 bg-gray-100 rounded"></div>
          </div>
        </div>
        <div class="space-y-4">
          <div v-for="j in 5" :key="j" class="flex items-center gap-3">
            <div class="w-8 h-8 bg-gray-100 rounded-full"></div>
            <div class="flex-1 space-y-1.5">
              <div class="h-3 w-3/4 bg-gray-200 rounded"></div>
              <div class="h-2 w-1/2 bg-gray-100 rounded"></div>
            </div>
            <div class="h-4 w-10 bg-gray-100 rounded"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Long Chart Skeleton -->
    <div class="bg-white rounded-xl border border-gray-100 p-6 h-[400px]">
      <div class="flex justify-between items-start mb-6">
        <div class="space-y-2">
          <div class="h-5 w-64 bg-gray-200 rounded"></div>
          <div class="h-3 w-40 bg-gray-100 rounded"></div>
        </div>
        <div class="flex gap-2">
          <div class="h-8 w-24 bg-gray-100 rounded"></div>
          <div class="h-8 w-24 bg-gray-100 rounded"></div>
        </div>
      </div>
      <div class="h-[280px] w-full bg-gray-50 rounded-lg"></div>
    </div>
  </div>
</template>

<style scoped>
.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}
</style>
