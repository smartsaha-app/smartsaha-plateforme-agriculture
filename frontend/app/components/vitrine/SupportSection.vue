<template>
  <section id="support-ecosystem" class="py-32 bg-[#fcfdfd]">
    <div class="max-w-7xl mx-auto px-6">
      <!-- Introduction Section -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center mb-24">
        <div class="space-y-8">
          <div class="inline-flex items-center gap-2 px-4 py-2 bg-[#10b481]/10 rounded-full">
            <span class="w-1.5 h-1.5 rounded-full bg-[#10b481] animate-pulse"></span>
            <span class="text-[10px] font-black uppercase tracking-[0.2em] text-[#10b481]">{{ $t('support_page.badge') }}</span>
          </div>
          <h2 class="text-4xl md:text-6xl font-black text-[#112830] tracking-tight leading-[1.1]">
            {{ $t('support_page.title') }}
          </h2>
          <p class="text-lg text-gray-500 font-medium leading-relaxed">
            {{ $t('support_page.description') }}
          </p>
        </div>
        <div class="relative group">
          <div class="absolute inset-0 bg-[#10b481]/5 rounded-[3rem] blur-3xl group-hover:bg-[#10b481]/10 transition-all duration-1000"></div>
          <img 
            src="/support_ecosystem_hybrid_1775824592559.png" 
            alt="Écosystème hybride SmartSaha" 
            class="relative w-full aspect-[16/9] object-cover rounded-[3rem] shadow-2xl border border-gray-100 group-hover:scale-[1.01] transition-all duration-1000"
          />
          <!-- Badge flottant -->
          <div class="absolute -bottom-6 -left-6 bg-white p-6 rounded-3xl shadow-xl border border-gray-100 flex items-center gap-4">
             <div class="w-12 h-12 bg-[#112830] rounded-2xl flex items-center justify-center text-[#10b481]">
                <i class="bx bx-sync text-2xl animate-spin-slow"></i>
             </div>
             <div class="flex flex-col">
                <span class="text-[10px] font-black uppercase tracking-widest text-gray-400">Sync. Temps Réel</span>
                <span class="text-xs font-bold text-[#112830]">Web & Mobile connectés</span>
             </div>
          </div>
        </div>
      </div>

      <!-- Ecosystem Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
        <!-- Web Platform Card -->
        <div class="group bg-white p-10 md:p-14 rounded-[3rem] border border-gray-100 hover:border-[#10b481]/20 hover:shadow-2xl transition-all duration-500 relative overflow-hidden">
          <div class="absolute -top-10 -right-10 opacity-5 group-hover:opacity-10 transition-all duration-700">
            <i class="bx bx-laptop text-[240px] text-[#112830]"></i>
          </div>
          
          <div class="space-y-8 relative z-10">
            <div class="w-20 h-20 bg-[#f7faf9] rounded-3xl flex items-center justify-center text-[#10b481] shadow-inner mb-6 group-hover:scale-110 transition-transform duration-500">
              <i class="bx bx-laptop text-4xl"></i>
            </div>
            
            <div class="space-y-2">
              <h3 class="text-3xl font-black text-[#112830]">{{ $t('support_page.web_title') }}</h3>
              <p class="text-[11px] font-bold text-[#10b481] uppercase tracking-[0.2em]">{{ $t('support_page.web_subtitle') }}</p>
            </div>

            <p class="text-[15px] text-gray-500 font-medium leading-relaxed max-w-md">
              {{ $t('support_page.web_desc') }}
            </p>

            <ul class="space-y-4 pt-4">
              <li v-for="(feature, index) in $tm('support_page.web_features')" :key="index" class="flex items-center gap-4 group/item">
                <div class="w-6 h-6 rounded-full bg-[#10b481]/10 flex items-center justify-center text-[#10b481] group-hover/item:bg-[#10b481] group-hover/item:text-white transition-all">
                  <i class="bx bx-check text-base"></i>
                </div>
                <span class="text-sm font-bold text-[#112830] opacity-80 group-hover/item:opacity-100 transition-opacity">{{ $rt(feature) }}</span>
              </li>
            </ul>

            <div class="pt-8">
               <NuxtLink to="/login" class="inline-flex items-center gap-3 text-sm font-black text-[#112830] uppercase tracking-widest hover:gap-5 transition-all">
                Accéder à la plateforme <i class="bx bx-right-arrow-alt text-2xl text-[#10b481]"></i>
              </NuxtLink>
            </div>
          </div>
        </div>

        <!-- Mobile App Card -->
        <div class="group bg-[#112830] p-10 md:p-14 rounded-[3rem] text-white hover:shadow-2xl hover:shadow-black/20 transition-all duration-500 relative overflow-hidden">
          <div class="absolute -top-10 -right-10 opacity-10 group-hover:opacity-20 transition-all duration-700">
            <i class="bx bx-mobile-alt text-[240px] text-white"></i>
          </div>

          <div class="space-y-8 relative z-10">
            <div class="w-20 h-20 bg-white/5 rounded-3xl flex items-center justify-center text-[#10b481] shadow-inner mb-6 group-hover:scale-110 transition-transform duration-500">
              <i class="bx bx-mobile-alt text-4xl"></i>
            </div>

            <div class="space-y-2">
              <h3 class="text-3xl font-black text-white">{{ $t('support_page.mobile_title') }}</h3>
              <p class="text-[11px] font-bold text-[#10b481] uppercase tracking-[0.2em]">{{ $t('support_page.mobile_subtitle') }}</p>
            </div>

            <p class="text-[15px] text-gray-400 font-medium leading-relaxed max-w-md">
              {{ $t('support_page.mobile_desc') }}
            </p>

            <ul class="space-y-4 pt-4">
              <li v-for="(feature, index) in $tm('support_page.mobile_features')" :key="index" class="flex items-center gap-4 group/item">
                <div class="w-6 h-6 rounded-full bg-white/10 flex items-center justify-center text-[#10b481] group-hover/item:bg-[#10b481] group-hover/item:text-white transition-all">
                  <i class="bx bx-check text-base"></i>
                </div>
                <span class="text-sm font-bold text-gray-300 group-hover/item:text-white transition-colors">{{ $rt(feature) }}</span>
              </li>
            </ul>

            <div class="pt-8 space-y-6">
              <p class="text-[10px] font-black uppercase tracking-[0.2em] text-[#10b481]">{{ $t('support_page.cta_mobile') }}</p>
              <div class="flex flex-wrap gap-4">
                <a href="#" class="flex items-center gap-3 px-6 py-4 bg-white/5 hover:bg-white/10 border border-white/10 rounded-2xl transition-all group/btn">
                  <i class="bx bxl-play-store text-2xl"></i>
                  <div class="text-left">
                    <p class="text-[8px] font-bold uppercase opacity-60 leading-none mb-1">Get it on</p>
                    <p class="text-xs font-black leading-none">Google Play</p>
                  </div>
                </a>
                <a href="#" class="flex items-center gap-3 px-6 py-4 bg-white/5 hover:bg-white/10 border border-white/10 rounded-2xl transition-all group/btn">
                  <i class="bx bxl-apple text-2xl"></i>
                  <div class="text-left">
                    <p class="text-[8px] font-bold uppercase opacity-60 leading-none mb-1">Download on</p>
                    <p class="text-xs font-black leading-none">App Store</p>
                  </div>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
// Pas de logique spécifique nécessaire, tout passe par i18n
</script>

<style scoped>
/* Effets de survol additionnels si nécessaire */
</style>
