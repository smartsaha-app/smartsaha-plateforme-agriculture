<template>
  <div class="font-['Readex_Pro'] bg-white selection:bg-[#10b481]/30">
    <!-- Navbar -->
    <nav 
      class="fixed top-0 left-0 right-0 z-[100] transition-all duration-500 py-6"
      :class="isScrolled ? 'bg-white/80 backdrop-blur-xl shadow-sm py-4 border-b border-gray-100' : 'bg-transparent'"
    >
      <div class="max-w-7xl mx-auto px-6 flex items-center justify-between">
        <!-- Logo -->
        <NuxtLink :to="localePath('/')" class="flex items-center gap-3 group">
          <img src="/logo.png" alt="SmartSaha" class="w-12 h-12 object-contain group-hover:rotate-12 transition-transform" />
          <div class="flex flex-col">
            <span class="text-xl font-black text-[#112830] tracking-tight leading-none">SmartSaha</span>
            <span class="text-[10px] font-bold text-[#10b481] uppercase tracking-widest mt-0.5">Agriculture Tech</span>
          </div>
        </NuxtLink>

        <!-- Desktop Links -->
        <div class="hidden lg:flex items-center gap-10">
          <NuxtLink 
            v-for="item in menuItems" 
            :key="item.path"
            :to="localePath(item.path)" 
            class="relative text-xs font-black uppercase tracking-widest text-[#112830] hover:text-[#10b481] transition-colors py-2 group"
            active-class="nav-active"
          >
            {{ $t(item.label) }}
            <span class="absolute bottom-0 left-1/2 -translate-x-1/2 w-0 h-1 bg-[#10b481] rounded-full transition-all duration-300 group-[.nav-active]:w-full group-hover:w-full opacity-0 group-[.nav-active]:opacity-100"></span>
          </NuxtLink>
        </div>

        <!-- Auth & Lang & Mobile Toggle -->
        <div class="flex items-center gap-4">
          <!-- Language Dropdown (Desktop) -->
          <div class="hidden sm:relative sm:block">
            <button 
              @click="isLangOpen = !isLangOpen"
              class="flex items-center gap-2 px-3 py-2 hover:bg-gray-100/50 rounded-xl transition-all text-[10px] font-black uppercase tracking-widest text-[#112830]"
            >
              <i class="bx bx-globe text-base text-[#10b481]"></i>
              {{ locale.toUpperCase() }}
              <i class="bx bx-chevron-down text-sm transition-transform" :class="{ 'rotate-180': isLangOpen }"></i>
            </button>
            <div 
              v-if="isLangOpen"
              class="absolute top-full right-0 mt-2 w-40 bg-white border border-gray-100 rounded-2xl shadow-2xl p-2 z-[200] overflow-hidden"
            >
              <button 
                v-for="l in locales" 
                :key="l.code"
                @click="handleSetLocale(l.code as string)"
                class="w-full flex items-center gap-3 px-4 py-3 hover:bg-[#10b481]/5 text-left transition-all rounded-xl group"
                :class="{ 'bg-[#10b481]/10 text-[#10b481]': locale === l.code }"
              >
                <div class="w-1.5 h-1.5 rounded-full transition-all" :class="locale === l.code ? 'bg-[#10b481]' : 'bg-gray-200 group-hover:bg-[#10b481]/30'"></div>
                <span class="text-[10px] font-black uppercase tracking-widest">{{ (l as any).name }}</span>
              </button>
            </div>
          </div>

          <NuxtLink to="/login" class="hidden sm:block text-sm font-black text-[#112830] hover:opacity-70 transition-all uppercase tracking-widest text-[10px]">{{ $t('menu.login') }}</NuxtLink>
          <NuxtLink 
            to="/signup" 
            class="hidden sm:block px-6 py-3 bg-[#112830] text-white rounded-2xl font-black text-[10px] uppercase tracking-widest shadow-xl shadow-[#112830]/20 hover:-translate-y-1 transition-all active:scale-95"
          >
            {{ $t('menu.join') }}
          </NuxtLink>

          <!-- Mobile Toggle -->
          <button 
            @click="isMenuOpen = !isMenuOpen"
            class="lg:hidden w-12 h-12 flex items-center justify-center bg-[#112830]/5 rounded-xl hover:bg-[#112830]/10 transition-colors text-[#112830]"
          >
            <i class="bx text-2xl" :class="isMenuOpen ? 'bx-x' : 'bx-menu-alt-right'"></i>
          </button>
        </div>
      </div>
    </nav>

    <!-- Mobile Menu Overlay -->
    <Transition
      enter-active-class="transition duration-300 ease-out"
      enter-from-class="opacity-0 translate-x-10"
      enter-to-class="opacity-100 translate-x-0"
      leave-active-class="transition duration-200 ease-in"
      leave-from-class="opacity-100 translate-x-0"
      leave-to-class="opacity-0 translate-x-10"
    >
      <div v-if="isMenuOpen" class="fixed inset-0 z-[150] lg:hidden">
        <div class="absolute inset-0 bg-[#112830]/40 backdrop-blur-md" @click="isMenuOpen = false"></div>
        <div class="absolute top-0 right-0 bottom-0 w-[300px] bg-white shadow-2xl p-8 flex flex-col">
          <div class="flex items-center justify-between mb-12">
            <img src="/logo.png" class="w-10 h-10 object-contain" />
            <button @click="isMenuOpen = false" class="text-2xl text-[#112830]"><i class="bx bx-x"></i></button>
          </div>

          <div class="flex flex-col gap-8 mb-auto">
            <NuxtLink 
              v-for="item in menuItems" 
              :key="item.path"
              :to="localePath(item.path)"
              class="flex items-center justify-between text-2xl font-black text-[#112830] group"
              active-class="mobile-nav-active"
              @click="isMenuOpen = false"
            >
              <span class="group-[.mobile-nav-active]:text-[#10b481] transition-colors">{{ $t(item.label) }}</span>
              <i class="bx bx-right-arrow-alt text-[#10b481] opacity-0 group-[.mobile-nav-active]:opacity-100 transition-all"></i>
            </NuxtLink>
          </div>

          <div class="space-y-4 pt-8 border-t border-gray-100">
             <div class="flex items-center gap-4 mb-4">
                <button 
                  v-for="l in locales" 
                  :key="l.code"
                  @click="handleSetLocale(l.code as string)"
                  class="px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all"
                  :class="locale === l.code ? 'bg-[#10b481] text-white' : 'bg-gray-100 text-[#112830]'"
                >
                  {{ l.code }}
                </button>
             </div>
             <NuxtLink to="/login" class="block w-full text-center py-4 bg-gray-100 text-[#112830] rounded-2xl font-black text-[10px] uppercase tracking-widest">{{ $t('menu.login') }}</NuxtLink>
             <NuxtLink to="/signup" class="block w-full text-center py-4 bg-[#112830] text-white rounded-2xl font-black text-[10px] uppercase tracking-widest shadow-lg shadow-[#112830]/20">{{ $t('menu.join') }}</NuxtLink>
          </div>
        </div>
      </div>
    </Transition>

    <main class="min-h-screen">
      <slot />
    </main>

    <a 
      href="mailto:feedback@smartsaha.mg" 
      class="fixed bottom-8 right-8 z-[140] flex items-center gap-3 px-6 py-4 bg-[#10b481] text-white rounded-2xl shadow-2xl shadow-[#10b481]/40 hover:-translate-y-2 hover:scale-105 active:scale-95 transition-all group"
    >
      <div class="w-10 h-10 bg-white/20 rounded-xl flex items-center justify-center group-hover:rotate-12 transition-transform">
        <i class="bx bx-message-square-detail text-xl"></i>
      </div>
      <div class="flex flex-col items-start pr-2">
        <span class="text-[9px] font-black uppercase tracking-widest leading-none mb-1 opacity-80">{{ $t('footer.feedback_badge') }}</span>
        <span class="text-sm font-black whitespace-nowrap">{{ $t('footer.feedback_btn') }}</span>
      </div>
    </a>

    <!-- Footer -->
    <footer class="bg-[#112830] text-white py-20 px-6">
      <div class="max-w-7xl mx-auto">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-12 mb-20">
          <div class="col-span-1 md:col-span-2 space-y-6">
            <div class="flex items-center gap-3">
              <img src="/logo.png" alt="SmartSaha" class="w-12 h-12 rounded-lg" />
              <div class="flex flex-col">
                <span class="text-3xl font-black tracking-tight">SmartSaha</span>
                <span class="text-[10px] font-bold text-[#10b481] uppercase tracking-widest mt-0.5">Agriculture Tech</span>
              </div>
            </div>
            <p class="text-gray-400 max-w-sm font-medium leading-relaxed">
              {{ $t('footer.description') }}
            </p>
          </div>
          <div class="space-y-6">
            <h4 class="text-[10px] font-black uppercase tracking-widest text-[#10b481]">{{ $t('footer.nav_title') }}</h4>
            <ul class="space-y-4">
              <li><NuxtLink :to="localePath('/')" class="text-gray-400 hover:text-white transition-colors font-bold text-sm">{{ $t('footer.nav_home') }}</NuxtLink></li>
              <li><NuxtLink :to="localePath('/features')" class="text-gray-400 hover:text-white transition-colors font-bold text-sm">{{ $t('footer.nav_solutions') }}</NuxtLink></li>
              <li><NuxtLink :to="localePath('/guide')" class="text-gray-400 hover:text-white transition-colors font-bold text-sm">{{ $t('footer.nav_tutorial') }}</NuxtLink></li>
            </ul>
          </div>
          <div class="space-y-6">
            <h4 class="text-[10px] font-black uppercase tracking-widest text-[#10b481]">{{ $t('footer.legal_title') }}</h4>
            <ul class="space-y-4">
              <li><a href="#" class="text-gray-400 hover:text-white transition-colors font-bold text-sm">{{ $t('footer.legal_privacy') }}</a></li>
              <li><a href="#" class="text-gray-400 hover:text-white transition-colors font-bold text-sm">{{ $t('footer.legal_terms') }}</a></li>
              <li><a href="#" class="text-gray-400 hover:text-white transition-colors font-bold text-sm">{{ $t('footer.legal_contact') }}</a></li>
            </ul>
          </div>
        </div>
        <div class="pt-8 border-t border-white/5 flex flex-col md:flex-row justify-between items-center gap-4 text-gray-500 text-xs font-bold uppercase tracking-widest">
          <p>© 2026 SmartSaha. {{ $t('footer.rights') }}</p>
          <div class="flex gap-6">
            <a href="#"><i class="bx bxl-facebook text-xl hover:text-white transition-colors"></i></a>
            <a href="#"><i class="bx bxl-linkedin text-xl hover:text-white transition-colors"></i></a>
            <a href="#"><i class="bx bxl-instagram text-xl hover:text-white transition-colors"></i></a>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';

const { locale, locales, setLocale } = useI18n()
const localePath = useLocalePath()

const isScrolled = ref(false);
const isLangOpen = ref(false);
const isMenuOpen = ref(false);

const menuItems = [
  { path: '/', label: 'menu.about' },
  { path: '/features', label: 'menu.features' },
  { path: '/guide', label: 'menu.guide' },
  { path: '/support', label: 'menu.support' },
]

const handleScroll = () => {
  isScrolled.value = window.scrollY > 50;
};

const handleSetLocale = (code: string) => {
  setLocale(code);
  isLangOpen.value = false;
};

onMounted(() => {
  window.addEventListener('scroll', handleScroll);
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
});
</script>

<style scoped>
@keyframes spin-slow {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
.animate-spin-slow {
  animation: spin-slow 8s linear infinite;
}
html {
  scroll-behavior: smooth;
}
</style>
