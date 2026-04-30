<template>
  <transition name="fade-zoom">
    <div 
      v-if="show"
      class="fixed inset-0 z-[9999] flex flex-col items-center justify-center bg-[#0d1b21] text-white overflow-hidden pointer-events-none"
    >
      <!-- Premium Background Effects -->
      <div class="absolute inset-0 bg-[radial-gradient(circle_at_center,_#10b48122_0%,_transparent_70%)] animate-pulse-slow"></div>
      <div class="absolute -top-[20%] -left-[10%] w-[60%] h-[60%] bg-[#10b481]/10 rounded-full blur-[120px] animate-blob"></div>
      <div class="absolute -bottom-[20%] -right-[10%] w-[60%] h-[60%] bg-[#00c3ff]/10 rounded-full blur-[120px] animate-blob animation-delay-2000"></div>

      <!-- Main Branded Content -->
      <div class="relative z-10 flex flex-col items-center animate-scale-in">
        <div class="relative mb-8">
            <!-- Glow behind logo -->
            <div class="absolute inset-0 bg-[#10b481]/30 blur-3xl rounded-full scale-110"></div>
            <img
              src="/logo.png"
              alt="SmartSaha"
              class="relative w-36 h-36 rounded-2xl shadow-[0_20px_50px_rgba(16,180,129,0.3)] ring-1 ring-white/10"
            />
        </div>
        
        <h1 class="text-6xl font-black tracking-tighter text-white mb-4 bg-clip-text text-transparent bg-gradient-to-b from-white to-gray-400">
          SmartSaha
        </h1>
        <p class="text-[#10b481] text-lg font-bold tracking-[0.4em] uppercase opacity-80 mb-12">
          Nurture data • Harvest impact
        </p>
      </div>

      <!-- Expansive Progress Bar (Bottom) -->
      <div class="absolute bottom-32 left-1/2 -translate-x-1/2 w-[300px] max-w-[80vw] h-1.5 bg-white/5 rounded-full overflow-hidden backdrop-blur-md">
        <div class="h-full bg-gradient-to-r from-[#10b481] via-[#00c3ff] to-[#10b481] animate-loading w-full origin-left"></div>
      </div>

      <!-- Bottom Credits / Technical Info -->
      <div class="absolute bottom-12 flex flex-col items-center gap-2">
        <div class="text-[11px] text-gray-500 font-black uppercase tracking-[0.3em] inline-flex items-center gap-2">
            <span class="w-1.5 h-1.5 bg-[#10b481] rounded-full animate-ping"></span>
            Initialisation du moteur agronomique
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
@keyframes scale-in {
  0% { transform: scale(0.85); opacity: 0; filter: blur(20px); }
  100% { transform: scale(1); opacity: 1; filter: blur(0); }
}
.animate-scale-in {
  animation: scale-in 1s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
}

@keyframes loading {
  0% { transform: translateX(-100%); }
  50% { transform: translateX(0); }
  100% { transform: translateX(100%); }
}
.animate-loading {
  animation: loading 3s cubic-bezier(0.65, 0, 0.35, 1) infinite;
}

@keyframes blob {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(30px, -50px) scale(1.1); }
  66% { transform: translate(-20px, 20px) scale(0.9); }
}
.animate-blob {
  animation: blob 7s infinite alternate;
}

@keyframes pulse-slow {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 1; }
}
.animate-pulse-slow {
  animation: pulse-slow 4s ease-in-out infinite;
}

.animation-delay-2000 {
  animation-delay: 2s;
}

.fade-zoom-enter-active,
.fade-zoom-leave-active {
  transition: all 1s cubic-bezier(0.4, 0, 0.2, 1);
}
.fade-zoom-enter-from {
  opacity: 0;
  transform: scale(1.1);
}
.fade-zoom-leave-to {
  opacity: 0;
  transform: scale(0.9);
  filter: blur(20px);
}
</style>
