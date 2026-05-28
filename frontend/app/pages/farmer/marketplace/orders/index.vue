<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8">

    <!-- ===== HEADER ===== -->
    <PageHeader title="Commandes reçues">
      <template #subtitle>
        <i class="bx bx-shopping-bag"></i>
        Suivez et gérez les commandes de vos acheteurs
      </template>
      <template #breadcrumb>
        <NuxtLink to="/farmer/dashboard" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
          <span>Accueil</span>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-gray-400">Marketplace</span>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">Commandes</span>
      </template>
    </PageHeader>

    <!-- ===== STATUS FILTERS ===== -->
    <div class="flex gap-2 flex-wrap mb-6">
      <button
        v-for="status in statusFilters"
        :key="status.id"
        @click="activeStatus = status.id"
        :class="activeStatus === status.id ? 'bg-[#013b28] text-white' : 'bg-white text-gray-400 border border-gray-100 hover:border-gray-200'"
        class="px-5 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all shadow-sm"
      >
        {{ status.label }}
      </button>
    </div>

    <!-- ===== ORDERS TABLE ===== -->
    <div v-if="loading" class="space-y-4 animate-pulse">
      <div v-for="i in 5" :key="i" class="h-24 bg-white rounded-2xl border border-gray-100 shadow-sm"></div>
    </div>

    <div v-else-if="filteredOrders.length === 0" class="bg-white py-24 rounded-2xl border border-gray-100 text-center space-y-6 shadow-sm">
      <div class="w-24 h-24 bg-gray-50 rounded-full flex items-center justify-center mx-auto text-gray-200">
        <i class="bx bx-shopping-bag text-5xl"></i>
      </div>
      <div class="space-y-2">
        <h3 class="text-xl font-black text-[#112830]">Aucune commande</h3>
        <p class="text-gray-400 max-w-sm mx-auto">Vous n'avez pas de commandes correspondant à ce statut pour le moment.</p>
      </div>
    </div>

    <div v-else class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
      <table class="w-full text-left">
        <thead>
          <tr class="bg-gray-50/50 border-b border-gray-100">
            <th class="px-6 py-4 text-[10px] font-black text-gray-400 uppercase tracking-widest">N° Commande</th>
            <th class="px-6 py-4 text-[10px] font-black text-gray-400 uppercase tracking-widest">Acheteur</th>
            <th class="px-6 py-4 text-[10px] font-black text-gray-400 uppercase tracking-widest">Articles</th>
            <th class="px-6 py-4 text-[10px] font-black text-gray-400 uppercase tracking-widest">Total</th>
            <th class="px-6 py-4 text-[10px] font-black text-gray-400 uppercase tracking-widest">Statut</th>
            <th class="px-6 py-4"></th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-50">
          <tr
            v-for="order in filteredOrders"
            :key="order.id"
            class="hover:bg-gray-50/50 transition-colors cursor-pointer"
            @click="navigateTo(`/farmer/marketplace/orders/${order.id}`)"
          >
            <td class="px-6 py-5">
              <p class="font-black text-[#112830] text-sm">{{ order.order_number }}</p>
              <p class="text-[10px] text-gray-400 font-bold uppercase tracking-widest">{{ new Date(order.created_at).toLocaleDateString('fr-FR') }}</p>
            </td>
            <td class="px-6 py-5">
              <div class="flex items-center gap-3">
                <div class="w-9 h-9 bg-gray-100 rounded-xl flex items-center justify-center text-gray-400">
                  <i class="bx bx-user text-xl"></i>
                </div>
                <div>
                  <p class="text-sm font-black text-[#112830]">{{ order.buyer_name || 'Client' }}</p>
                  <p class="text-[10px] text-gray-400 font-bold">{{ order.buyer_email }}</p>
                </div>
              </div>
            </td>
            <td class="px-6 py-5">
              <div class="flex -space-x-2">
                <div v-for="item in order.items?.slice(0, 3)" :key="item.id" class="w-8 h-8 rounded-lg ring-2 ring-white bg-gray-50 overflow-hidden border border-gray-100">
                  <img v-if="item.product_image" :src="item.product_image" class="h-full w-full object-cover">
                  <div v-else class="h-full w-full flex items-center justify-center text-gray-300">
                    <i class="bx bx-image text-xs"></i>
                  </div>
                </div>
                <div v-if="order.items?.length > 3" class="w-8 h-8 rounded-lg ring-2 ring-white bg-gray-100 flex items-center justify-center text-[10px] font-black text-gray-400">
                  +{{ order.items.length - 3 }}
                </div>
              </div>
            </td>
            <td class="px-6 py-5">
              <p class="font-black text-[#10b481] text-sm">{{ order.total }} Ar</p>
            </td>
            <td class="px-6 py-5" @click.stop>
              <div class="relative group/status">
                <button class="flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-[9px] font-black uppercase tracking-widest border border-gray-100 hover:border-[#10b481] transition-all" :class="getStatusClass(order.status)">
                  {{ getStatusLabel(order.status) }}
                  <i class="bx bx-chevron-down text-xs"></i>
                </button>
                <div class="absolute top-full left-0 mt-2 w-44 bg-white border border-gray-100 rounded-xl shadow-xl hidden group-hover/status:block z-20 overflow-hidden">
                  <button
                    v-for="s in ['PAID', 'CONFIRMED', 'SHIPPED', 'DELIVERED', 'CANCELLED']"
                    :key="s"
                    @click="handleUpdateStatus(order, s)"
                    class="w-full text-left px-4 py-2.5 text-[9px] font-black uppercase tracking-widest hover:bg-gray-50 transition-colors"
                  >{{ getStatusLabel(s) }}</button>
                </div>
              </div>
            </td>
            <td class="px-6 py-5 text-right">
              <NuxtLink :to="`/farmer/marketplace/orders/${order.id}`" class="w-9 h-9 rounded-xl hover:bg-gray-50 text-gray-400 hover:text-[#112830] transition-all flex items-center justify-center ml-auto" @click.stop>
                <i class="bx bx-show text-xl"></i>
              </NuxtLink>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useMarketplace } from '~/composables/useMarketplace'

