<template>
  <div class="p-6 space-y-8 max-w-[1400px] mx-auto">
    <!-- ===== HERO SECTION PREMIUM ===== -->
    <div class="bg-gradient-to-r from-[#112830] to-[#0a8f6e] p-10 sm:p-16 rounded-[4rem] text-white relative overflow-hidden shadow-2xl">
      <div class="relative z-10 space-y-6">
        <span class="px-5 py-2 bg-white/10 backdrop-blur-xl rounded-full text-xs font-black uppercase tracking-[0.2em] border border-white/10">{{ $t('marketplacePro.b2bSourcingHub') }}</span>
        <h1 class="text-5xl sm:text-6xl font-black leading-tight">{{ $t('marketplacePro.marketplacePro') }}</h1>
        <p class="text-white/70 max-w-2xl text-lg font-medium leading-relaxed">
          {{ $t('marketplacePro.centraliseYourPurchasesOptimiseYourSuppl') }}
        </p>
        <div class="flex flex-wrap gap-4 pt-4">
          <button @click="showOfferModal = true" class="px-10 py-5 bg-[#10b481] hover:bg-white hover:text-[#112830] text-white rounded-[2rem] font-black transition-all duration-500 shadow-xl shadow-[#10b481]/20 flex items-center gap-3">
            <i class="bx bx-plus-circle text-2xl"></i> {{ $t('marketplacePro.createACallForTenders') }}
          </button>
          <button class="px-10 py-5 bg-white/10 hover:bg-white/20 text-white rounded-[2rem] font-black transition-all border border-white/10 backdrop-blur-md">
            {{ $t('marketplacePro.exploreOffers') }}
          </button>
        </div>
      </div>
      
      <div class="absolute top-0 right-0 p-12 opacity-10 pointer-events-none">
        <i class="bx bx-store text-[20rem]"></i>
      </div>
      <div class="absolute bottom-[-20%] left-[30%] w-96 h-96 bg-white/5 rounded-full blur-[120px]"></div>
    </div>

    <!-- ===== MARKET INSIGHTS WIDGETS ===== -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
       <div v-for="insight in insights" :key="insight.label" class="bg-white p-8 rounded-[2.5rem] border border-gray-100 shadow-sm hover:shadow-xl transition-all group cursor-pointer">
         <div class="flex items-center justify-between mb-4">
           <div :class="['w-12 h-12 rounded-2xl flex items-center justify-center text-xl', insight.bg, insight.text]">
             <i :class="insight.icon"></i>
           </div>
           <span :class="['text-[10px] font-black px-2 py-1 rounded-lg', insight.trendUp ? 'bg-emerald-50 text-emerald-600' : 'bg-rose-50 text-rose-600']">
             {{ insight.trend }}
           </span>
         </div>
         <p class="text-xs font-bold text-gray-400 uppercase tracking-widest">{{ insight.label }}</p>
         <h3 class="text-2xl font-black text-[#112830] mt-1">{{ insight.value }}</h3>
         <p class="text-[10px] text-gray-400 mt-4 italic">{{ insight.sub }}</p>
       </div>
    </div>

    <!-- ===== ACTIVE TENDERS TABLE ===== -->
    <div class="bg-white rounded-[3rem] border border-gray-100 shadow-sm overflow-hidden">
      <div class="p-10 border-b border-gray-50 flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <h3 class="text-2xl font-black text-[#112830]">{{ $t('marketplacePro.yourCallsForTenders') }}</h3>
          <p class="text-sm text-gray-400 font-medium tracking-tight">{{ $t('marketplacePro.trackTheStatusOfYourRequestsAndCompareTh') }}</p>
        </div>
        <div class="flex items-center gap-4">
          <div class="relative">
            <i class="bx bx-search absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"></i>
            <input type="text" :placeholder="$t('dashboard.search')" class="pl-12 pr-6 py-3 bg-gray-50 rounded-2xl border-none text-sm outline-none focus:ring-2 focus:ring-[#10b481]/20 w-64" />
          </div>
          <button class="w-12 h-12 rounded-2xl bg-gray-50 flex items-center justify-center text-gray-400 hover:bg-[#112830] hover:text-white transition-all">
            <i class="bx bx-filter-alt"></i>
          </button>
        </div>
      </div>

      <div class="px-10 pb-10">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="text-left border-b border-gray-50">
                <th class="py-6 text-[10px] font-black text-gray-400 uppercase tracking-widest">{{ $t('marketplacePro.product') }}</th>
                <th class="py-6 text-[10px] font-black text-gray-400 uppercase tracking-widest">{{ $t('marketplacePro.requiredVolume') }}</th>
                <th class="py-6 text-[10px] font-black text-gray-400 uppercase tracking-widest">{{ $t('marketplacePro.deadline') }}</th>
                <th class="py-6 text-[10px] font-black text-gray-400 uppercase tracking-widest">{{ $t('marketplacePro.offersReceived') }}</th>
                <th class="py-6 text-[10px] font-black text-gray-400 uppercase tracking-widest">{{ $t('dashboard.status') }}</th>
                <th class="py-6"></th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-50">
              <tr v-for="tender in tenders" :key="tender.id" class="group hover:bg-gray-50/50 transition-colors">
                <td class="py-6">
                  <div class="flex items-center gap-4">
                    <div class="w-12 h-12 rounded-2xl bg-emerald-50 text-[#10b481] flex items-center justify-center font-bold relative">
                      <i class="bx bx-leaf text-xl"></i>
                    </div>
                    <div>
                      <p class="font-bold text-[#112830] group-hover:text-[#10b481] transition-colors">{{ tender.product }}</p>
                      <p class="text-[9px] font-bold text-gray-400 uppercase tracking-tighter">{{ tender.id }}</p>
                    </div>
                  </div>
                </td>
                <td class="py-6">
                  <p class="font-black text-[#112830]">{{ tender.volume }} <span class="text-[10px] text-gray-400 ml-1">TONNES</span></p>
                </td>
                <td class="py-6">
                  <div class="flex items-center gap-2 text-xs font-bold text-gray-500">
                    <i class="bx bx-calendar"></i>
                    {{ tender.deadline }}
                  </div>
                </td>
                <td class="py-6">
                  <div class="flex items-center gap-3">
                    <div class="flex -space-x-2">
                       <div v-for="i in Math.min(tender.offers, 3)" :key="i" class="w-7 h-7 rounded-full border-2 border-white bg-gray-200 overflow-hidden">
                         <img :src="`https://i.pravatar.cc/100?u=offerer${tender.id}${i}`" alt="" />
                       </div>
                    </div>
                    <span class="text-xs font-black text-[#10b481]">{{ $t('marketplacePro.p0Offers', { p0: tender.offers }) }}</span>
                  </div>
                </td>
                <td class="py-6">
                   <span :class="['px-3 py-1 rounded-xl text-[10px] font-black uppercase tracking-widest', tender.status === 'Ouvert' ? 'bg-emerald-50 text-emerald-600' : 'bg-gray-100 text-gray-400']">
                     {{ tender.status }}
                   </span>
                </td>
                <td class="py-6 text-right">
                   <button class="px-6 py-2 bg-[#112830] text-white rounded-xl text-xs font-bold shadow-lg shadow-[#112830]/10 hover:bg-[#10b481] transition-all">{{ $t('marketplacePro.details') }}</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div v-if="tenders.length === 0" class="py-20 text-center space-y-4">
           <i class="bx bx-file-blank text-6xl text-gray-100"></i>
           <p class="text-gray-400 font-medium italic">{{ $t('marketplacePro.noCallForTendersInProgress') }}</p>
        </div>
      </div>
    </div>

    <!-- ===== MODAL PUBLICATION ===== -->
    <div v-if="showOfferModal" class="fixed inset-0 z-[100] flex items-center justify-center p-6 backdrop-blur-xl bg-black/40">
       <div class="bg-white w-full max-w-3xl rounded-[3rem] p-12 shadow-2xl relative overflow-hidden border border-white/20 animate-in fade-in zoom-in duration-300">
          <button @click="showOfferModal = false" class="absolute top-8 right-8 w-12 h-12 rounded-full hover:bg-gray-100 flex items-center justify-center transition-all bg-white shadow-sm border border-gray-100">
            <i class="bx bx-x text-3xl"></i>
          </button>

          <div class="flex items-center gap-4 mb-10">
            <div class="w-16 h-16 rounded-[1.5rem] bg-[#10b481] text-white flex items-center justify-center text-3xl shadow-xl shadow-[#10b481]/30">
              <i class="bx bx-spreadsheet"></i>
            </div>
            <div>
              <h2 class="text-3xl font-black text-[#112830]">{{ $t('marketplacePro.newSourcing') }}</h2>
              <p class="text-gray-400 font-medium">{{ $t('marketplacePro.defineYourNeedsForThisCallForTenders') }}</p>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div class="space-y-6">
               <div class="space-y-1">
                 <label class="text-[10px] font-black text-gray-400 uppercase tracking-[0.2em] ml-2">{{ $t('marketplacePro.targetProduct') }}</label>
                 <select class="w-full p-5 bg-gray-50 rounded-[1.5rem] border-none outline-none focus:ring-2 focus:ring-[#10b481]/30 transition-all font-bold text-[#112830]">
                   <option>{{ $t('marketplacePro.grainMaizeCoop') }}</option>
                   <option>{{ $t('marketplacePro.paddyRice') }}</option>
                   <option>{{ $t('marketplacePro.arabicaCoffee') }}</option>
                   <option>{{ $t('marketplacePro.blackVanilla') }}</option>
                 </select>
               </div>
               <div class="space-y-1">
                 <label class="text-[10px] font-black text-gray-400 uppercase tracking-[0.2em] ml-2">{{ $t('marketplacePro.totalVolumeTonnes') }}</label>
                 <input type="number" :placeholder="$t('marketplacePro.eG50')" class="w-full p-5 bg-gray-50 rounded-[1.5rem] border-none outline-none focus:ring-2 focus:ring-[#10b481]/30 transition-all font-bold text-[#112830]" />
               </div>
               <div class="space-y-1">
                 <label class="text-[10px] font-black text-gray-400 uppercase tracking-[0.2em] ml-2">{{ $t('marketplacePro.targetPriceArKg') }}</label>
                 <input type="number" :placeholder="$t('marketplacePro.eG1200')" class="w-full p-5 bg-gray-50 rounded-[1.5rem] border-none outline-none focus:ring-2 focus:ring-[#10b481]/30 transition-all font-bold text-[#112830]" />
               </div>
            </div>
            
            <div class="space-y-6">
               <div class="space-y-1">
                 <label class="text-[10px] font-black text-gray-400 uppercase tracking-[0.2em] ml-2">{{ $t('marketplacePro.submissionDeadline') }}</label>
                 <input type="date" class="w-full p-5 bg-gray-50 rounded-[1.5rem] border-none outline-none focus:ring-2 focus:ring-[#10b481]/30 transition-all font-bold text-[#112830]" />
               </div>
               <div class="space-y-1">
                 <label class="text-[10px] font-black text-gray-400 uppercase tracking-[0.2em] ml-2">{{ $t('marketplacePro.qualityCriteria') }}</label>
                 <textarea :placeholder="$t('marketplacePro.eGCertifiedOrganicMoisture14')" class="w-full h-[152px] p-5 bg-gray-50 rounded-[1.5rem] border-none outline-none focus:ring-2 focus:ring-[#10b481]/30 transition-all font-bold text-[#112830] resize-none"></textarea>
               </div>
            </div>
          </div>

          <div class="flex items-center gap-6 pt-10 mt-10 border-t border-gray-50">
             <div class="flex items-center gap-3 text-emerald-600">
               <i class="bx bx-check-shield text-2xl"></i>
               <span class="text-xs font-bold leading-tight">{{ $t('marketplacePro.yourCallWillBeSentTo') }}<br/>{{ $t('marketplacePro.t42CertifiedCooperatives') }}</span>
             </div>
             <button @click="showOfferModal = false" class="ml-auto px-12 py-5 bg-[#112830] text-white rounded-[2rem] font-black shadow-2xl shadow-[#112830]/30 hover:bg-[#10b481] transition-all duration-500">
               {{ $t('marketplacePro.publishTheCall') }}
             </button>
          </div>
       </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const { t: tr } = useI18n()
import { ref } from 'vue';

definePageMeta({ layout: 'dashboard' });

const showOfferModal = ref(false);

const insights = [
  { label: tr('marketplacePro.averageMaizePrice'), value: '1,250 Ar', trend: '+12%', trendUp: true, icon: 'bx bx-trending-up', bg: 'bg-emerald-50', text: 'text-emerald-600', sub: tr('marketplacePro.calculatedFrom18Transactions') },
  { label: tr('marketplacePro.qualityIndex'), value: 'A++', trend: 'Stable', trendUp: true, icon: 'bx bx-award', bg: 'bg-blue-50', text: 'text-blue-600', sub: tr('marketplacePro.globalgapCertifications') },
  { label: tr('marketplacePro.availableVolume'), value: '450 T', trend: '-5%', trendUp: false, icon: 'bx bx-package', bg: 'bg-amber-50', text: 'text-amber-600', sub: tr('marketplacePro.vakinankaratraRegion') },
];

const tenders = [
  { id: 'AO-2026-001', product: tr('marketplacePro.premiumGrainMaize'), volume: 150, deadline: tr('marketplacePro.t24March2026'), offers: 12, status: tr('marketplacePro.open') },
  { id: 'AO-2026-002', product: tr('marketplacePro.longGrainRice'), volume: 80, deadline: tr('marketplacePro.t05April2026'), offers: 5, status: tr('marketplacePro.open') },
  { id: 'AO-2026-003', product: tr('marketplacePro.organicArabicaCoffee'), volume: 20, deadline: tr('marketplacePro.t15Feb2026'), offers: 18, status: tr('marketplacePro.closed') },
];
</script>
