<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8">

    <!-- ===== HEADER ===== -->
    <PageHeader :title="orderDetail ? `Commande ${orderDetail.order_number}` : 'Détail commande'">
      <template #subtitle>
        <template v-if="orderDetail">
          <span :class="getStatusClass(orderDetail.status)" class="px-2.5 py-1 rounded-lg text-[9px] font-black uppercase tracking-wider">
            {{ getStatusLabel(orderDetail.status) }}
          </span>
          <span class="text-gray-400">· Reçue le {{ formatDate(orderDetail.created_at) }}</span>
        </template>
      </template>
      <template #breadcrumb>
        <NuxtLink to="/farmer/dashboard" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
          <span>Accueil</span>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <NuxtLink to="/farmer/marketplace/orders" class="hover:text-[#10b481] transition-colors">Commandes</NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">Détail</span>
      </template>
    </PageHeader>

    <!-- Loading -->
    <div v-if="loading" class="flex items-center justify-center py-24">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-[#10b481]"></div>
    </div>

    <template v-else-if="orderDetail">

      <!-- ===== ACTIONS BAR ===== -->
      <div
        v-if="orderDetail.status !== 'DELIVERED' && orderDetail.status !== 'CANCELLED'"
        class="bg-[#013b28] p-6 rounded-2xl shadow-xl flex flex-col md:flex-row items-center justify-between gap-6 mb-8"
      >
        <div class="flex items-center gap-4">
          <div class="w-12 h-12 bg-[#10b481] text-white rounded-xl flex items-center justify-center text-2xl">
            <i class="bx bx-zap"></i>
          </div>
          <div>
            <h3 class="text-white font-black text-sm">Action requise</h3>
            <p class="text-gray-400 text-xs font-medium">{{ getNextActionText(orderDetail.status) }}</p>
          </div>
        </div>
        <div class="flex gap-3 w-full md:w-auto">
          <button
            v-if="orderDetail.status === 'PAID'"
            @click="updateStatus('CONFIRMED')"
            class="flex-1 md:flex-none px-6 py-3 bg-[#10b481] text-white rounded-xl font-black text-[10px] uppercase tracking-widest hover:scale-105 transition-all shadow-lg"
          >Confirmer la commande</button>
          <button
            v-if="orderDetail.status === 'CONFIRMED'"
            @click="updateStatus('SHIPPED')"
            class="flex-1 md:flex-none px-6 py-3 bg-blue-500 text-white rounded-xl font-black text-[10px] uppercase tracking-widest hover:scale-105 transition-all shadow-lg"
          >Marquer expédiée</button>
          <button
            v-if="orderDetail.status === 'SHIPPED'"
            @click="updateStatus('DELIVERED')"
            class="flex-1 md:flex-none px-6 py-3 bg-emerald-500 text-white rounded-xl font-black text-[10px] uppercase tracking-widest hover:scale-105 transition-all shadow-lg"
          >Confirmer la livraison</button>
        </div>
      </div>

      <!-- ===== CONTENT GRID ===== -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Produits commandés -->
        <div class="lg:col-span-2">
          <div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
            <div class="p-6 border-b border-gray-50 flex items-center justify-between">
              <h3 class="text-base font-black text-[#112830]">Produits commandés</h3>
              <span class="px-3 py-1 bg-gray-50 text-gray-500 rounded-full text-[10px] font-black uppercase">{{ orderDetail.items?.length }} article(s)</span>
            </div>
            <div class="divide-y divide-gray-50">
              <div v-for="item in orderDetail.items" :key="item.id" class="p-6 flex gap-5 items-center">
                <div class="w-16 h-16 bg-gray-50 rounded-2xl overflow-hidden flex-shrink-0 border border-gray-100">
                  <img v-if="item.product_image" :src="item.product_image" class="w-full h-full object-cover" />
                  <i v-else class="bx bx-image text-gray-200 text-2xl flex items-center justify-center w-full h-full"></i>
                </div>
                <div class="flex-1 min-w-0">
                  <p class="text-base font-black text-[#112830] truncate">{{ item.product_name }}</p>
                  <p class="text-sm font-bold text-[#10b481]">{{ item.price }} Ar / unité</p>
                </div>
                <div class="text-right">
                  <p class="text-xs font-bold text-gray-400 uppercase tracking-widest">Quantité</p>
                  <p class="text-xl font-black text-[#112830]">x {{ item.quantity }}</p>
                </div>
                <div class="text-right pl-6 border-l border-gray-50 min-w-[100px]">
                  <p class="text-xs font-bold text-gray-400 uppercase tracking-widest">Sous-total</p>
                  <p class="text-lg font-black text-[#112830]">{{ item.subtotal }} Ar</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Sidebar : client + résumé -->
        <div class="space-y-6">
          <!-- Client -->
          <div class="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm space-y-5">
            <div class="flex items-center gap-3">
              <div class="w-9 h-9 bg-blue-50 text-blue-500 rounded-xl flex items-center justify-center text-lg">
                <i class="bx bx-user"></i>
              </div>
              <h3 class="text-base font-black text-[#112830]">Acheteur</h3>
            </div>
            <div class="p-4 bg-gray-50 rounded-xl flex items-center gap-3">
              <div class="w-9 h-9 bg-white rounded-full flex items-center justify-center font-black text-[#112830] shadow-sm border border-gray-100">
                {{ orderDetail.buyer_name?.charAt(0) }}
              </div>
              <div>
                <p class="text-sm font-black text-[#112830]">{{ orderDetail.buyer_name }}</p>
                <p class="text-[10px] font-bold text-gray-400">{{ orderDetail.buyer_details?.email }}</p>
              </div>
            </div>
            <div class="space-y-3 pt-1">
              <div class="flex items-center gap-3 text-sm text-gray-500">
                <i class="bx bx-phone text-gray-300"></i>
                <span class="font-bold">{{ orderDetail.delivery_phone || '—' }}</span>
              </div>
              <div class="flex items-start gap-3 text-sm text-gray-500">
                <i class="bx bx-map text-gray-300 mt-0.5"></i>
                <span class="font-bold">{{ orderDetail.delivery_address }}, {{ orderDetail.delivery_city }}</span>
              </div>
            </div>
          </div>

          <!-- Résumé financier -->
          <div class="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm space-y-5">
            <h3 class="text-base font-black text-[#112830]">Résumé financier</h3>
            <div class="space-y-3">
              <div class="flex justify-between text-sm">
                <span class="text-gray-400 font-bold">Produits</span>
                <span class="text-[#112830] font-black">{{ orderDetail.subtotal }} Ar</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-400 font-bold">Commission SmartSaha</span>
                <span class="text-rose-500 font-black">- 0 Ar</span>
              </div>
              <div class="pt-4 border-t border-gray-50 flex justify-between items-center">
                <span class="text-base font-black text-[#112830]">Net à recevoir</span>
                <span class="text-xl font-black text-[#10b481]">{{ orderDetail.subtotal }} Ar</span>
              </div>
              <div v-if="orderDetail.payment_status === 'ESCROWED'" class="mt-4 p-3 bg-emerald-50 text-emerald-600 rounded-xl text-[10px] font-black uppercase text-center tracking-widest border border-emerald-100">
                <i class="bx bx-lock-alt mr-1"></i>
                Fonds en séquestre
              </div>
            </div>
          </div>
        </div>
      </div>

    </template>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMarketplace } from '~/composables/useMarketplace'

