<template>
  <div class="p-6 space-y-8 max-w-[1000px] mx-auto">

    <!-- ===== HEADER ===== -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-6">
      <div>
        <h1 class="text-3xl font-extrabold text-[#112830]">Mes Invitations & Demandes</h1>
        <p class="text-gray-500 font-medium">Gérez vos invitations reçues et vos demandes d'adhésion envoyées.</p>
      </div>
      <span class="px-4 py-2 bg-amber-50 text-amber-600 rounded-2xl font-black text-xs uppercase tracking-widest border border-amber-100 italic w-fit">
        {{ activeTab === 'invitations'
          ? `${invitations.length} invitation(s) en attente`
          : `${sentRequests.length} demande(s) envoyée(s)` }}
      </span>
    </div>

    <!-- ===== ONGLETS ===== -->
    <div class="flex gap-2 bg-gray-100 p-1.5 rounded-2xl w-fit">
      <button
        @click="activeTab = 'invitations'"
        :class="[
          'px-6 py-2.5 rounded-xl font-bold text-sm transition-all',
          activeTab === 'invitations'
            ? 'bg-white text-[#112830] shadow-sm'
            : 'text-gray-400 hover:text-gray-600'
        ]"
      >
        <i class="bx bx-envelope mr-2"></i>
        Invitations reçues
        <span v-if="invitations.length > 0" class="ml-2 px-2 py-0.5 bg-amber-100 text-amber-600 rounded-full text-xs font-black">
          {{ invitations.length }}
        </span>
      </button>
      <button
        @click="activeTab = 'requests'"
        :class="[
          'px-6 py-2.5 rounded-xl font-bold text-sm transition-all',
          activeTab === 'requests'
            ? 'bg-white text-[#112830] shadow-sm'
            : 'text-gray-400 hover:text-gray-600'
        ]"
      >
        <i class="bx bx-send mr-2"></i>
        Mes demandes envoyées
        <span v-if="sentRequests.length > 0" class="ml-2 px-2 py-0.5 bg-blue-100 text-blue-600 rounded-full text-xs font-black">
          {{ sentRequests.length }}
        </span>
      </button>
    </div>

    <!-- ===== LOADING ===== -->
    <div v-if="isLoading" class="space-y-4">
      <div v-for="i in 3" :key="i" class="h-24 bg-gray-50 rounded-3xl animate-pulse border border-gray-100"></div>
    </div>

    <!-- ===== ONGLET : INVITATIONS REÇUES ===== -->
    <div v-else-if="activeTab === 'invitations'">
      <div v-if="invitations.length === 0" class="py-20 text-center space-y-6">
        <div class="w-24 h-24 bg-gray-50 rounded-full flex items-center justify-center mx-auto text-gray-200">
          <i class="bx bx-envelope-open text-5xl"></i>
        </div>
        <div>
          <h2 class="text-xl font-black text-[#112830] mb-1">Aucune invitation en attente</h2>
          <p class="text-gray-400 font-medium italic">Rejoignez des organisations pour collaborer davantage.</p>
        </div>
        <button @click="router.push('/management/organisations')" class="px-6 py-3 bg-white text-[#112830] font-bold rounded-2xl border border-gray-100 hover:bg-gray-50 transition-all">
          Découvrir des groupes
        </button>
      </div>

      <div v-else class="space-y-4">
        <div v-for="inv in invitations" :key="inv.uuid"
             class="bg-white p-8 rounded-[2.5rem] border border-gray-100 shadow-sm hover:shadow-xl transition-all duration-500 flex flex-col md:flex-row md:items-center justify-between gap-6 group">
          <div class="flex items-center gap-6">
            <div class="w-16 h-16 rounded-2xl bg-[#112830] text-white flex items-center justify-center text-2xl font-black group-hover:bg-[#10b481] transition-all duration-300">
              {{ (inv.group.organisation?.name || 'O')[0].toUpperCase() }}
            </div>
            <div>
              <h3 class="text-xl font-black text-[#112830] mb-1">{{ inv.group.organisation?.name || 'Organisation' }}</h3>
              <p class="text-gray-400 font-bold flex items-center gap-2 text-sm flex-wrap">
                <span class="px-2 py-0.5 bg-gray-50 rounded-lg text-[#112830] text-[10px] uppercase font-black tracking-tighter border border-gray-100">
                  {{ inv.group.name }}
                </span>
                • Rôle proposé : <span class="text-[#10b481]">{{ inv.role.name }}</span>
              </p>
            </div>
          </div>
          <div class="flex items-center gap-3">
            <button @click="respond(inv, 'accept')" class="px-8 py-3 bg-[#112830] text-white rounded-2xl font-bold hover:bg-[#10b481] transition-all duration-300 shadow-lg shadow-[#112830]/10 flex items-center gap-2">
              <i class="bx bx-check text-xl"></i> Accepter
            </button>
            <button @click="respond(inv, 'reject')" class="px-8 py-3 bg-white text-gray-400 rounded-2xl font-bold border border-gray-100 hover:bg-rose-50 hover:text-rose-500 hover:border-rose-100 transition-all flex items-center gap-2">
              <i class="bx bx-x text-xl"></i> Refuser
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- ===== ONGLET : DEMANDES ENVOYÉES ===== -->
    <div v-else-if="activeTab === 'requests'">
      <div v-if="sentRequests.length === 0" class="py-20 text-center space-y-6">
        <div class="w-24 h-24 bg-gray-50 rounded-full flex items-center justify-center mx-auto text-gray-200">
          <i class="bx bx-send text-5xl"></i>
        </div>
        <div>
          <h2 class="text-xl font-black text-[#112830] mb-1">Aucune demande en attente</h2>
          <p class="text-gray-400 font-medium italic">Vos demandes d'adhésion envoyées apparaîtront ici.</p>
        </div>
        <button @click="router.push('/management/organisations')" class="px-6 py-3 bg-white text-[#112830] font-bold rounded-2xl border border-gray-100 hover:bg-gray-50 transition-all">
          Découvrir des groupes
        </button>
      </div>

      <div v-else class="space-y-4">
        <div v-for="req in sentRequests" :key="req.uuid"
             class="bg-white p-8 rounded-[2.5rem] border border-gray-100 shadow-sm hover:shadow-xl transition-all duration-500 flex flex-col md:flex-row md:items-center justify-between gap-6 group">
          <div class="flex items-center gap-6">
            <div class="w-16 h-16 rounded-2xl bg-blue-50 text-blue-400 flex items-center justify-center text-2xl font-black group-hover:scale-110 transition-transform shadow-lg">
              {{ (req.group.organisation?.name || 'O')[0].toUpperCase() }}
            </div>
            <div>
              <h3 class="text-xl font-black text-[#112830] mb-1">{{ req.group.organisation?.name || 'Organisation' }}</h3>
              <p class="text-gray-400 font-bold flex items-center gap-2 text-sm flex-wrap">
                <span class="px-2 py-0.5 bg-gray-50 rounded-lg text-[#112830] text-[10px] uppercase font-black tracking-tighter border border-gray-100">
                  {{ req.group.name }}
                </span>
                • En attente de validation
              </p>
            </div>
          </div>
          <div class="flex items-center gap-3">
            <span class="px-4 py-2 bg-amber-50 text-amber-500 rounded-2xl text-xs font-black uppercase tracking-widest border border-amber-100">
              En attente
            </span>
            <button @click="openCancelModal(req)" class="px-6 py-3 bg-white border border-rose-100 text-rose-500 rounded-2xl font-bold hover:bg-rose-50 transition-all flex items-center gap-2">
              <i class="bx bx-x-circle"></i> Annuler
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- ===== MODALE : CONFIRMER ANNULATION ===== -->
    <div v-if="selectedRequest" class="fixed inset-0 z-[100] flex items-center justify-center p-6 backdrop-blur-md bg-black/20">
      <div class="bg-white w-full max-w-md rounded-[2.5rem] p-10 shadow-2xl space-y-6 relative border border-white/20">
        <button @click="selectedRequest = null" class="absolute top-6 right-6 w-10 h-10 rounded-full hover:bg-gray-100 flex items-center justify-center transition-colors">
          <i class="bx bx-x text-2xl"></i>
        </button>
        <div class="text-center space-y-2">
          <div class="w-20 h-20 rounded-3xl bg-rose-50 text-rose-400 flex items-center justify-center mx-auto mb-4">
            <i class="bx bx-x-circle text-4xl"></i>
          </div>
          <h2 class="text-2xl font-black text-[#112830]">Annuler la demande ?</h2>
          <p class="text-sm text-gray-400">
            Vous êtes sur le point d'annuler votre demande pour rejoindre
            <b>{{ selectedRequest.group.name }}</b>
            de l'organisation <b>{{ selectedRequest.group.organisation?.name }}</b>.
            Cette action est irréversible.
          </p>
        </div>
        <div class="flex gap-3 pt-4">
          <button @click="selectedRequest = null" class="flex-1 py-4 text-gray-400 font-bold hover:text-gray-600">
            Garder
          </button>
          <button @click="confirmCancel" :disabled="isCancelling" class="flex-2 py-4 px-10 bg-rose-500 text-white rounded-2xl font-bold hover:bg-rose-600 shadow-lg shadow-rose-500/20 disabled:opacity-50 transition-all flex items-center gap-2 justify-center">
            <div v-if="isCancelling" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            <i v-else class="bx bx-trash"></i>
            Annuler la demande
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useApi } from '~/composables/useApi';
import { useAuthStore } from '~/stores/auth';

