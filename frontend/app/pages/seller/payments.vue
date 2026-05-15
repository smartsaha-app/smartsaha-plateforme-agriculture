<template>
  <div class="space-y-8">
    <!-- Header -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <h1 class="text-3xl font-black text-[#112830]">Mes Revenus</h1>
        <p class="text-gray-500 font-medium">Suivez vos ventes et gérez vos retraits.</p>
      </div>
      <div class="flex gap-4 w-full md:w-auto">
        <div class="flex-1 md:flex-none px-6 py-4 bg-emerald-50 rounded-[2rem] border border-emerald-100 flex items-center gap-4">
          <div class="w-10 h-10 bg-[#10b481] text-white rounded-xl flex items-center justify-center text-xl shadow-lg shadow-[#10b481]/20">
            <i class="bx bx-trending-up"></i>
          </div>
          <div>
            <p class="text-[10px] font-black text-[#10b481] uppercase tracking-widest">Solde Disponible</p>
            <p class="text-xl font-black text-[#112830]">{{ formatAmount(sellerStats.available_balance) }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Stats Grid -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-white p-8 rounded-[2.5rem] border border-gray-100 shadow-sm space-y-4">
        <div class="w-12 h-12 bg-blue-50 text-blue-500 rounded-2xl flex items-center justify-center text-2xl">
          <i class="bx bx-shopping-bag"></i>
        </div>
        <div>
          <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest">Ventes Totales</p>
          <p class="text-2xl font-black text-[#112830]">{{ formatAmount(sellerStats.total_sales) }}</p>
        </div>
      </div>
      
      <div class="bg-white p-8 rounded-[2.5rem] border border-gray-100 shadow-sm space-y-4">
        <div class="w-12 h-12 bg-amber-50 text-amber-500 rounded-2xl flex items-center justify-center text-2xl">
          <i class="bx bx-lock-alt"></i>
        </div>
        <div>
          <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest">En Séquestre (Escrow)</p>
          <p class="text-2xl font-black text-[#112830]">{{ formatAmount(sellerStats.escrow_balance) }}</p>
        </div>
      </div>

      <div class="bg-[#112830] p-8 rounded-[2.5rem] shadow-xl shadow-[#112830]/20 space-y-4 flex flex-col justify-between">
        <div>
          <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest">Actions</p>
          <h3 class="text-white font-black text-lg">Demander un retrait</h3>
        </div>
        <button class="w-full py-3 bg-[#10b481] text-white rounded-2xl font-black text-[10px] uppercase tracking-widest hover:bg-[#0da072] transition-all">
          Retirer mes fonds
        </button>
      </div>
    </div>

    <!-- History -->
    <div class="bg-white rounded-[3rem] border border-gray-100 shadow-sm overflow-hidden">
      <div class="p-8 border-b border-gray-50 flex items-center justify-between">
        <h3 class="text-lg font-black text-[#112830]">Derniers encaissements</h3>
        <button class="text-xs font-black text-[#10b481] uppercase tracking-widest hover:underline">Tout voir</button>
      </div>
      <div class="p-12 text-center space-y-4">
        <div class="w-16 h-16 bg-gray-50 rounded-full flex items-center justify-center mx-auto text-gray-200">
          <i class="bx bx-transfer text-3xl"></i>
        </div>
        <p class="text-gray-400 font-medium">Aucune transaction récente à afficher.</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useMarketplace } from '~/composables/useMarketplace';

definePageMeta({
  layout: 'dashboard'
});

const { sellerStats, loading, fetchSellerStats } = useMarketplace();

onMounted(() => {
  fetchSellerStats();
});

const formatAmount = (val: number) => {
  return new Intl.NumberFormat('fr-MG').format(val) + ' Ar';
};
</script>
