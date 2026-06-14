<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8 space-y-6">

    <!-- HEADER -->
    <PageHeader title="Gestion des abonnements">
      <template #subtitle>
        <i class="bx bx-crown"></i>
        Gérer les plans FREE / PRO des utilisateurs
      </template>
      <template #breadcrumb>
        <NuxtLink to="/admin" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
          <span>Tableau de bord</span>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">Abonnements</span>
      </template>
    </PageHeader>

    <!-- STATS -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div v-for="stat in statsCards" :key="stat.label"
        class="bg-white rounded-2xl border border-gray-100 shadow-sm p-5 flex items-center gap-4">
        <div :class="['w-11 h-11 rounded-xl flex items-center justify-center flex-shrink-0', stat.bg]">
          <i :class="['text-xl', stat.icon, stat.color]"></i>
        </div>
        <div class="min-w-0">
          <p class="text-2xl font-black text-[#112830]">{{ stat.value ?? '—' }}</p>
          <p class="text-[10px] font-bold text-gray-400 uppercase tracking-widest truncate">{{ stat.label }}</p>
        </div>
      </div>
    </div>

    <!-- FILTERS -->
    <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-3 flex flex-wrap items-center gap-2">
      <div class="flex-1 min-w-[180px] relative">
        <i class="bx bx-search absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-base pointer-events-none"></i>
        <input v-model="searchQuery" type="text" placeholder="Rechercher par email ou nom…"
          class="w-full pl-9 pr-8 py-2.5 bg-gray-50 border border-gray-100 rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/30 transition-all font-medium text-[#112830]" />
        <button v-if="searchQuery" @click="searchQuery = ''" class="absolute right-2.5 top-1/2 -translate-y-1/2 text-gray-300 hover:text-gray-500">
          <i class="bx bx-x"></i>
        </button>
      </div>
      <div class="hidden md:block w-px h-7 bg-gray-100 flex-shrink-0"></div>
      <div class="flex gap-1 flex-shrink-0">
        <button v-for="f in planFilters" :key="f.val" @click="selectedPlan = f.val"
          :class="['px-4 py-2 rounded-xl text-xs font-bold transition-all', selectedPlan === f.val ? 'bg-[#112830] text-white' : 'bg-gray-50 text-gray-400 hover:bg-gray-100']">
          {{ f.label }}
        </button>
      </div>
      <div class="hidden md:block w-px h-7 bg-gray-100 flex-shrink-0"></div>
      <div class="flex gap-1 flex-shrink-0">
        <button v-for="f in statusFilters" :key="f.val" @click="selectedStatus = f.val"
          :class="['px-4 py-2 rounded-xl text-xs font-bold transition-all', selectedStatus === f.val ? 'bg-[#112830] text-white' : 'bg-gray-50 text-gray-400 hover:bg-gray-100']">
          {{ f.label }}
        </button>
      </div>
      <span class="ml-auto text-xs font-bold text-gray-400 whitespace-nowrap flex-shrink-0">
        {{ subscriptions.length }} abonnement{{ subscriptions.length !== 1 ? 's' : '' }}
      </span>
    </div>

    <!-- TABLE -->
    <div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
      <div v-if="isLoading" class="py-20 flex flex-col items-center gap-4">
        <div class="w-10 h-10 border-2 border-[#10b481] border-t-transparent rounded-full animate-spin"></div>
        <p class="text-xs font-bold text-gray-400 uppercase tracking-widest">Chargement…</p>
      </div>

      <div v-else-if="subscriptions.length === 0" class="py-20 text-center space-y-4">
        <div class="w-16 h-16 bg-gray-50 rounded-2xl flex items-center justify-center mx-auto">
          <i class="bx bx-crown text-4xl text-gray-200"></i>
        </div>
        <p class="text-sm text-gray-400 font-medium">Aucun abonnement trouvé</p>
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full text-left">
          <thead>
            <tr class="bg-gray-50/70 border-b border-gray-100">
              <th class="px-6 py-4 text-[9px] font-black text-gray-400 uppercase tracking-widest">Utilisateur</th>
              <th class="px-6 py-4 text-[9px] font-black text-gray-400 uppercase tracking-widest">Plan</th>
              <th class="px-6 py-4 text-[9px] font-black text-gray-400 uppercase tracking-widest">Statut</th>
              <th class="px-6 py-4 text-[9px] font-black text-gray-400 uppercase tracking-widest hidden md:table-cell">Expiration</th>
              <th class="px-6 py-4 text-[9px] font-black text-gray-400 uppercase tracking-widest hidden lg:table-cell">Provider</th>
              <th class="px-6 py-4 text-[9px] font-black text-gray-400 uppercase tracking-widest text-right">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-50">
            <tr v-for="sub in subscriptions" :key="sub.id" class="hover:bg-gray-50/50 transition-colors group">
              <!-- User -->
              <td class="px-6 py-4">
                <div class="flex items-center gap-3">
                  <div class="w-9 h-9 rounded-xl bg-[#112830] text-white flex items-center justify-center font-black text-sm flex-shrink-0">
                    {{ (sub.user.first_name || sub.user.username || '?').charAt(0).toUpperCase() }}
                  </div>
                  <div class="min-w-0">
                    <p class="text-sm font-black text-[#112830] group-hover:text-[#10b481] transition-colors truncate">
                      {{ sub.user.first_name }} {{ sub.user.last_name }}
                    </p>
                    <p class="text-xs text-gray-400 truncate">{{ sub.user.email }}</p>
                  </div>
                </div>
              </td>

              <!-- Plan badge -->
              <td class="px-6 py-4">
                <span :class="['inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-[10px] font-black uppercase tracking-widest border',
                  sub.plan === 'PRO' ? 'bg-amber-50 text-amber-600 border-amber-100' : 'bg-gray-50 text-gray-500 border-gray-100']">
                  <i :class="sub.plan === 'PRO' ? 'bx bxs-crown' : 'bx bx-user'" class="text-xs"></i>
                  {{ sub.plan }}
                </span>
              </td>

              <!-- Status badge -->
              <td class="px-6 py-4">
                <span :class="['px-2.5 py-1 rounded-lg text-[10px] font-black uppercase tracking-widest border',
                  sub.status === 'ACTIVE' ? 'bg-emerald-50 text-emerald-600 border-emerald-100'
                  : sub.status === 'EXPIRED' ? 'bg-orange-50 text-orange-500 border-orange-100'
                  : 'bg-rose-50 text-rose-500 border-rose-100']">
                  {{ statusLabel(sub.status) }}
                </span>
              </td>

              <!-- Expiry -->
              <td class="px-6 py-4 hidden md:table-cell">
                <span class="text-xs font-medium text-gray-400">
                  {{ sub.expires_at ? formatDate(sub.expires_at) : '∞' }}
                </span>
              </td>

              <!-- Provider -->
              <td class="px-6 py-4 hidden lg:table-cell">
                <span class="text-xs font-medium text-gray-400">{{ sub.provider ?? '—' }}</span>
              </td>

              <!-- Actions -->
              <td class="px-6 py-4">
                <div class="flex items-center justify-end gap-2">
                  <button @click="openSetPlanModal(sub)"
                    class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold border bg-amber-50 border-amber-100 text-amber-600 hover:bg-amber-500 hover:text-white hover:border-amber-500 transition-all"
                    title="Modifier le plan">
                    <i class="bx bx-crown text-sm"></i>
                    <span class="hidden lg:inline">Modifier plan</span>
                  </button>
                  <button v-if="sub.status === 'ACTIVE'" @click="confirmCancel(sub)"
                    class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold border bg-rose-50 border-rose-100 text-rose-500 hover:bg-rose-500 hover:text-white hover:border-rose-500 transition-all"
                    title="Annuler l'abonnement">
                    <i class="bx bx-x text-sm"></i>
                    <span class="hidden lg:inline">Annuler</span>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- MODAL: Set Plan -->
    <div v-if="showSetPlanModal && selectedSub" class="fixed inset-0 z-[100] flex items-center justify-center p-6 backdrop-blur-sm bg-black/20">
      <div class="bg-white w-full max-w-md rounded-2xl p-8 shadow-2xl space-y-5 border border-gray-100">
        <div class="flex items-center gap-3 mb-1">
          <div class="w-11 h-11 bg-[#112830] rounded-xl flex items-center justify-center flex-shrink-0">
            <i class="bx bxs-crown text-amber-400 text-lg"></i>
          </div>
          <div>
            <h2 class="text-base font-black text-[#112830]">Modifier le plan</h2>
            <p class="text-xs text-gray-400">{{ selectedSub.user.email }}</p>
          </div>
        </div>

        <div class="space-y-4">
          <!-- Plan choice -->
          <div class="space-y-1.5">
            <label class="text-[9px] font-black text-gray-400 uppercase tracking-widest block">Plan</label>
            <div class="flex gap-3">
              <button v-for="p in ['FREE', 'PRO']" :key="p" @click="planForm.plan = p"
                :class="['flex-1 py-3 rounded-xl font-black text-sm border transition-all',
                  planForm.plan === p ? 'bg-[#112830] text-white border-[#112830]' : 'bg-gray-50 text-gray-500 border-gray-100 hover:border-gray-300']">
                {{ p }}
              </button>
            </div>
          </div>

          <!-- Duration (PRO only) -->
          <div v-if="planForm.plan === 'PRO'" class="space-y-1.5">
            <label class="text-[9px] font-black text-gray-400 uppercase tracking-widest block">Durée (jours)</label>
            <div class="flex gap-2 flex-wrap">
              <button v-for="d in [30, 90, 180, 365]" :key="d" @click="planForm.duration_days = d"
                :class="['px-4 py-2 rounded-xl text-xs font-bold border transition-all',
                  planForm.duration_days === d ? 'bg-amber-500 text-white border-amber-500' : 'bg-gray-50 text-gray-500 border-gray-100 hover:border-gray-300']">
                {{ d }}j
              </button>
            </div>
            <input v-model.number="planForm.duration_days" type="number" min="1" max="3650"
              class="w-full px-4 py-2.5 bg-gray-50 border border-gray-100 rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/30 font-medium" />
          </div>

          <!-- Payment ref -->
          <div class="space-y-1.5">
            <label class="text-[9px] font-black text-gray-400 uppercase tracking-widest block">Référence paiement (optionnel)</label>
            <input v-model="planForm.payment_ref" type="text" placeholder="ex: STRIPE-abc123"
              class="w-full px-4 py-2.5 bg-gray-50 border border-gray-100 rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/30 font-medium" />
          </div>

          <!-- Provider -->
          <div class="space-y-1.5">
            <label class="text-[9px] font-black text-gray-400 uppercase tracking-widest block">Provider</label>
            <select v-model="planForm.provider"
              class="w-full px-4 py-2.5 bg-gray-50 border border-gray-100 rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/30 font-medium">
              <option value="MANUAL">Manuel (admin)</option>
              <option value="STRIPE">Stripe</option>
              <option value="MVOLA">MVola</option>
              <option value="ORANGE_MONEY">Orange Money</option>
              <option value="AIRTEL_MONEY">Airtel Money</option>
            </select>
          </div>
        </div>

        <div class="flex gap-3 pt-1">
          <button @click="showSetPlanModal = false"
            class="flex-1 py-3 rounded-xl border border-gray-100 text-gray-500 font-bold text-sm hover:bg-gray-50 transition-colors">
            Annuler
          </button>
          <button @click="submitSetPlan" :disabled="isSaving"
            class="flex-1 py-3 rounded-xl bg-[#112830] text-white font-bold text-sm hover:bg-[#10b481] transition-all disabled:opacity-40 flex items-center justify-center gap-2">
            <div v-if="isSaving" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            <i v-else class="bx bx-check"></i>
            Enregistrer
          </button>
        </div>
      </div>
    </div>

    <!-- MODAL: Cancel confirm -->
    <div v-if="subToCancel" class="fixed inset-0 z-[100] flex items-center justify-center p-6 backdrop-blur-sm bg-black/20">
      <div class="bg-white w-full max-w-sm rounded-2xl p-8 shadow-2xl space-y-5 border border-gray-100">
        <div class="text-center space-y-3">
          <div class="w-14 h-14 bg-rose-50 rounded-2xl flex items-center justify-center mx-auto">
            <i class="bx bx-x-circle text-2xl text-rose-500"></i>
          </div>
          <div>
            <h2 class="text-base font-black text-[#112830]">Annuler l'abonnement ?</h2>
            <p class="text-sm text-gray-400 mt-1">
              L'utilisateur <span class="font-bold text-[#112830]">{{ subToCancel.user.email }}</span>
              sera rétrogradé en plan <span class="font-bold">FREE</span>.
            </p>
          </div>
        </div>
        <div class="flex gap-3">
          <button @click="subToCancel = null"
            class="flex-1 py-3 rounded-xl border border-gray-100 text-gray-500 font-bold text-sm hover:bg-gray-50 transition-colors">
            Retour
          </button>
          <button @click="executeCancel" :disabled="isSaving"
            class="flex-1 py-3 rounded-xl bg-rose-500 text-white font-bold text-sm hover:bg-rose-600 transition-all disabled:opacity-40 flex items-center justify-center gap-2">
            <div v-if="isSaving" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            <span v-else>Confirmer</span>
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useApi } from '~/composables/useApi'

