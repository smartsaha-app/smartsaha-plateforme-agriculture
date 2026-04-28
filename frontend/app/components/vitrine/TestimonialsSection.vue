<template>
  <section class="py-32 bg-[#112830] relative overflow-hidden">
    <!-- Background glow -->
    <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[400px] bg-[#10b481]/10 blur-[120px] rounded-full pointer-events-none"></div>

    <div class="max-w-7xl mx-auto px-6 relative z-10 text-center">
      <h2 class="text-4xl md:text-5xl font-black text-white tracking-tight mb-20 whitespace-pre-wrap">{{ $t('testimonials.title') }} <br/><span class="text-[#10b481]">{{ $t('testimonials.title_highlight') }}</span></h2>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-8 text-left">
        <!-- Testimonial 1 -->
        <div class="bg-white/5 backdrop-blur-xl border border-white/10 p-10 rounded-[2.5rem] space-y-6 hover:-translate-y-2 transition-all duration-500">
          <div class="flex gap-1 text-yellow-500">
            <i class="bx bxs-star"></i><i class="bx bxs-star"></i><i class="bx bxs-star"></i><i class="bx bxs-star"></i><i class="bx bxs-star"></i>
          </div>
          <p class="text-gray-300 font-medium leading-relaxed italic">
            {{ $t('testimonials.items[0].text') }}
          </p>
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 rounded-full bg-[#10b481]/20 flex items-center justify-center text-[#10b481] font-black">R</div>
            <div>
              <p class="text-white font-bold text-sm">{{ $t('testimonials.items[0].name') }}</p>
              <p class="text-gray-500 text-[10px] uppercase font-black tracking-widest">{{ $t('testimonials.items[0].role') }}</p>
            </div>
          </div>
        </div>

        <!-- Testimonial 2 -->
        <div class="bg-white/5 backdrop-blur-xl border border-white/10 p-10 rounded-[2.5rem] space-y-6 hover:-translate-y-2 transition-all duration-500">
          <div class="flex gap-1 text-yellow-500">
            <i class="bx bxs-star"></i><i class="bx bxs-star"></i><i class="bx bxs-star"></i><i class="bx bxs-star"></i><i class="bx bxs-star"></i>
          </div>
          <p class="text-gray-300 font-medium leading-relaxed italic">
            {{ $t('testimonials.items[1].text') }}
          </p>
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 rounded-full bg-[#10b481]/20 flex items-center justify-center text-[#10b481] font-black">M</div>
            <div>
              <p class="text-white font-bold text-sm">{{ $t('testimonials.items[1].name') }}</p>
              <p class="text-gray-500 text-[10px] uppercase font-black tracking-widest">{{ $t('testimonials.items[1].role') }}</p>
            </div>
          </div>
        </div>

        <!-- Testimonial 3 -->
        <div class="bg-white/5 backdrop-blur-xl border border-white/10 p-10 rounded-[2.5rem] space-y-6 hover:-translate-y-2 transition-all duration-500">
          <div class="flex gap-1 text-yellow-500">
            <i class="bx bxs-star"></i><i class="bx bxs-star"></i><i class="bx bxs-star"></i><i class="bx bxs-star"></i><i class="bx bxs-star"></i>
          </div>
          <p class="text-gray-300 font-medium leading-relaxed italic">
            {{ $t('testimonials.items[2].text') }}
          </p>
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 rounded-full bg-[#10b481]/20 flex items-center justify-center text-[#10b481] font-black">J</div>
            <div>
              <p class="text-white font-bold text-sm">{{ $t('testimonials.items[2].name') }}</p>
              <p class="text-gray-500 text-[10px] uppercase font-black tracking-widest">{{ $t('testimonials.items[2].role') }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
