<template>
  <div>
    <VitrineHeroSection />
    <VitrineStatsSection />

    <!-- Sesily AI spotlight -->
    <section class="py-20 bg-[#112830] overflow-hidden relative">
      <div class="absolute inset-0 pointer-events-none" aria-hidden="true">
        <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[300px] bg-[#10b481]/8 rounded-full blur-[80px]"></div>
      </div>
      <div class="max-w-7xl mx-auto px-6 relative z-10">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          <div class="space-y-8">
            <div class="inline-flex items-center gap-3 px-4 py-2 bg-[#10b481]/15 border border-[#10b481]/20 rounded-full">
              <span class="relative flex h-2 w-2" aria-hidden="true">
                <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#10b481] opacity-75"></span>
                <span class="relative inline-flex rounded-full h-2 w-2 bg-[#10b481]"></span>
              </span>
              <span class="text-xs font-black uppercase tracking-widest text-[#10b481]">Sesily AI — Disponible 24h/7j</span>
            </div>
            <h2 class="text-4xl md:text-5xl font-black text-white tracking-tight leading-[1.1]">
              Votre agronome IA,<br />
              <span class="text-[#10b481]">toujours disponible.</span>
            </h2>
            <p class="text-gray-400 font-medium text-lg leading-relaxed">
              {{ $t('features.items.ai.desc') }}
            </p>
            <NuxtLink :to="localePath('/sesily-ai')"
              class="inline-flex items-center gap-3 px-8 py-5 bg-[#10b481] text-white rounded-2xl font-black text-sm uppercase tracking-widest hover:-translate-y-1 transition-all shadow-2xl shadow-[#10b481]/30">
              <i class="bx bx-robot text-lg" aria-hidden="true"></i>
              {{ $t('hero.sesily_badge') }}
              <i class="bx bx-right-arrow-alt text-xl" aria-hidden="true"></i>
            </NuxtLink>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div v-for="feature in sesilFeatures" :key="feature.icon"
              class="bg-white/5 border border-white/10 rounded-2xl p-6 hover:bg-white/10 hover:border-[#10b481]/30 transition-all group">
              <div class="w-10 h-10 bg-[#10b481]/20 rounded-xl flex items-center justify-center mb-4 group-hover:bg-[#10b481]/30 transition-colors">
                <i :class="['bx', feature.icon, 'text-xl text-[#10b481]']" aria-hidden="true"></i>
              </div>
              <p class="text-white font-bold text-sm">{{ feature.label }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features teaser -->
    <section class="py-24 bg-white">
      <div class="max-w-7xl mx-auto px-6 text-center space-y-16">
        <div class="max-w-3xl mx-auto space-y-4">
          <h2 class="text-4xl md:text-5xl font-black text-[#112830] tracking-tight">
            {{ $t('features.badge') }}
          </h2>
          <p class="text-gray-500 font-medium text-base leading-relaxed">
            {{ $t('features.description') }}
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="p-10 bg-gray-50 rounded-[3rem] space-y-6 hover:scale-105 hover:shadow-xl transition-all">
            <div class="w-16 h-16 bg-[#10b481] text-white rounded-2xl flex items-center justify-center mx-auto shadow-lg shadow-[#10b481]/20">
              <i class="bx bx-leaf text-3xl" aria-hidden="true"></i>
            </div>
            <h3 class="text-xl font-black text-[#112830]">{{ $t('features.items.precision.title') }}</h3>
            <p class="text-sm text-gray-500 font-medium leading-relaxed">{{ $t('features.items.precision.desc') }}</p>
          </div>

          <div class="p-10 bg-gray-50 rounded-[3rem] space-y-5 hover:scale-105 hover:shadow-xl transition-all text-left">
            <div class="w-16 h-16 bg-[#112830] text-white rounded-2xl flex items-center justify-center shadow-lg shadow-[#112830]/20">
              <i class="bx bx-store-alt text-3xl" aria-hidden="true"></i>
            </div>
            <h3 class="text-xl font-black text-[#112830]">{{ $t('features.items.marketplace.title') }}</h3>
            <p class="text-sm text-gray-500 font-medium leading-relaxed">{{ $t('features.items.marketplace.desc') }}</p>
          </div>

          <div class="p-10 bg-gray-50 rounded-[3rem] space-y-6 hover:scale-105 hover:shadow-xl transition-all">
            <div class="w-16 h-16 bg-[#112830] text-white rounded-2xl flex items-center justify-center mx-auto shadow-lg shadow-[#112830]/20">
              <i class="bx bx-line-chart text-3xl" aria-hidden="true"></i>
            </div>
            <h3 class="text-xl font-black text-[#112830]">{{ $t('features.items.yield.title') }}</h3>
            <p class="text-sm text-gray-500 font-medium leading-relaxed">{{ $t('features.items.yield.desc') }}</p>
          </div>

          <!-- Card Alerte Feu -->
          <NuxtLink :to="localePath('/fires')"
            class="p-10 bg-orange-50 rounded-[3rem] space-y-6 hover:scale-105 transition-all border border-orange-100 hover:border-orange-200 hover:shadow-xl group block text-left">
            <div class="relative w-16 h-16 mx-auto">
              <span class="absolute -top-1 -right-1 flex h-3 w-3 z-10" aria-hidden="true">
                <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-orange-500 opacity-60"></span>
                <span class="relative inline-flex rounded-full h-3 w-3 bg-orange-500"></span>
              </span>
              <div class="w-16 h-16 bg-orange-500 text-white rounded-2xl flex items-center justify-center shadow-lg shadow-orange-500/30 group-hover:rotate-6 transition-transform duration-300">
                <i class="bx bxs-flame text-3xl" aria-hidden="true"></i>
              </div>
            </div>
            <div class="space-y-2">
              <div class="inline-flex items-center gap-1.5 px-2.5 py-1 bg-orange-100 text-orange-700 text-xs font-black uppercase tracking-widest rounded-full">
                NASA FIRMS · Live
              </div>
              <h3 class="text-xl font-black text-[#112830]">Alerte Incendie</h3>
              <p class="text-sm text-gray-500 font-medium leading-relaxed">
                Détection des feux actifs à Madagascar par satellite MODIS (NASA) en temps réel.
              </p>
            </div>
            <div class="flex items-center gap-2 text-orange-500 font-black text-xs uppercase tracking-widest group-hover:gap-3 transition-all">
              Voir la carte <i class="bx bx-right-arrow-alt text-base" aria-hidden="true"></i>
            </div>
          </NuxtLink>

          <!-- Card Alerte Météo -->
          <div class="p-10 bg-sky-50 rounded-[3rem] space-y-6 hover:scale-105 transition-all border border-sky-100 hover:border-sky-200 hover:shadow-xl group text-left">
            <div class="w-16 h-16 bg-sky-500 text-white rounded-2xl flex items-center justify-center mx-auto shadow-lg shadow-sky-500/30 group-hover:-rotate-6 transition-transform duration-300">
              <i class="bx bx-cloud-lightning text-3xl" aria-hidden="true"></i>
            </div>
            <div class="space-y-2">
              <div class="inline-flex items-center gap-1.5 px-2.5 py-1 bg-sky-100 text-sky-700 text-xs font-black uppercase tracking-widest rounded-full">
                Météo · 7 jours
              </div>
              <h3 class="text-xl font-black text-[#112830]">Alerte Météo</h3>
              <p class="text-sm text-gray-500 font-medium leading-relaxed">
                Prévisions météorologiques localisées par parcelle : pluie, température, vent et risques de sécheresse.
              </p>
            </div>
            <div class="flex items-center gap-2 text-sky-500 font-black text-xs uppercase tracking-widest opacity-0 group-hover:opacity-100 transition-all">
              Inclus dans l'app <i class="bx bx-check-double text-base" aria-hidden="true"></i>
            </div>
          </div>

          <!-- Card Sesily AI -->
          <NuxtLink :to="localePath('/sesily-ai')"
            class="p-10 bg-[#112830] rounded-[3rem] space-y-6 hover:scale-105 transition-all border border-[#10b481]/10 hover:border-[#10b481]/40 hover:shadow-xl group block text-left">
            <div class="w-16 h-16 bg-[#10b481] text-white rounded-2xl flex items-center justify-center mx-auto shadow-lg shadow-[#10b481]/30 group-hover:rotate-6 transition-transform duration-300">
              <i class="bx bx-robot text-3xl" aria-hidden="true"></i>
            </div>
            <div class="space-y-2">
              <div class="inline-flex items-center gap-1.5 px-2.5 py-1 bg-[#10b481]/20 text-[#10b481] text-xs font-black uppercase tracking-widest rounded-full">
                IA · 24h/7j
              </div>
              <h3 class="text-xl font-black text-white">Sesily AI</h3>
              <p class="text-sm text-gray-400 font-medium leading-relaxed">
                {{ $t('features.items.ai.desc') }}
              </p>
            </div>
            <div class="flex items-center gap-2 text-[#10b481] font-black text-xs uppercase tracking-widest group-hover:gap-3 transition-all">
              {{ $t('features.sesily_cta') }} <i class="bx bx-right-arrow-alt text-base" aria-hidden="true"></i>
            </div>
          </NuxtLink>
        </div>

        <NuxtLink :to="localePath('/features')" class="inline-flex items-center gap-3 text-[#10b481] font-black text-sm uppercase tracking-widest hover:gap-5 transition-all">
          {{ $t('footer.nav_solutions') }} <i class="bx bx-right-arrow-alt text-2xl" aria-hidden="true"></i>
        </NuxtLink>
      </div>
    </section>

    <!-- Testimonials -->
    <VitrineTestimonialsSection />

    <VitrineCTASection />
  </div>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router";
import { useAuthStore } from "~/stores/auth";
import { watch } from "vue";

const localePath = useLocalePath();
const { t } = useI18n();

definePageMeta({ layout: "vitrine" });

const authStore = useAuthStore();
const router = useRouter();

watch(() => authStore.isInitialized, (initialized) => {
  if (initialized && authStore.isAuthenticated) {
    router.push(authStore.getWorkspacePath());
  }
}, { immediate: true });

const sesilFeatures = [
  { icon: 'bx-leaf',         label: 'Cultures & Maladies' },
  { icon: 'bx-cloud',        label: 'Météo & Alertes' },
  { icon: 'bx-map-alt',      label: 'Analyse Parcelles' },
  { icon: 'bx-line-chart',   label: 'Optimisation Rendements' },
];
</script>