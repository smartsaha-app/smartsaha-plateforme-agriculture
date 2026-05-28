<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8">

    <!-- ===== HEADER ===== -->
    <PageHeader title="Mes Revenus">
      <template #subtitle>
        <i class="bx bx-wallet"></i>
        Suivez vos ventes et gérez vos retraits
      </template>
      <template #breadcrumb>
        <NuxtLink to="/farmer/dashboard" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
          <span>Accueil</span>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-gray-400">Marketplace</span>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">Revenus</span>
      </template>
    </PageHeader>

    <!-- ===== SOLDE DISPONIBLE (highlight) ===== -->
    <div class="flex flex-col md:flex-row gap-4 mb-8">
      <div class="flex-1 px-6 py-5 bg-emerald-50 rounded-2xl border border-emerald-100 flex items-center gap-4">
        <div class="w-12 h-12 bg-[#10b481] text-white rounded-xl flex items-center justify-center text-2xl shadow-lg shadow-[#10b481]/20">
          <i class="bx bx-trending-up"></i>
        </div>
        <div>
          <p class="text-[10px] font-black text-[#10b481] uppercase tracking-widest">Solde Disponible</p>
          <p class="text-2xl font-black text-[#112830]">{{ formatAmount(sellerStats.available_balance) }}</p>
        </div>
      </div>
    </div>

    <!-- ===== STATS GRID ===== -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <div class="bg-white p-7 rounded-2xl border border-gray-100 shadow-sm space-y-4">
        <div class="w-11 h-11 bg-blue-50 text-blue-500 rounded-xl flex items-center justify-center text-xl">
          <i class="bx bx-shopping-bag"></i>
        </div>
        <div>
          <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest">Ventes Totales</p>
          <p class="text-2xl font-black text-[#112830]">{{ formatAmount(sellerStats.total_sales) }}</p>
        </div>
      </div>

      <div class="bg-white p-7 rounded-2xl border border-gray-100 shadow-sm space-y-4">
        <div class="w-11 h-11 bg-amber-50 text-amber-500 rounded-xl flex items-center justify-center text-xl">
          <i class="bx bx-lock-alt"></i>
        </div>
        <div>
          <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest">En Séquestre (Escrow)</p>
          <p class="text-2xl font-black text-[#112830]">{{ formatAmount(sellerStats.escrow_balance) }}</p>
        </div>
      </div>

      <div class="bg-[#013b28] p-7 rounded-2xl shadow-xl shadow-[#013b28]/20 space-y-4 flex flex-col justify-between">
        <div>
          <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest">Actions</p>
          <h3 class="text-white font-black text-lg">Demander un retrait</h3>
        </div>
        <button class="w-full py-3 bg-[#10b481] text-white rounded-xl font-black text-[10px] uppercase tracking-widest hover:bg-[#0da072] transition-all">
          Retirer mes fonds
        </button>
      </div>
    </div>

    <!-- ===== HISTORIQUE ENCAISSEMENTS ===== -->
    <div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
      <div class="p-6 border-b border-gray-50 flex items-center justify-between">
        <h3 class="text-base font-black text-[#112830]">Derniers encaissements</h3>
        <NuxtLink to="/farmer/marketplace/history" class="text-xs font-black text-[#10b481] uppercase tracking-widest hover:underline">
          Tout voir →
        </NuxtLink>
      </div>
      <div class="p-12 text-center space-y-4">
        <div class="w-16 h-16 bg-gray-50 rounded-full flex items-center justify-center mx-auto text-gray-200">
          <i class="bx bx-transfer text-3xl"></i>
        </div>
        <p class="text-gray-400 font-medium text-sm">Aucune transaction récente à afficher.</p>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useMarketplace } from '~/composables/useMarketplace'

definePageMeta({ layout: 'dashboard' })

const { sellerStats, loading, fetchSellerStats } = useMarketplace()

onMounted(() => {
  fetchSellerStats()
})

const formatAmount = (val: number) =>
  new Intl.NumberFormat('fr-MG').format(val || 0) + ' Ar'
</script>