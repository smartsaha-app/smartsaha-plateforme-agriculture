<template>
  <div>
    <!-- Page d'accueil épurée pour attirer l'attention -->
    <VitrineHeroSection />
    
    <!-- Points clés rapides -->
    <VitrineStatsSection />
    
    <!-- Un petit teaser des fonctionnalités -->
    <section class="py-24 bg-white">
      <div class="max-w-7xl mx-auto px-6 text-center space-y-16">
        <div class="max-w-3xl mx-auto space-y-4">
          <h2 class="text-4xl md:text-5xl font-black text-[#112830] tracking-tight">
            {{ $t('features.badge') }}
          </h2>
          <p class="text-gray-500 font-medium">
            {{ $t('features.description') }}
          </p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="p-10 bg-gray-50 rounded-[3rem] space-y-6 hover:scale-105 transition-transform">
             <div class="w-16 h-16 bg-[#10b481] text-white rounded-2xl flex items-center justify-center mx-auto shadow-lg shadow-[#10b481]/20">
                <i class="bx bx-leaf text-3xl"></i>
             </div>
             <h3 class="text-xl font-black text-[#112830]">{{ $t('features.items.precision.title') }}</h3>
             <p class="text-sm text-gray-500 font-medium leading-relaxed">{{ $t('features.items.precision.desc') }}</p>
          </div>
          <div class="p-10 bg-gray-50 rounded-[3rem] space-y-6 hover:scale-105 transition-transform">
             <div class="w-16 h-16 bg-[#112830] text-white rounded-2xl flex items-center justify-center mx-auto shadow-lg shadow-[#112830]/20">
                <i class="bx bx-store-alt text-3xl"></i>
             </div>
             <h3 class="text-xl font-black text-[#112830]">{{ $t('features.items.marketplace.title') }}</h3>
             <p class="text-sm text-gray-500 font-medium leading-relaxed">{{ $t('features.items.marketplace.desc') }}</p>
          </div>
          <div class="p-10 bg-gray-50 rounded-[3rem] space-y-6 hover:scale-105 transition-transform">
             <div class="w-16 h-16 bg-[#112830] text-white rounded-2xl flex items-center justify-center mx-auto shadow-lg shadow-[#112830]/20">
                <i class="bx bx-bot text-3xl"></i>
             </div>
             <h3 class="text-xl font-black text-[#112830]">{{ $t('features.items.ai.title') }}</h3>
             <p class="text-sm text-gray-500 font-medium leading-relaxed">{{ $t('features.items.ai.desc') }}</p>
          </div>
          <div class="p-10 bg-gray-50 rounded-[3rem] space-y-6 hover:scale-105 transition-transform">
             <div class="w-16 h-16 bg-[#112830] text-white rounded-2xl flex items-center justify-center mx-auto shadow-lg shadow-[#112830]/20">
                <i class="bx bx-line-chart text-3xl"></i>
             </div>
             <h3 class="text-xl font-black text-[#112830]">{{ $t('features.items.yield.title') }}</h3>
             <p class="text-sm text-gray-500 font-medium leading-relaxed">{{ $t('features.items.yield.desc') }}</p>
          </div>

          <!-- Card Alerte Feu -->
          <NuxtLink
            :to="localePath('/fires')"
            class="p-10 bg-orange-50 rounded-[3rem] space-y-6 hover:scale-105 transition-transform border border-orange-100 hover:border-orange-200 group block"
          >
            <div class="relative w-16 h-16 mx-auto">
              <!-- Ping live -->
              <span class="absolute -top-1 -right-1 flex h-3 w-3 z-10">
                <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-orange-500 opacity-60"></span>
                <span class="relative inline-flex rounded-full h-3 w-3 bg-orange-500"></span>
              </span>
              <div class="w-16 h-16 bg-orange-500 text-white rounded-2xl flex items-center justify-center shadow-lg shadow-orange-500/30 group-hover:rotate-6 transition-transform duration-300">
                <i class="bx bxs-flame text-3xl"></i>
              </div>
            </div>
            <div class="space-y-2">
              <div class="inline-flex items-center gap-1.5 px-2.5 py-1 bg-orange-100 text-orange-700 text-[9px] font-black uppercase tracking-widest rounded-full">
                NASA FIRMS · Live
              </div>
              <h3 class="text-xl font-black text-[#112830]">Alerte Incendie</h3>
              <p class="text-sm text-gray-500 font-medium leading-relaxed">
                Détection des feux actifs à Madagascar par satellite MODIS (NASA) en temps réel.
              </p>
            </div>
            <div class="flex items-center gap-2 text-orange-500 font-black text-[10px] uppercase tracking-widest group-hover:gap-3 transition-all">
              Voir la carte <i class="bx bx-right-arrow-alt text-base"></i>
            </div>
          </NuxtLink>

          <!-- Card Alerte Météo -->
          <div class="p-10 bg-sky-50 rounded-[3rem] space-y-6 hover:scale-105 transition-transform border border-sky-100 hover:border-sky-200 group">
            <div class="w-16 h-16 bg-sky-500 text-white rounded-2xl flex items-center justify-center mx-auto shadow-lg shadow-sky-500/30 group-hover:-rotate-6 transition-transform duration-300">
              <i class="bx bx-cloud-lightning text-3xl"></i>
            </div>
            <div class="space-y-2">
              <div class="inline-flex items-center gap-1.5 px-2.5 py-1 bg-sky-100 text-sky-700 text-[9px] font-black uppercase tracking-widest rounded-full">
                Météo · 7 jours
              </div>
              <h3 class="text-xl font-black text-[#112830]">Alerte Météo</h3>
              <p class="text-sm text-gray-500 font-medium leading-relaxed">
                Prévisions météorologiques localisées par parcelle : pluie, température, vent et risques de sécheresse pour anticiper vos récoltes.
              </p>
            </div>
            <div class="flex items-center gap-2 text-sky-500 font-black text-[10px] uppercase tracking-widest opacity-0 group-hover:opacity-100 transition-all">
              Inclus dans l'app <i class="bx bx-check-double text-base"></i>
            </div>
          </div>

        </div>

        <NuxtLink :to="localePath('/features')" class="inline-flex items-center gap-3 text-[#10b481] font-black text-sm uppercase tracking-widest hover:gap-5 transition-all">
          {{ $t('footer.nav_solutions') }} <i class="bx bx-right-arrow-alt text-2xl"></i>
        </NuxtLink>
      </div>
    </section>

    <VitrineCTASection />
  </div>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router";
import { useAuthStore } from "~/stores/auth";
import { watch } from "vue";

const localePath = useLocalePath();

definePageMeta({
  layout: "vitrine"
});

const authStore = useAuthStore();
const router = useRouter();

watch(() => authStore.isInitialized, (initialized) => {
  if (initialized && authStore.isAuthenticated) {
    router.push(authStore.getWorkspacePath());
  }
}, { immediate: true });
</script>
