<template>
  <section id="features" class="py-32 bg-[#fcfdfd]">
    <div class="max-w-7xl mx-auto px-6">

      <!-- Section Intro -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center mb-32">
        <div class="space-y-8">
          <div class="inline-flex items-center gap-2 px-4 py-2 bg-[#10b481]/10 rounded-full">
            <span class="w-1.5 h-1.5 rounded-full bg-[#10b481] animate-pulse" aria-hidden="true"></span>
            <span class="text-xs font-black uppercase tracking-[0.2em] text-[#10b481]">{{ $t('features.badge') }}</span>
          </div>
          <h2 class="text-4xl md:text-6xl font-black text-[#112830] tracking-tight leading-[1.1]">
            {{ $t('features.title') }}
          </h2>
          <p class="text-lg text-gray-500 font-medium leading-relaxed">
            {{ $t('features.description') }}
          </p>
          <div class="pt-4">
            <NuxtLink :to="localePath('/signup')" class="inline-flex items-center gap-4 px-10 py-5 bg-[#112830] text-white rounded-2xl font-black text-sm uppercase tracking-widest hover:scale-105 transition-all shadow-2xl shadow-[#112830]/20">
              {{ $t('features.cta_start') }} <i class="bx bx-right-arrow-alt text-xl text-[#10b481]" aria-hidden="true"></i>
            </NuxtLink>
          </div>
        </div>
        <div class="relative group">
          <div class="absolute inset-0 bg-gradient-to-tr from-[#10b481]/20 to-transparent rounded-[3rem] blur-2xl group-hover:blur-3xl transition-all duration-1000" aria-hidden="true"></div>
          <img
            src="/features_intro_tech_agri_1775824362754.png"
            alt="Agriculture de précision Madagascar — SmartSaha"
            class="relative w-full aspect-[4/3] object-cover rounded-[3rem] shadow-2xl border border-white/50 group-hover:scale-[1.02] transition-all duration-1000"
          />
          <div class="absolute -bottom-6 -right-6 bg-white p-6 rounded-3xl shadow-xl border border-gray-100 max-w-[200px] animate-bounce-slow" aria-hidden="true">
            <div class="flex items-center gap-3 mb-2">
              <i class="bx bx-radar text-2xl text-[#10b481]"></i>
              <span class="text-xs font-black uppercase tracking-widest text-[#112830]">Scan en direct</span>
            </div>
            <p class="text-xs text-gray-400 font-bold">Analyse NDVI active sur la parcelle B-04</p>
          </div>
        </div>
      </div>

      <!-- Grille des fonctionnalités -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">

        <!-- Card 1: GPS & Satellite -->
        <div class="bg-white p-10 rounded-[3rem] border border-gray-100 hover:border-[#10b481]/30 hover:shadow-2xl hover:shadow-[#10b481]/5 transition-all group relative overflow-hidden">
          <div class="absolute top-0 right-0 w-32 h-32 bg-gray-50 rounded-bl-[5rem] -mr-10 -mt-10 group-hover:bg-[#10b481]/5 transition-colors" aria-hidden="true"></div>
          <div class="w-16 h-16 bg-[#112830] text-white rounded-2xl flex items-center justify-center mb-8 group-hover:bg-[#10b481] transition-all duration-500 relative z-10 shadow-lg shadow-[#112830]/10 group-hover:rotate-6">
            <i class="bx bx-map-alt text-3xl" aria-hidden="true"></i>
          </div>
          <h3 class="text-2xl font-black text-[#112830] mb-4 tracking-tight relative z-10">{{ $t('features.items.precision.title') }}</h3>
          <p class="text-gray-500 text-sm font-medium leading-relaxed relative z-10 mb-6">{{ $t('features.items.precision.desc') }}</p>
          <div class="flex items-center gap-2 text-[#10b481] font-black text-xs uppercase tracking-widest opacity-0 group-hover:opacity-100 transition-all translate-y-4 group-hover:translate-y-0">
            {{ $t('features.items.precision.label') }} <i class="bx bx-check-double text-base" aria-hidden="true"></i>
          </div>
        </div>

        <!-- Card 2: SESILY AI — Mise en avant spéciale -->
        <NuxtLink :to="localePath('/sesily-ai')"
          class="bg-gradient-to-br from-[#112830] to-[#0d1f25] p-10 rounded-[3rem] border border-[#10b481]/20 hover:border-[#10b481]/60 hover:shadow-2xl hover:shadow-[#10b481]/20 transition-all group relative overflow-hidden lg:mt-12 block"
          aria-label="Découvrir Sesily AI"
        >
          <!-- Glow background -->
          <div class="absolute inset-0 bg-[#10b481]/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500 rounded-[3rem]" aria-hidden="true"></div>
          <div class="w-16 h-16 bg-[#10b481] text-white rounded-2xl flex items-center justify-center mb-8 transition-all duration-500 relative z-10 shadow-lg shadow-[#10b481]/30 group-hover:-rotate-6 group-hover:scale-110">
            <i class="bx bx-robot text-3xl" aria-hidden="true"></i>
          </div>
          <h3 class="text-2xl font-black text-white mb-2 tracking-tight relative z-10">Sesily AI</h3>
          <p class="text-xs font-black text-[#10b481] uppercase tracking-widest mb-4 relative z-10">{{ $t('features.items.ai.label') }}</p>
          <p class="text-gray-400 text-sm font-medium leading-relaxed relative z-10 mb-6">{{ $t('features.items.ai.desc') }}</p>
          <div class="flex items-center gap-2 text-[#10b481] font-black text-sm uppercase tracking-widest relative z-10 group-hover:gap-4 transition-all">
            {{ $t('features.sesily_cta') }} <i class="bx bx-right-arrow-alt text-xl" aria-hidden="true"></i>
          </div>
        </NuxtLink>

        <!-- Card 3: Marketplace — Achat & Vente -->
        <div class="bg-white p-10 rounded-[3rem] border border-gray-100 hover:border-[#10b481]/30 hover:shadow-2xl hover:shadow-[#10b481]/5 transition-all group relative overflow-hidden">
          <div class="absolute top-0 right-0 w-32 h-32 bg-gray-50 rounded-bl-[5rem] -mr-10 -mt-10 group-hover:bg-[#10b481]/5 transition-colors" aria-hidden="true"></div>
          <div class="w-16 h-16 bg-[#112830] text-white rounded-2xl flex items-center justify-center mb-8 group-hover:bg-[#10b481] transition-all duration-500 relative z-10 shadow-lg shadow-[#112830]/10 group-hover:rotate-6">
            <i class="bx bx-store-alt text-3xl" aria-hidden="true"></i>
          </div>
          <h3 class="text-2xl font-black text-[#112830] mb-4 tracking-tight relative z-10">{{ $t('features.items.marketplace.title') }}</h3>
          <p class="text-gray-500 text-sm font-medium leading-relaxed relative z-10 mb-5">{{ $t('features.items.marketplace.desc') }}</p>
          <div class="flex items-center gap-2 text-[#10b481] font-black text-xs uppercase tracking-widest opacity-0 group-hover:opacity-100 transition-all translate-y-4 group-hover:translate-y-0 relative z-10">
            {{ $t('features.items.marketplace.label') }} <i class="bx bx-check-double text-base" aria-hidden="true"></i>
          </div>
        </div>

        <!-- Card 4: Rendements -->
        <div class="bg-white p-10 rounded-[3rem] border border-gray-100 hover:border-[#10b481]/30 hover:shadow-2xl hover:shadow-[#10b481]/5 transition-all group relative overflow-hidden">
          <div class="absolute top-0 right-0 w-32 h-32 bg-gray-50 rounded-bl-[5rem] -mr-10 -mt-10 group-hover:bg-[#10b481]/5 transition-colors" aria-hidden="true"></div>
          <div class="w-16 h-16 bg-[#112830] text-white rounded-2xl flex items-center justify-center mb-8 group-hover:bg-[#10b481] transition-all duration-500 relative z-10 shadow-lg shadow-[#112830]/10 group-hover:-rotate-6">
            <i class="bx bx-line-chart text-3xl" aria-hidden="true"></i>
          </div>
          <h3 class="text-2xl font-black text-[#112830] mb-4 tracking-tight relative z-10">{{ $t('features.items.yield.title') }}</h3>
          <p class="text-gray-500 text-sm font-medium leading-relaxed relative z-10 mb-6">{{ $t('features.items.yield.desc') }}</p>
          <div class="flex items-center gap-2 text-[#10b481] font-black text-xs uppercase tracking-widest opacity-0 group-hover:opacity-100 transition-all translate-y-4 group-hover:translate-y-0">
            {{ $t('features.items.yield.label') }} <i class="bx bx-check-double text-base" aria-hidden="true"></i>
          </div>
        </div>

        <!-- Card 5: Tâches -->
        <div class="bg-white p-10 rounded-[3rem] border border-gray-100 hover:border-[#10b481]/30 hover:shadow-2xl hover:shadow-[#10b481]/5 transition-all group relative overflow-hidden lg:mt-12">
          <div class="absolute top-0 right-0 w-32 h-32 bg-gray-50 rounded-bl-[5rem] -mr-10 -mt-10 group-hover:bg-[#10b481]/5 transition-colors" aria-hidden="true"></div>
          <div class="w-16 h-16 bg-[#112830] text-white rounded-2xl flex items-center justify-center mb-8 group-hover:bg-[#10b481] transition-all duration-500 relative z-10 shadow-lg shadow-[#112830]/10 group-hover:rotate-6">
            <i class="bx bx-calendar-check text-3xl" aria-hidden="true"></i>
          </div>
          <h3 class="text-2xl font-black text-[#112830] mb-4 tracking-tight relative z-10">{{ $t('features.items.tasks.title') }}</h3>
          <p class="text-gray-500 text-sm font-medium leading-relaxed relative z-10 mb-6">{{ $t('features.items.tasks.desc') }}</p>
          <div class="flex items-center gap-2 text-[#10b481] font-black text-xs uppercase tracking-widest opacity-0 group-hover:opacity-100 transition-all translate-y-4 group-hover:translate-y-0">
            {{ $t('features.items.tasks.label') }} <i class="bx bx-check-double text-base" aria-hidden="true"></i>
          </div>
        </div>

        <!-- Card 6: CTA Final -->
        <div class="bg-[#112830] p-10 rounded-[3rem] flex flex-col justify-center items-center text-center space-y-6 group hover:scale-[1.02] transition-all duration-500 shadow-2xl shadow-[#112830]/20 min-h-[400px]">
          <h3 class="text-3xl font-black text-white px-2">{{ $t('features.cta_final.title') }}</h3>
          <p class="text-gray-400 text-sm font-medium">{{ $t('features.cta_final.subtitle') }}</p>
          <NuxtLink :to="localePath('/signup')" class="inline-flex items-center justify-center whitespace-nowrap px-8 py-4 bg-[#10b481] text-white rounded-2xl font-black text-sm uppercase tracking-widest hover:rotate-2 transition-all">
            {{ $t('features.cta_final.btn') }}
          </NuxtLink>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const localePath = useLocalePath()
</script>

<style scoped>
@keyframes bounce-slow {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}
.animate-bounce-slow {
  animation: bounce-slow 4s infinite ease-in-out;
}
</style>