<template>
  <section id="about" class="relative pt-32 pb-20 md:pt-36 md:pb-36 overflow-hidden">
    <!-- Background elements -->
    <div class="absolute top-0 right-0 -translate-y-1/4 translate-x-1/4 w-[700px] h-[700px] bg-[#10b481]/5 rounded-full blur-[120px] pointer-events-none"></div>
    <div class="absolute bottom-0 left-0 translate-y-1/4 -translate-x-1/4 w-[400px] h-[400px] bg-[#112830]/5 rounded-full blur-3xl pointer-events-none"></div>

    <div class="max-w-7xl mx-auto px-6 grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">

      <!-- Left: Copy -->
      <div class="space-y-8 relative z-10">
        <!-- Badge -->
        <div class="inline-flex items-center gap-2 px-4 py-2 bg-[#10b481]/10 border border-[#10b481]/15 rounded-full">
          <span class="relative flex h-2 w-2" aria-hidden="true">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#10b481] opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2 w-2 bg-[#10b481]"></span>
          </span>
          <span class="text-xs font-black uppercase tracking-widest text-[#10b481]">{{ $t('hero.badge') }}</span>
        </div>

        <!-- Headline -->
        <h1 class="text-5xl md:text-[4.2rem] font-black text-[#112830] leading-[1.08] tracking-tight">
          {{ $t('hero.title_1') }}
          <span class="text-[#10b481] relative">
            {{ $t('hero.title_highlight') }}
            <svg class="absolute -bottom-2 left-0 w-full" height="6" viewBox="0 0 200 6" preserveAspectRatio="none" aria-hidden="true">
              <path d="M0 5 Q50 0 100 4 Q150 8 200 3" stroke="#10b481" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.5"/>
            </svg>
          </span>
          {{ $t('hero.title_2') }}
        </h1>

        <!-- Description -->
        <p class="text-lg md:text-xl text-gray-500 font-medium leading-relaxed max-w-lg">
          {{ $t('hero.description') }}
        </p>

        <!-- CTAs -->
        <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-4 pt-4">
          <NuxtLink
            :to="localePath('/signup')"
            class="inline-flex items-center justify-center whitespace-nowrap px-8 py-4 bg-[#10b481] text-white rounded-3xl font-black text-sm uppercase tracking-widest shadow-2xl shadow-[#10b481]/30 hover:-translate-y-1 hover:shadow-[#10b481]/40 active:scale-95 transition-all"
          >
            {{ $t('hero.cta_start') }}
          </NuxtLink>
          <NuxtLink
            :to="localePath('/sesily-ai')"
            class="inline-flex items-center justify-center gap-2 whitespace-nowrap px-8 py-4 bg-[#112830] hover:bg-[#10b481] text-white rounded-3xl font-black text-sm uppercase tracking-widest active:scale-95 transition-all shadow-xl shadow-[#112830]/20"
          >
            <i class="bx bx-robot text-base flex-shrink-0" aria-hidden="true"></i>
            <span>{{ $t('hero.sesily_badge') }}</span>
          </NuxtLink>
        </div>
      </div>

      <!-- Right: Image + floating cards -->
      <div class="relative group">
        <!-- Image glow -->
        <div class="absolute inset-0 bg-gradient-to-tr from-[#10b481]/20 to-transparent rounded-[3rem] blur-2xl group-hover:blur-3xl transition-all duration-700 pointer-events-none"></div>

        <img
          src="/hero_premium.png"
          alt="Agriculteur moderne Madagascar utilisant SmartSaha"
          class="relative w-full aspect-[4/5] object-cover rounded-[3rem] shadow-2xl grayscale-[10%] group-hover:grayscale-0 transition-all duration-1000"
        />

        <!-- Floating card — Sesily AI (bottom left) -->
        <NuxtLink :to="localePath('/sesily-ai')"
          class="absolute -bottom-6 -left-6 bg-[#112830]/95 backdrop-blur-xl p-5 rounded-3xl shadow-2xl border border-[#10b481]/20 max-w-[230px] animate-bounce-slow z-10 hover:border-[#10b481]/50 transition-all group/sesily"
          :aria-label="$t('hero.sesily_card_title')"
        >
          <div class="flex items-center gap-3 mb-2">
            <div class="w-9 h-9 rounded-xl bg-[#10b481] flex items-center justify-center text-white flex-shrink-0 group-hover/sesily:scale-110 transition-transform">
              <i class="bx bx-robot text-lg" aria-hidden="true"></i>
            </div>
            <div>
              <p class="text-xs font-black text-[#10b481] uppercase tracking-widest leading-none mb-0.5">{{ $t('hero.sesily_card_title') }}</p>
              <p class="text-xs font-bold text-white/70 leading-tight">{{ $t('hero.sesily_card_text') }}</p>
            </div>
          </div>
          <div class="flex items-center gap-1.5 mt-2">
            <span class="relative flex h-2 w-2" aria-hidden="true">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#10b481] opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2 w-2 bg-[#10b481]"></span>
            </span>
            <span class="text-xs font-black text-white/50 uppercase tracking-widest">Live</span>
          </div>
        </NuxtLink>

        <!-- Floating card — top right (fire alert) -->
        <NuxtLink :to="localePath('/fires')"
          class="absolute -top-4 -right-4 bg-[#1c0800]/90 backdrop-blur-xl px-4 py-3 rounded-2xl shadow-xl border border-orange-500/20 flex items-center gap-3 z-10 hover:border-orange-500/40 transition-all group/fire"
          :aria-label="$t('hero.alert_title')"
        >
          <span class="relative flex h-2 w-2 flex-shrink-0" aria-hidden="true">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-orange-500 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2 w-2 bg-orange-400"></span>
          </span>
          <div>
            <p class="text-xs font-black text-orange-500/70 uppercase tracking-widest leading-none mb-0.5">NASA FIRMS</p>
            <p class="text-sm font-black text-orange-300 group-hover/fire:text-orange-200 transition-colors">Incendies · Live</p>
          </div>
          <i class="bx bxs-flame text-orange-400 text-xl animate-pulse" aria-hidden="true"></i>
        </NuxtLink>
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
  50% { transform: translateY(-14px); }
}
.animate-bounce-slow {
  animation: bounce-slow 5s infinite ease-in-out;
}
</style>