const { apiFetch } = useApi()

// ── Types ──────────────────────────────────────────────────────────────────────
interface SubUser { uuid: string; email: string; username: string; first_name: string; last_name: string; role: string; plan: string; plan_expires_at: string | null }
interface Subscription { id: string; user: SubUser; plan: string; status: string; started_at: string; expires_at: string | null; payment_ref: string | null; provider: string | null }

// ── State ─────────────────────────────────────────────────────────────────────
const isLoading    = ref(false)
const isSaving     = ref(false)
const subscriptions = ref<Subscription[]>([])
const statsData    = ref<{ total_users: number; pro_users: number; free_users: number; active_subscriptions: number } | null>(null)

const searchQuery  = ref('')
const selectedPlan = ref('')
const selectedStatus = ref('')

const showSetPlanModal = ref(false)
const selectedSub  = ref<Subscription | null>(null)
const subToCancel  = ref<Subscription | null>(null)

const planForm = ref({ plan: 'PRO', duration_days: 30, payment_ref: '', provider: 'MANUAL' })

// ── Filters ───────────────────────────────────────────────────────────────────
const planFilters   = [{ val: '', label: 'Tous' }, { val: 'PRO', label: 'PRO' }, { val: 'FREE', label: 'Gratuit' }]
const statusFilters = [{ val: '', label: 'Tous' }, { val: 'ACTIVE', label: 'Actif' }, { val: 'EXPIRED', label: 'Expiré' }, { val: 'CANCELLED', label: 'Annulé' }]