definePageMeta({ layout: 'dashboard' })

const route = useRoute()
const router = useRouter()
const { orderDetail, loading, fetchOrderDetail, updateOrderStatus } = useMarketplace()

onMounted(() => {
  if (route.params.id) fetchOrderDetail(route.params.id as string)
})

const updateStatus = async (status: string) => {
  if (!confirm(`Confirmer le passage au statut : ${getStatusLabel(status)} ?`)) return
  try {
    await updateOrderStatus(orderDetail.value.id, status)
  } catch (err: any) {
    alert('Erreur lors de la mise à jour du statut')
  }
}

const formatDate = (dateStr: string) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' })
}

const getStatusLabel = (status: string) => {
  const map: any = {
    PENDING:   'En attente',
    PAID:      'Payé (À préparer)',
    CONFIRMED: 'En préparation',
    SHIPPED:   'Expédiée',
    DELIVERED: 'Livrée',
    CANCELLED: 'Annulée',
  }
  return map[status] || status
}

const getStatusClass = (status: string) => {
  switch (status) {
    case 'PAID':      return 'bg-emerald-50 text-[#10b481]'
    case 'CONFIRMED': return 'bg-blue-50 text-blue-600'
    case 'SHIPPED':   return 'bg-amber-50 text-amber-600'
    case 'DELIVERED': return 'bg-emerald-100 text-emerald-600'
    default:          return 'bg-gray-100 text-gray-600'
  }
}

const getNextActionText = (status: string) => {
  switch (status) {
    case 'PENDING':   return "En attente du règlement de l'acheteur."
    case 'PAID':      return 'Le paiement a été reçu. Préparez la commande et confirmez.'
    case 'CONFIRMED': return 'La commande est prête. Marquez-la comme expédiée.'
    case 'SHIPPED':   return 'Le colis est en route. Confirmez la livraison une fois reçue.'
    default:          return 'Aucune action requise.'
  }
}
</script>