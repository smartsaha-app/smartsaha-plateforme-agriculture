<template>
  <transition name="fade">
    <div 
      v-if="show"
      class="fixed inset-0 z-[9998] bg-white/60 backdrop-blur-xl flex flex-col items-center justify-center overflow-hidden pointer-events-none"
    >
      <!-- Subtle Background Glows -->
      <div class="absolute top-1/4 -left-1/4 w-1/2 h-1/2 bg-[#10b481]/5 rounded-full blur-[100px]"></div>
      <div class="absolute bottom-1/4 -right-1/4 w-1/2 h-1/2 bg-[#00c3ff]/5 rounded-full blur-[100px]"></div>

      <div class="relative flex flex-col items-center gap-8">
        <!-- Main Spinner Container -->
        <div class="relative w-32 h-32">
          <!-- Outer Static Ring -->
          <div class="absolute inset-0 border-[10px] border-gray-100/50 rounded-full shadow-sm"></div>
          <!-- Spinning Ring -->
          <div class="absolute inset-0 border-[10px] border-t-[#10b481] border-r-[#10b481]/40 rounded-full animate-spin-fast"></div>
          
          <!-- Moving Leaf Icon -->
          <div class="absolute inset-0 flex items-center justify-center">
              <div class="w-16 h-16 bg-white rounded-2xl shadow-xl flex items-center justify-center ring-1 ring-gray-100">
                <i class="bx bxs-leaf text-[#10b481] text-4xl animate-pulse"></i>
              </div>
          </div>
        </div>
        
        <!-- Text & Progress Indicators -->
        <div class="flex flex-col items-center gap-4">
          <h2 class="text-3xl font-black text-[#112830] tracking-tight">SmartSaha</h2>
          <div class="flex items-center gap-2">
            <div class="flex gap-1.5">
              <span class="w-2.5 h-2.5 bg-[#10b481] rounded-full animate-bounce [animation-delay:-0.3s]"></span>
              <span class="w-2.5 h-2.5 bg-[#10b481] rounded-full animate-bounce [animation-delay:-0.15s]"></span>
              <span class="w-2.5 h-2.5 bg-[#10b481] rounded-full animate-bounce"></span>
            </div>
            <p class="text-gray-400 text-sm font-black uppercase tracking-[0.2em] ml-2">Synchronisation</p>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup lang="ts">
defineProps<{
  show: boolean
}>()
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@keyframes spin-fast {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
.animate-spin-fast {
  animation: spin-fast 0.8s linear infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); opacity: 0.5; }
  50% { transform: translateY(-6px); opacity: 1; }
}
.animate-bounce {
  animation: bounce 0.6s infinite;
}
</style>