// ── Stats cards ───────────────────────────────────────────────────────────────
const statsCards = computed(() => [
  { label: 'Total utilisateurs', value: statsData.value?.total_users, icon: 'bx bx-group',   bg: 'bg-blue-50',   color: 'text-blue-500' },
  { label: 'Abonnés PRO',        value: statsData.value?.pro_users,   icon: 'bx bxs-crown',  bg: 'bg-amber-50',  color: 'text-amber-500' },
  { label: 'Utilisateurs FREE',  value: statsData.value?.free_users,  icon: 'bx bx-user',    bg: 'bg-gray-100',  color: 'text-gray-400' },
  { label: 'Abonnements actifs', value: statsData.value?.active_subscriptions, icon: 'bx bx-check-circle', bg: 'bg-emerald-50', color: 'text-emerald-500' },
])

// ── Helpers ───────────────────────────────────────────────────────────────────
function statusLabel(s: string) {
  return s === 'ACTIVE' ? 'Actif' : s === 'EXPIRED' ? 'Expiré' : 'Annulé'
}

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' })
}

// ── Data fetching ─────────────────────────────────────────────────────────────
async function fetchSubscriptions() {
  isLoading.value = true
  try {
    const params = new URLSearchParams()
    if (searchQuery.value)   params.set('search', searchQuery.value)
    if (selectedPlan.value)  params.set('plan',   selectedPlan.value)
    if (selectedStatus.value) params.set('status', selectedStatus.value)
    const qs = params.toString() ? `?${params}` : ''
    subscriptions.value = await apiFetch(`/api/admin/subscriptions/${qs}`)
  } catch (e) {
    subscriptions.value = []
  } finally {
    isLoading.value = false
  }
}

