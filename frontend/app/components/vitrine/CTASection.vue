<template>
  <section class="relative py-32 overflow-hidden">
    <div class="absolute inset-0 z-0" aria-hidden="true">
      <img src="/cta_premium.png" alt="" class="w-full h-full object-cover scale-110" />
      <div class="absolute inset-0 bg-gradient-to-b from-[#112830]/90 to-[#112830]/70 backdrop-blur-[2px]"></div>
    </div>

    <div class="relative z-10 max-w-7xl mx-auto px-6 text-center space-y-12">

      <div class="w-20 h-20 bg-[#10b481]/20 rounded-full flex items-center justify-center mx-auto border border-[#10b481]/30">
        <i class="bx bx-robot text-4xl text-[#10b481] animate-pulse" aria-hidden="true"></i>
      </div>

      <h2 class="text-4xl md:text-6xl font-black text-white tracking-tight max-w-4xl mx-auto leading-tight">
        {{ $t('cta_final.title') }}
      </h2>

      <p class="text-white/70 font-medium text-lg max-w-2xl mx-auto">
        {{ $t('cta_final.cta_subtitle') }}
      </p>

      <div class="flex flex-col sm:flex-row justify-center items-center gap-4 pt-2">
        <!-- Sesily AI — CTA principal -->
        <NuxtLink :to="localePath('/sesily-ai')"
          class="group relative px-10 py-6 bg-[#10b481] text-white rounded-3xl font-black text-sm uppercase tracking-[0.18em] shadow-2xl shadow-[#10b481]/40 hover:-translate-y-1 transition-all flex items-center gap-3 overflow-hidden">
          <i class="bx bx-robot text-lg" aria-hidden="true"></i>
          <span class="relative z-10">{{ $t('cta_final.try_sesily') }}</span>
          <div class="absolute inset-0 bg-white/20 rounded-3xl scale-x-0 group-hover:scale-x-100 transition-transform origin-left" aria-hidden="true"></div>
        </NuxtLink>

        <!-- Créer compte -->
        <NuxtLink :to="localePath('/signup')"
          class="px-10 py-6 bg-white/10 backdrop-blur-md text-white border border-white/20 rounded-3xl font-black text-sm uppercase tracking-[0.18em] hover:bg-white/20 transition-all">
          {{ $t('cta_final.free_account') }}
        </NuxtLink>
      </div>

    </div>
  </section>
</template>

<script setup lang="ts">
const localePath = useLocalePath()
</script>