definePageMeta({ layout: 'dashboard' });

const router    = useRouter();
const { apiFetch } = useApi();
const authStore = useAuthStore();

const isLoading   = ref(true);
const activeTab   = ref<'invitations' | 'requests'>('invitations');

// Invitations reçues (initiated_by=ORGANISATION, destinataire = moi)
const invitations  = ref<any[]>([]);
// Demandes envoyées (initiated_by=USER, émetteur = moi)
const sentRequests = ref<any[]>([]);

const selectedRequest = ref<any>(null);
const isCancelling    = ref(false);

async function fetchAll() {
  isLoading.value = true;
  const userUuid = authStore.uuid;
  if (!userUuid) return;

  try {
    const data: any = await apiFetch(`/api/member-groups/?user=${userUuid}&status=PENDING`);
    const all = data.results || data || [];

    // Invitations : l'organisation a initié → je dois répondre
    invitations.value  = all.filter((r: any) => r.initiated_by === 'ORGANISATION');

    // Demandes : j'ai initié → en attente de validation
    sentRequests.value = all.filter((r: any) => r.initiated_by === 'USER');
  } catch (err) {
    console.error("Erreur fetchAll:", err);
  } finally {
    isLoading.value = false;
  }
}

async function respond(inv: any, action: 'accept' | 'reject') {
  try {
    await apiFetch(`/api/member-groups/${inv.uuid}/${action}/`, { method: 'POST' });
    invitations.value = invitations.value.filter(i => i.uuid !== inv.uuid);
    if (action === 'accept') router.push(`/group/${inv.group.uuid}`);
  } catch (err) {
    console.error(`Erreur ${action}:`, err);
    alert("Une erreur est survenue lors de la réponse.");
  }
}

function openCancelModal(req: any) {
  selectedRequest.value = req;
}

async function confirmCancel() {
  if (!selectedRequest.value) return;
  isCancelling.value = true;
  try {
    // L'agriculteur annule sa propre demande → endpoint reject (suppression)
    await apiFetch(`/api/member-groups/${selectedRequest.value.uuid}/reject/`, { method: 'POST' });
    sentRequests.value = sentRequests.value.filter(r => r.uuid !== selectedRequest.value.uuid);
    selectedRequest.value = null;
  } catch (err) {
    console.error("Erreur annulation:", err);
    alert("Une erreur est survenue lors de l'annulation.");
  } finally {
    isCancelling.value = false;
  }
}

onMounted(() => {
  fetchAll();
});
</script>