async function fetchStats() {
  try {
    statsData.value = await apiFetch('/api/admin/subscriptions/stats/')
  } catch (_) {}
}

// ── Actions ───────────────────────────────────────────────────────────────────
function openSetPlanModal(sub: Subscription) {
  selectedSub.value = sub
  planForm.value = { plan: sub.plan, duration_days: 30, payment_ref: '', provider: 'MANUAL' }
  showSetPlanModal.value = true
}

async function submitSetPlan() {
  if (!selectedSub.value) return
  isSaving.value = true
  try {
    await apiFetch(`/api/admin/subscriptions/set-plan/${selectedSub.value.user.uuid}/`, {
      method: 'POST',
      body: planForm.value,
    })
    showSetPlanModal.value = false
    await fetchSubscriptions()
    await fetchStats()
  } catch (_) {
  } finally {
    isSaving.value = false
  }
}

function confirmCancel(sub: Subscription) {
  subToCancel.value = sub
}

async function executeCancel() {
  if (!subToCancel.value) return
  isSaving.value = true
  try {
    await apiFetch(`/api/admin/subscriptions/${subToCancel.value.id}/cancel/`, { method: 'POST' })
    subToCancel.value = null
    await fetchSubscriptions()
    await fetchStats()
  } catch (_) {
  } finally {
    isSaving.value = false
  }
}

// ── Watchers ──────────────────────────────────────────────────────────────────
let debounceTimer: ReturnType<typeof setTimeout>
watch([searchQuery, selectedPlan, selectedStatus], () => {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(fetchSubscriptions, 300)
})

onMounted(() => {
  fetchSubscriptions()
  fetchStats()
})
</script>
