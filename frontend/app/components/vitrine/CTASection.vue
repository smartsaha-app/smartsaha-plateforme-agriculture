<template>
  <section class="relative py-32 overflow-hidden">
    <!-- Background Image with Overlay -->
    <div class="absolute inset-0 z-0">
      <img 
        src="/cta_premium.png" 
        alt="Future Vision" 
        class="w-full h-full object-cover scale-110"
      />
      <div class="absolute inset-0 bg-gradient-to-b from-[#112830]/90 to-[#112830]/70 backdrop-blur-[2px]"></div>
    </div>

    <div class="relative z-10 max-w-7xl mx-auto px-6 text-center space-y-12">
      <div class="w-20 h-20 bg-[#10b481]/20 rounded-full flex items-center justify-center mx-auto mb-8 border border-[#10b481]/30">
        <i class="bx bxs-paper-plane text-4xl text-[#10b481] animate-pulse"></i>
      </div>
      
      <h2 class="text-4xl md:text-6xl font-black text-white tracking-tight max-w-4xl mx-auto leading-tight">
        {{ $t('cta_final.title') }}
      </h2>
      
      <p class="text-white/60 font-medium text-lg max-w-2xl mx-auto">
        Rejoignez des milliers d'agriculteurs et d'organisations qui transforment déjà le paysage agricole malgache.
      </p>

      <div class="flex flex-col sm:flex-row justify-center items-center gap-6 pt-4">
        <NuxtLink to="/signup" class="group relative px-12 py-6 bg-[#10b481] text-white rounded-3xl font-black text-xs uppercase tracking-[0.2em] shadow-2xl shadow-[#10b481]/40 hover:-translate-y-1 transition-all">
          <span class="relative z-10">{{ $t('cta_final.free_account') }}</span>
          <div class="absolute inset-0 bg-white/20 rounded-3xl scale-x-0 group-hover:scale-x-100 transition-transform origin-left"></div>
        </NuxtLink>
        
        <NuxtLink to="/login" class="px-12 py-6 bg-white/10 backdrop-blur-md text-white border border-white/20 rounded-3xl font-black text-xs uppercase tracking-[0.2em] hover:bg-white/20 transition-all">
          {{ $t('cta_final.access_space') }}
        </NuxtLink>
      </div>
    </div>
  </section>
</template>