definePageMeta({ layout: 'dashboard' })

const { orders, loading, fetchOrders, updateOrderStatus } = useMarketplace()
const activeStatus = ref('ALL')

const statusFilters = [
  { id: 'ALL',       label: 'En cours' },
  { id: 'PENDING',   label: 'En attente' },
  { id: 'PAID',      label: 'À préparer' },
  { id: 'SHIPPED',   label: 'Expédiées' },
  { id: 'DELIVERED', label: 'Livrées' },
]

onMounted(async () => {
  await fetchOrders({ as_seller: 'true' })
})

const filteredOrders = computed(() => {
  const all = orders.value || []
  if (activeStatus.value === 'ALL') return all.filter(o => o.status !== 'DELIVERED' && o.status !== 'CANCELLED')
  return all.filter(o => o.status === activeStatus.value)
})

const getStatusLabel = (status: string) => {
  const map: any = {
    PENDING:   'En attente',
    PAID:      'À préparer',
    CONFIRMED: 'En préparation',
    SHIPPED:   'Expédiée',
    DELIVERED: 'Livrée',
    CANCELLED: 'Annulée',
  }
  return map[status] || status
}

const getStatusClass = (status: string) => {
  switch (status) {
    case 'PENDING':   return 'text-amber-600 bg-amber-50'
    case 'PAID':      return 'text-emerald-600 bg-emerald-50'
    case 'SHIPPED':   return 'text-blue-600 bg-blue-50'
    case 'DELIVERED': return 'text-emerald-600 bg-emerald-100'
    case 'CANCELLED': return 'text-rose-600 bg-rose-50'
    default:          return 'text-gray-600 bg-gray-50'
  }
}

const handleUpdateStatus = async (order: any, newStatus: string) => {
  try {
    await updateOrderStatus(order.id, newStatus)
  } catch (err) {
    alert('Erreur lors de la mise à jour du statut')
  }
}
</script>