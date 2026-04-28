<template>
  <section id="about" class="relative pt-32 pb-20 md:pt-30 md:pb-32 overflow-hidden">
    <!-- Background elements -->
    <div class="absolute top-0 right-0 -translate-y-1/4 translate-x-1/4 w-[600px] h-[600px] bg-[#10b481]/5 rounded-full blur-3xl pointer-events-none"></div>
    <div class="absolute bottom-0 left-0 translate-y-1/4 -translate-x-1/4 w-[400px] h-[400px] bg-[#112830]/5 rounded-full blur-3xl pointer-events-none"></div>

    <div class="max-w-7xl mx-auto px-6 grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
      <div class="space-y-8 relative z-10">
        <div class="inline-flex items-center gap-2 px-4 py-2 bg-[#10b481]/10 rounded-full">
          <span class="w-2 h-2 bg-[#10b481] rounded-full animate-ping"></span>
          <span class="text-[10px] font-black uppercase tracking-widest text-[#10b481]">{{ $t('hero.badge') }}</span>
        </div>
        <h1 class="text-5xl md:text-7xl font-black text-[#112830] leading-[1.1] tracking-tight">
          {{ $t('hero.title_1') }} <span class="text-[#10b481]">{{ $t('hero.title_highlight') }}</span> {{ $t('hero.title_2') }}
        </h1>
        <p class="text-lg md:text-xl text-gray-500 font-medium leading-relaxed max-w-lg">
          {{ $t('hero.description') }}
        </p>
        <div class="flex flex-col sm:flex-row items-center gap-4 pt-4">
          <NuxtLink to="/signup" class="w-full sm:w-auto px-10 py-5 bg-[#10b481] text-white rounded-3xl font-black text-xs uppercase tracking-[0.2em] shadow-2xl shadow-[#10b481]/30 hover:-translate-y-1 transition-all">
            {{ $t('hero.cta_start') }}
          </NuxtLink>
        </div>
      </div>

      <div class="relative group">
        <div class="absolute inset-0 bg-gradient-to-tr from-[#10b481]/20 to-transparent rounded-[3rem] blur-2xl group-hover:blur-3xl transition-all duration-700"></div>
        <img 
          src="/hero_premium.png" 
          alt="Modern Farmer Madagascar" 
          class="relative w-full aspect-[4/5] object-cover rounded-[3rem] shadow-2xl grayscale-[20%] group-hover:grayscale-0 transition-all duration-1000"
        />
        <!-- Floating UI Card -->
        <div class="absolute -bottom-6 -left-6 bg-white/90 backdrop-blur-xl p-6 rounded-3xl shadow-2xl border border-white/50 max-w-[240px] animate-bounce-slow">
          <div class="flex items-center gap-4 mb-4">
            <div class="w-10 h-10 rounded-xl bg-green-500 flex items-center justify-center text-white">
              <i class="bx bxs-bolt text-xl"></i>
            </div>
            <div>
              <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest leading-none mb-1">{{ $t('hero.alert_title') }}</p>
              <p class="text-sm font-black text-[#112830]">{{ $t('hero.alert_subtitle') }}</p>
            </div>
          </div>
          <p class="text-gray-500 text-[11px] font-bold leading-relaxed">
            {{ $t('hero.alert_text') }}
          </p>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
@keyframes bounce-slow {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-15px); }
}
.animate-bounce-slow {
  animation: bounce-slow 5s infinite ease-in-out;
}
</style>
