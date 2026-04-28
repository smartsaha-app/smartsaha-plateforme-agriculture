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
