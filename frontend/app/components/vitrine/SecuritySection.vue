<template>
  <section id="support" class="py-32 bg-gray-50/50">
    <div class="max-w-7xl mx-auto px-6">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-20 items-center">
        <div class="space-y-8">
          <h2 class="text-4xl md:text-5xl font-black text-[#112830] tracking-tight">{{ $t('security.title') }} <br/><span class="text-[#10b481]">{{ $t('security.title_highlight') }}</span></h2>
          <p class="text-gray-500 font-medium leading-relaxed">
            {{ $t('security.description') }}
          </p>
          
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-6 pt-4">
            <div class="flex items-start gap-4">
              <div class="w-10 h-10 rounded-xl bg-white flex items-center justify-center text-[#10b481] shadow-sm">
                <i class="bx bx-shield-quarter text-xl"></i>
              </div>
              <div>
                <h4 class="text-sm font-black text-[#112830] uppercase tracking-widest mb-1">{{ $t('security.items.security.title') }}</h4>
                <p class="text-xs text-gray-400 font-bold">{{ $t('security.items.security.desc') }}</p>
              </div>
            </div>
            <div class="flex items-start gap-4">
              <div class="w-10 h-10 rounded-xl bg-white flex items-center justify-center text-[#10b481] shadow-sm">
                <i class="bx bx-support text-xl"></i>
              </div>
              <div>
                <h4 class="text-sm font-black text-[#112830] uppercase tracking-widest mb-1">{{ $t('security.items.support.title') }}</h4>
                <p class="text-xs text-gray-400 font-bold">{{ $t('security.items.support.desc') }}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-[#112830] rounded-[3rem] p-12 text-white relative overflow-hidden">
          <div class="absolute -bottom-10 -right-10 p-10 opacity-10">
            <i class="bx bx-devices text-[200px]"></i>
          </div>
          <h3 class="text-2xl font-black mb-6 relative z-10">{{ $t('security.hybrid.title') }}</h3>
          <ul class="space-y-6 relative z-10">
            <li class="flex gap-4">
              <i class="bx bx-check-circle text-[#10b481] text-2xl"></i>
              <div>
                <span class="font-black text-sm uppercase tracking-widest">{{ $t('security.hybrid.web.title') }}</span>
                <p class="text-xs text-gray-400 font-medium">{{ $t('security.hybrid.web.desc') }}</p>
              </div>
            </li>
            <li class="flex gap-4">
              <i class="bx bx-check-circle text-[#10b481] text-2xl"></i>
              <div>
                <span class="font-black text-sm uppercase tracking-widest">{{ $t('security.hybrid.mobile.title') }}</span>
                <p class="text-xs text-gray-400 font-medium">{{ $t('security.hybrid.mobile.desc') }}</p>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </section>
</template>
