<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8">

    <!-- ===== HEADER ===== -->
    <PageHeader title="Historique des ventes">
      <template #subtitle>
        <i class="bx bx-history"></i>
        Consultez l'ensemble de vos transactions terminées
      </template>
      <template #breadcrumb>
        <NuxtLink to="/farmer/dashboard" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
          <span>Accueil</span>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-gray-400">Marketplace</span>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">Historique</span>
      </template>
    </PageHeader>

    <!-- ===== TABLE ===== -->
    <div v-if="loading" class="space-y-4 animate-pulse">
      <div v-for="i in 5" :key="i" class="h-24 bg-white rounded-2xl border border-gray-100 shadow-sm"></div>
    </div>

    <div v-else-if="filteredOrders.length === 0" class="bg-white py-24 rounded-2xl border border-gray-100 text-center space-y-6 shadow-sm">
      <div class="w-24 h-24 bg-gray-50 rounded-full flex items-center justify-center mx-auto text-gray-200">
        <i class="bx bx-history text-5xl"></i>
      </div>
      <div class="space-y-2">
        <h3 class="text-xl font-black text-[#112830]">Aucun historique</h3>
        <p class="text-gray-400 max-w-sm mx-auto">Vous n'avez pas encore de ventes terminées.</p>
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
          <tr v-for="order in filteredOrders" :key="order.id" class="hover:bg-gray-50/50 transition-colors">
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
                  <p class="text-sm font-black text-[#112830]">{{ order.buyer_details?.username || 'Client' }}</p>
                  <p class="text-[10px] text-gray-400 font-bold">{{ order.buyer_details?.email }}</p>
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
            <td class="px-6 py-5">
              <span class="px-3 py-1.5 rounded-xl text-[9px] font-black uppercase tracking-widest border border-gray-100" :class="getStatusClass(order.status)">
                {{ getStatusLabel(order.status) }}
              </span>
            </td>
            <td class="px-6 py-5 text-right">
              <NuxtLink :to="`/farmer/marketplace/orders/${order.id}`" class="w-9 h-9 rounded-xl hover:bg-gray-50 text-gray-400 hover:text-[#112830] transition-all flex items-center justify-center ml-auto">
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
import { useApi } from '~/composables/useApi'

definePageMeta({ layout: 'dashboard' })

const { apiFetch } = useApi()
const orders = ref<any[]>([])
const loading = ref(true)

const filteredOrders = computed(() =>
  orders.value.filter(o => o.status === 'DELIVERED' || o.status === 'CANCELLED')
)

onMounted(async () => {
  try {
    const data = await apiFetch('/api/orders/orders/?as_seller=true')
    orders.value = data.results || data
  } catch (err) {
    console.error('Erreur chargement historique', err)
  } finally {
    loading.value = false
  }
})

const getStatusLabel = (status: string) => {
  const map: any = {
    DELIVERED: 'Livrée',
    CANCELLED: 'Annulée',
    PAID:      'Payée',
    SHIPPED:   'Expédiée',
  }
  return map[status] || status
}

const getStatusClass = (status: string) => {
  switch (status) {
    case 'DELIVERED': return 'text-emerald-600 bg-emerald-50'
    case 'CANCELLED': return 'text-rose-600 bg-rose-50'
    case 'PAID':      return 'text-emerald-600 bg-emerald-50'
    case 'SHIPPED':   return 'text-blue-600 bg-blue-50'
    default:          return 'text-gray-600 bg-gray-50'
  }
}
</script>