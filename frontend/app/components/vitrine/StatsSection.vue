<template>
  <section id="stats-section-trigger" class="py-20 bg-[#112830] text-white relative overflow-hidden">
    <!-- Background subtle glow -->
    <div class="absolute inset-0 pointer-events-none">
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[200px] bg-[#10b481]/6 rounded-full blur-[80px]"></div>
    </div>

    <div class="max-w-7xl mx-auto px-6 relative z-10">
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-6 lg:gap-10">

        <!-- Agriculteurs -->
        <div class="flex flex-col items-center text-center group">
          <div class="w-12 h-12 bg-[#10b481]/10 border border-[#10b481]/20 rounded-2xl flex items-center justify-center mb-4 group-hover:bg-[#10b481]/20 transition-all duration-300">
            <i class="bx bx-user text-[#10b481] text-xl"></i>
          </div>
          <div class="flex items-end gap-0.5 mb-2">
            <span class="text-4xl font-black text-[#10b481] leading-none tabular-nums">{{ counts.farmers }}</span>
            <span class="text-[#10b481] font-black text-2xl leading-none mb-0.5">+</span>
          </div>
          <p class="text-[10px] font-black uppercase tracking-widest text-gray-400">{{ $t('stats.farmers') }}</p>
        </div>

        <!-- Coopératives -->
        <div class="flex flex-col items-center text-center group">
          <div class="w-12 h-12 bg-[#10b481]/10 border border-[#10b481]/20 rounded-2xl flex items-center justify-center mb-4 group-hover:bg-[#10b481]/20 transition-all duration-300">
            <i class="bx bx-buildings text-[#10b481] text-xl"></i>
          </div>
          <div class="flex items-end gap-0.5 mb-2">
            <span class="text-4xl font-black text-[#10b481] leading-none tabular-nums">{{ counts.cooperatives }}</span>
            <span class="text-[#10b481] font-black text-2xl leading-none mb-0.5">+</span>
          </div>
          <p class="text-[10px] font-black uppercase tracking-widest text-gray-400">{{ $t('stats.cooperatives') }}</p>
        </div>

        <!-- Hectares -->
        <div class="flex flex-col items-center text-center group">
          <div class="w-12 h-12 bg-[#10b481]/10 border border-[#10b481]/20 rounded-2xl flex items-center justify-center mb-4 group-hover:bg-[#10b481]/20 transition-all duration-300">
            <i class="bx bx-map-alt text-[#10b481] text-xl"></i>
          </div>
          <div class="flex items-end gap-0.5 mb-2">
            <span class="text-4xl font-black text-[#10b481] leading-none tabular-nums">{{ counts.hectares }}</span>
            <span class="text-[#10b481] font-black text-xl leading-none mb-0.5 ml-1">ha</span>
          </div>
          <p class="text-[10px] font-black uppercase tracking-widest text-gray-400">{{ $t('stats.hectares') }}</p>
        </div>

        <!-- Traçabilité -->
        <div class="flex flex-col items-center text-center group">
          <div class="w-12 h-12 bg-[#10b481]/10 border border-[#10b481]/20 rounded-2xl flex items-center justify-center mb-4 group-hover:bg-[#10b481]/20 transition-all duration-300">
            <i class="bx bx-check-shield text-[#10b481] text-xl"></i>
          </div>
          <div class="flex items-end gap-0.5 mb-2">
            <span class="text-4xl font-black text-[#10b481] leading-none tabular-nums">100</span>
            <span class="text-[#10b481] font-black text-2xl leading-none mb-0.5">%</span>
          </div>
          <p class="text-[10px] font-black uppercase tracking-widest text-gray-400">{{ $t('stats.traceability') }}</p>
        </div>

      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue"

const localePath = useLocalePath()

// Animated counter
const counts = ref({ farmers: 0, cooperatives: 0, hectares: 0 })
const targets = { farmers: 50, cooperatives: 50, hectares: 210 }

function animateCount(key: keyof typeof targets, duration = 1200) {
  const start = performance.now()
  const target = targets[key]
  const step = (now: number) => {
    const elapsed = now - start
    const progress = Math.min(elapsed / duration, 1)
    // Ease out cubic
    const eased = 1 - Math.pow(1 - progress, 3)
    counts.value[key] = Math.round(eased * target)
    if (progress < 1) requestAnimationFrame(step)
  }
  requestAnimationFrame(step)
}

onMounted(() => {
  // Trigger animation when section enters viewport
  const el = document.getElementById("stats-section-trigger")
  if (!el) {
    // Fallback: animate immediately with slight delay
    setTimeout(() => {
      animateCount("farmers", 1400)
      setTimeout(() => animateCount("cooperatives", 1400), 150)
      setTimeout(() => animateCount("hectares", 1600), 300)
    }, 300)
    return
  }
  const observer = new IntersectionObserver((entries) => {
    if (entries[0]?.isIntersecting) {
      animateCount("farmers", 1400)
      setTimeout(() => animateCount("cooperatives", 1400), 150)
      setTimeout(() => animateCount("hectares", 1600), 300)
      observer.disconnect()
    }
  }, { threshold: 0.3 })
  observer.observe(el)
})
</script>