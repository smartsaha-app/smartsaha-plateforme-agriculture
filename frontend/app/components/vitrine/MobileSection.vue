<template>
  <section id="mobile" class="py-32 px-6">
    <div class="max-w-7xl mx-auto bg-[#112830] rounded-[4rem] overflow-hidden relative">
      <!-- Abstract patterns -->
      <div class="absolute top-0 right-0 p-20 opacity-10 pointer-events-none">
        <i class="bx bx-mobile text-[300px]"></i>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center px-12 md:px-24">
        <div class="py-24 space-y-8 relative z-10 text-center lg:text-left">
          <h2 class="text-4xl md:text-6xl font-black text-white leading-tight tracking-tight">
            {{ $t('mobile.title') }} <br/>{{ $t('mobile.title_highlight') }}
          </h2>
          <p class="text-gray-400 font-medium text-lg leading-relaxed max-w-sm mx-auto lg:mx-0">
            {{ $t('mobile.description') }}
          </p>
          <div class="flex flex-wrap justify-center lg:justify-start gap-4">
            <div class="px-8 py-4 bg-white/5 border border-white/10 rounded-2xl flex items-center gap-4 hover:bg-white/10 transition-colors cursor-pointer">
              <i class="bx bxl-play-store text-3xl text-white"></i>
              <div class="text-left">
                <p class="text-[9px] font-black text-gray-500 uppercase tracking-widest leading-none mb-1">{{ $t('mobile.available') }}</p>
                <p class="text-sm font-black text-white">{{ $t('mobile.playstore') }}</p>
              </div>
            </div>
            <div class="px-8 py-4 bg-white/5 border border-white/10 rounded-2xl flex items-center gap-4 hover:bg-white/10 transition-colors cursor-pointer">
              <i class="bx bxl-apple text-3xl text-white"></i>
              <div class="text-left">
                <p class="text-[9px] font-black text-gray-500 uppercase tracking-widest leading-none mb-1">{{ $t('mobile.available') }}</p>
                <p class="text-sm font-black text-white">{{ $t('mobile.appstore') }}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="relative flex justify-center lg:justify-end">
          <img 
            src="/mobile_app.png" 
            alt="SmartSaha Mobile App" 
            class="w-full max-w-[400px] lg:translate-y-24 shadow-2xl skew-y-3 hover:skew-y-0 transition-transform duration-700"
          />
        </div>
      </div>
    </div>
  </section>
</template>
