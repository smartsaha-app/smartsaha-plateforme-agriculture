<template>
  <section id="tutorial" class="py-32 overflow-hidden bg-white">
    <div class="max-w-7xl mx-auto px-6">
      <!-- Intro Section -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center mb-24">
        <div class="space-y-8">
          <div class="inline-flex items-center gap-3 px-4 py-2 bg-[#10b481]/10 rounded-xl">
            <i class="bx bx-compass text-[#10b481] text-lg"></i>
            <span class="text-[10px] font-black uppercase tracking-[0.2em] text-[#10b481]">{{ $t('guide.badge') }}</span>
          </div>
          <h2 class="text-4xl md:text-6xl font-black text-[#112830] tracking-tight leading-[1.1]">
            {{ $t('guide.title') }}
          </h2>
          <p class="text-lg text-gray-500 font-medium leading-relaxed">
            {{ $t('guide.description') }}
          </p>
        </div>
        <div class="relative group">
          <div class="absolute inset-0 bg-gradient-to-tr from-[#112830]/10 to-transparent rounded-[4rem] blur-3xl group-hover:blur-2xl transition-all duration-1000"></div>
          <img 
            src="/guide_intro_farmer_success_1775824516251.png" 
            alt="Agriculteur SmartSaha heureux" 
            class="relative w-full aspect-[4/3] object-cover rounded-[4rem] shadow-2xl transition-all duration-1000 border-8 border-[#f7faf9]"
          />
          <!-- Badge flottant -->
          <div class="absolute -top-6 -left-6 bg-[#10b481] text-white p-5 rounded-3xl shadow-xl flex items-center gap-4 animate-pulse">
            <i class="bx bxs-check-shield text-3xl"></i>
            <div class="flex flex-col">
              <span class="text-[10px] font-black uppercase tracking-widest leading-none mb-1">Succès garanti</span>
              <span class="text-xs font-bold whitespace-nowrap">+40% de rendement</span>
            </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
        <!-- Espace : AGRICULTEUR (Couleur Verte/Claire) -->
        <div class="group bg-[#f7faf9] rounded-[4rem] p-10 md:p-14 space-y-12 border border-transparent hover:border-[#10b481]/20 hover:bg-white hover:shadow-2xl transition-all duration-700 relative overflow-hidden">
          <div class="absolute -top-10 -right-10 p-10 opacity-5 group-hover:opacity-10 group-hover:scale-110 transition-all duration-1000 rotate-12">
            <i class="bx bx-landscape text-[280px] text-[#112830]"></i>
          </div>
          
          <div class="flex items-center gap-6 relative z-10 transition-transform group-hover:translate-x-2">
            <div class="w-16 h-16 rounded-[1.5rem] bg-[#10b481] text-white flex items-center justify-center shadow-xl shadow-[#10b481]/20">
              <i class="bx bx-user text-4xl"></i>
            </div>
            <div>
              <h3 class="text-3xl font-black text-[#112830]">{{ $t('tutorial.farmer.title') }}</h3>
              <p class="text-[11px] font-bold text-[#10b481] uppercase tracking-[0.2em]">{{ $t('tutorial.farmer.subtitle') }}</p>
            </div>
          </div>

          <div class="space-y-12 relative z-10">
            <!-- Steps loop for farmer -->
            <div v-for="n in 4" :key="'f'+n" class="flex gap-8 group/item">
              <span class="text-5xl font-black text-gray-200 group-hover/item:text-[#10b481] transition-colors duration-500">0{{ n }}</span>
              <div class="space-y-2">
                <h4 class="font-black text-[#112830] uppercase text-[11px] tracking-[0.2em] group-hover/item:translate-x-1 transition-transform">
                  {{ $t(`tutorial.farmer.step${n}_title`) }}
                </h4>
                <p class="text-[15px] text-gray-500 font-medium leading-relaxed max-w-sm">
                  {{ $t(`tutorial.farmer.step${n}_desc`) }}
                </p>
              </div>
            </div>
          </div>
          
          <NuxtLink to="/signup" class="relative z-10 block w-full text-center py-6 bg-[#112830] text-white rounded-[2rem] font-black text-[11px] uppercase tracking-[0.2em] shadow-xl shadow-[#112830]/10 hover:scale-[1.02] active:scale-95 transition-all">
            {{ $t('tutorial.farmer.cta') }}
          </NuxtLink>
        </div>

        <!-- Espace : ORGANISATION (Couleur Sombre) -->
        <div class="group bg-[#112830] rounded-[4rem] p-10 md:p-14 space-y-12 border border-white/5 hover:bg-[#152e37] hover:shadow-2xl hover:shadow-black/50 transition-all duration-700 relative overflow-hidden">
          <div class="absolute -top-10 -right-10 p-10 opacity-5 group-hover:opacity-10 group-hover:scale-110 transition-all duration-1000 -rotate-12 text-white">
            <i class="bx bx-buildings text-[280px]"></i>
          </div>

          <div class="flex items-center gap-6 relative z-10 transition-transform group-hover:translate-x-2">
            <div class="w-16 h-16 rounded-[1.5rem] bg-white text-[#112830] flex items-center justify-center shadow-xl shadow-white/5">
              <i class="bx bx-group text-4xl"></i>
            </div>
            <div>
              <h3 class="text-3xl font-black text-white">{{ $t('tutorial.organization.title') }}</h3>
              <p class="text-[11px] font-bold text-[#10b481] uppercase tracking-[0.2em]">{{ $t('tutorial.organization.subtitle') }}</p>
            </div>
          </div>

          <div class="space-y-12 relative z-10">
             <!-- Steps loop for organization -->
             <div v-for="n in 4" :key="'o'+n" class="flex gap-8 group/item">
              <span class="text-5xl font-black text-white/5 group-hover/item:text-[#10b481] transition-colors duration-500">0{{ n }}</span>
              <div class="space-y-2">
                <h4 class="font-black text-[#10b481] uppercase text-[11px] tracking-[0.2em] group-hover/item:translate-x-1 transition-transform">
                  {{ $t(`tutorial.organization.step${n}_title`) }}
                </h4>
                <p class="text-[15px] text-gray-400 font-medium leading-relaxed max-w-sm">
                  {{ $t(`tutorial.organization.step${n}_desc`) }}
                </p>
              </div>
            </div>
          </div>
          
          <NuxtLink to="/signup" class="relative z-10 block w-full text-center py-6 bg-[#10b481] text-white rounded-[2rem] font-black text-[11px] uppercase tracking-[0.2em] shadow-xl shadow-[#10b481]/10 hover:scale-[1.02] active:scale-95 transition-all">
            {{ $t('tutorial.organization.cta') }}
          </NuxtLink>
        </div>
      </div>
    </div>
  </section>
</template>
