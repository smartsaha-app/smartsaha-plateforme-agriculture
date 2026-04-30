<template>
  <div class="p-6 space-y-8 max-w-[1400px] mx-auto">
    <!-- ===== HEADER ===== -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-6">
      <div>
        <h1 class="text-3xl font-extrabold text-[#112830]">Adhésions & Invitations</h1>
        <p class="text-gray-500 font-medium">Gérez les demandes et les invitations de vos groupes.</p>
      </div>
      <div class="flex gap-2">
        <span class="px-4 py-2 bg-amber-50 text-amber-600 rounded-2xl font-black text-xs uppercase tracking-widest border border-amber-100 italic">
          {{ activeTab === 'requests' ? pendingRequests.length : pendingInvitations.length }}
          {{ activeTab === 'requests' ? 'demande(s)' : 'invitation(s)' }} en attente
        </span>
      </div>
    </div>

    <!-- ===== ONGLETS ===== -->
    <div class="flex gap-2 bg-gray-100 p-1.5 rounded-2xl w-fit">
      <button
        @click="activeTab = 'requests'"
        :class="[
          'px-6 py-2.5 rounded-xl font-bold text-sm transition-all',
          activeTab === 'requests'
            ? 'bg-white text-[#112830] shadow-sm'
            : 'text-gray-400 hover:text-gray-600'
        ]"
      >
        <i class="bx bx-user-voice mr-2"></i>
        Demandes reçues
        <span v-if="pendingRequests.length > 0" class="ml-2 px-2 py-0.5 bg-amber-100 text-amber-600 rounded-full text-xs font-black">
          {{ pendingRequests.length }}
        </span>
      </button>
      <button
        @click="activeTab = 'invitations'"
        :class="[
          'px-6 py-2.5 rounded-xl font-bold text-sm transition-all',
          activeTab === 'invitations'
            ? 'bg-white text-[#112830] shadow-sm'
            : 'text-gray-400 hover:text-gray-600'
        ]"
      >
        <i class="bx bx-send mr-2"></i>
        Invitations envoyées
        <span v-if="pendingInvitations.length > 0" class="ml-2 px-2 py-0.5 bg-blue-100 text-blue-600 rounded-full text-xs font-black">
          {{ pendingInvitations.length }}
        </span>
      </button>
    </div>

    <!-- ===== LOADING ===== -->
    <div v-if="isLoading" class="flex flex-col items-center justify-center py-20 space-y-4">
      <div class="w-12 h-12 border-4 border-[#10b481] border-t-transparent rounded-full animate-spin"></div>
      <p class="text-gray-400 font-bold animate-pulse">Récupération des données...</p>
    </div>

    <!-- ===== ONGLET : DEMANDES REÇUES ===== -->
    <div v-else-if="activeTab === 'requests'">
      <div v-if="pendingRequests.length === 0" class="bg-white p-20 rounded-[3rem] text-center border border-dashed border-gray-200">
        <div class="w-20 h-20 bg-gray-50 rounded-full flex items-center justify-center mx-auto mb-6 text-gray-200 text-4xl">
          <i class="bx bx-user-voice"></i>
        </div>
        <h3 class="text-xl font-bold text-gray-400">Aucune demande d'adhésion pour le moment</h3>
        <p class="text-gray-300 mt-2">Les demandes envoyées par les agriculteurs apparaîtront ici.</p>
      </div>

      <div v-else class="grid grid-cols-1 gap-4">
        <div v-for="req in pendingRequests" :key="req.uuid"
             class="bg-white p-6 rounded-[2.5rem] border border-gray-100 shadow-sm hover:shadow-xl transition-all flex flex-col md:flex-row items-center justify-between gap-6 group">
          <div class="flex items-center gap-6">
            <div class="w-16 h-16 rounded-2xl bg-[#112830] text-white flex items-center justify-center text-2xl font-black group-hover:scale-110 transition-transform shadow-lg">
              {{ (req.user.email || req.user.username || 'A')[0].toUpperCase() }}
            </div>
            <div>
              <h3 class="text-xl font-bold text-[#112830]">{{ req.user.first_name }} {{ req.user.last_name }}</h3>
              <p class="text-sm text-gray-400 font-medium">Demande à rejoindre : <span class="text-[#10b481] font-bold">{{ req.group.name }}</span></p>
              <p class="text-[10px] text-gray-300 uppercase font-black tracking-tighter mt-1">{{ req.user.email }}</p>
            </div>
          </div>
          <div class="flex items-center gap-3">
            <button @click="openApproveModal(req)" class="px-6 py-3 bg-[#10b481] text-white rounded-2xl font-bold hover:bg-[#112830] transition-all flex items-center gap-2 shadow-lg shadow-[#10b481]/10">
              <i class="bx bx-check"></i> Accepter
            </button>
            <button @click="handleReject(req)" class="px-6 py-3 bg-white border border-rose-100 text-rose-500 rounded-2xl font-bold hover:bg-rose-50 transition-all flex items-center gap-2">
              <i class="bx bx-x"></i> Refuser
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- ===== ONGLET : INVITATIONS ENVOYÉES ===== -->
    <div v-else-if="activeTab === 'invitations'">
      <div v-if="pendingInvitations.length === 0" class="bg-white p-20 rounded-[3rem] text-center border border-dashed border-gray-200">
        <div class="w-20 h-20 bg-gray-50 rounded-full flex items-center justify-center mx-auto mb-6 text-gray-200 text-4xl">
          <i class="bx bx-send"></i>
        </div>
        <h3 class="text-xl font-bold text-gray-400">Aucune invitation en attente</h3>
        <p class="text-gray-300 mt-2">Les invitations envoyées aux agriculteurs apparaîtront ici.</p>
      </div>

      <div v-else class="grid grid-cols-1 gap-4">
        <div v-for="inv in pendingInvitations" :key="inv.uuid"
             class="bg-white p-6 rounded-[2.5rem] border border-gray-100 shadow-sm hover:shadow-xl transition-all flex flex-col md:flex-row items-center justify-between gap-6 group">
          <div class="flex items-center gap-6">
            <div class="w-16 h-16 rounded-2xl bg-blue-50 text-blue-400 flex items-center justify-center text-2xl font-black group-hover:scale-110 transition-transform shadow-lg">
              {{ (inv.user.email || inv.user.username || 'A')[0].toUpperCase() }}
            </div>
            <div>
              <h3 class="text-xl font-bold text-[#112830]">{{ inv.user.first_name }} {{ inv.user.last_name }}</h3>
              <p class="text-sm text-gray-400 font-medium">Invité à rejoindre : <span class="text-blue-500 font-bold">{{ inv.group.name }}</span></p>
              <p class="text-[10px] text-gray-300 uppercase font-black tracking-tighter mt-1">{{ inv.user.email }}</p>
            </div>
          </div>
          <!-- Badge statut + bouton annuler -->
          <div class="flex items-center gap-3">
            <span class="px-4 py-2 bg-amber-50 text-amber-500 rounded-2xl text-xs font-black uppercase tracking-widest border border-amber-100">
              En attente de réponse
            </span>
            <button @click="openCancelModal(inv)" class="px-6 py-3 bg-white border border-rose-100 text-rose-500 rounded-2xl font-bold hover:bg-rose-50 transition-all flex items-center gap-2">
              <i class="bx bx-x-circle"></i> Annuler
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- ===== MODALE : APPROUVER DEMANDE ===== -->
    <div v-if="selectedRequest" class="fixed inset-0 z-[100] flex items-center justify-center p-6 backdrop-blur-md bg-black/20">
      <div class="bg-white w-full max-w-lg rounded-[2.5rem] p-10 shadow-2xl space-y-6 relative border border-white/20">
        <button @click="selectedRequest = null" class="absolute top-6 right-6 w-10 h-10 rounded-full hover:bg-gray-100 flex items-center justify-center transition-colors">
          <i class="bx bx-x text-2xl"></i>
        </button>
        <div class="text-center space-y-2">
          <div class="w-20 h-20 rounded-3xl bg-emerald-50 text-[#10b481] flex items-center justify-center mx-auto mb-4">
            <i class="bx bx-check-shield text-4xl"></i>
          </div>
          <h2 class="text-2xl font-black text-[#112830]">Valider l'adhésion</h2>
          <p class="text-sm text-gray-400">Quel rôle souhaitez-vous attribuer à <b>{{ selectedRequest.user.first_name }}</b> dans le groupe {{ selectedRequest.group.name }} ?</p>
        </div>
        <div class="space-y-4 pt-4">
          <label class="text-xs font-black text-gray-400 uppercase tracking-widest">Rôle au sein du groupe</label>
          <select v-model="selectedRoleUuid" class="w-full p-4 bg-gray-50 rounded-2xl border-none outline-none focus:ring-2 focus:ring-[#10b481]/30 font-bold text-gray-700 cursor-pointer">
            <option v-for="r in roles" :key="r.uuid" :value="r.uuid">{{ r.name }}</option>
          </select>
        </div>
        <div class="flex gap-3 pt-6">
          <button @click="selectedRequest = null" class="flex-1 py-4 text-gray-400 font-bold hover:text-gray-600">Annuler</button>
          <button @click="confirmApprove" :disabled="!selectedRoleUuid" class="flex-2 py-4 px-10 bg-[#10b481] text-white rounded-2xl font-bold hover:bg-[#0da374] shadow-lg shadow-[#10b481]/20 disabled:opacity-50 transition-all">
            Valider
          </button>
        </div>
      </div>
    </div>

    <!-- ===== MODALE : CONFIRMER ANNULATION INVITATION ===== -->
    <div v-if="selectedInvitation" class="fixed inset-0 z-[100] flex items-center justify-center p-6 backdrop-blur-md bg-black/20">
      <div class="bg-white w-full max-w-md rounded-[2.5rem] p-10 shadow-2xl space-y-6 relative border border-white/20">
        <button @click="selectedInvitation = null" class="absolute top-6 right-6 w-10 h-10 rounded-full hover:bg-gray-100 flex items-center justify-center transition-colors">
          <i class="bx bx-x text-2xl"></i>
        </button>
        <div class="text-center space-y-2">
          <div class="w-20 h-20 rounded-3xl bg-rose-50 text-rose-400 flex items-center justify-center mx-auto mb-4">
            <i class="bx bx-x-circle text-4xl"></i>
          </div>
          <h2 class="text-2xl font-black text-[#112830]">Annuler l'invitation ?</h2>
          <p class="text-sm text-gray-400">
            Vous êtes sur le point d'annuler l'invitation envoyée à
            <b>{{ selectedInvitation.user.first_name }} {{ selectedInvitation.user.last_name }}</b>
            pour rejoindre <b>{{ selectedInvitation.group.name }}</b>.
            Cette action est irréversible.
          </p>
        </div>
        <div class="flex gap-3 pt-4">
          <button @click="selectedInvitation = null" class="flex-1 py-4 text-gray-400 font-bold hover:text-gray-600">
            Garder
          </button>
          <button @click="confirmCancel" :disabled="isCancelling" class="flex-2 py-4 px-10 bg-rose-500 text-white rounded-2xl font-bold hover:bg-rose-600 shadow-lg shadow-rose-500/20 disabled:opacity-50 transition-all flex items-center gap-2 justify-center">
            <div v-if="isCancelling" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            <i v-else class="bx bx-trash"></i>
            Annuler l'invitation
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useApi } from '~/composables/useApi';

definePageMeta({ layout: 'dashboard' });

const { apiFetch } = useApi();

const isLoading = ref(true);
const activeTab = ref<'requests' | 'invitations'>('requests');

// Demandes agriculteurs (initiated_by=USER)
const pendingRequests = ref<any[]>([]);
// Invitations org (initiated_by=ORGANISATION)
const pendingInvitations = ref<any[]>([]);

const roles = ref<any[]>([]);
const selectedRequest = ref<any>(null);
const selectedRoleUuid = ref('');

const selectedInvitation = ref<any>(null);
const isCancelling = ref(false);

async function fetchRoles() {
  try {
    const data: any = await apiFetch('/api/group-roles/');
    roles.value = data.results || data || [];
    const memberRole = roles.value.find(r => r.name.toUpperCase() === 'MEMBRE' || r.name.toUpperCase() === 'MEMBER');
    if (memberRole) selectedRoleUuid.value = memberRole.uuid;
    else if (roles.value.length > 0) selectedRoleUuid.value = roles.value[0].uuid;
  } catch (err) {
    console.error("Erreur roles:", err);
  }
}

async function fetchRequests() {
  isLoading.value = true;
  try {
    // Demandes agriculteurs
    const reqData: any = await apiFetch('/api/member-groups/?status=PENDING&initiated_by=USER');
    pendingRequests.value = (reqData.results || reqData || []).filter(
      (r: any) => r.user?.spaces?.agriculture === true
    );

    // Invitations envoyées par l'organisation
    const invData: any = await apiFetch('/api/member-groups/?status=PENDING&initiated_by=ORGANISATION');
    pendingInvitations.value = invData.results || invData || [];
  } catch (err) {
    console.error("Erreur fetchRequests:", err);
  } finally {
    isLoading.value = false;
  }
}

function openApproveModal(req: any) {
  selectedRequest.value = req;
}

function openCancelModal(inv: any) {
  selectedInvitation.value = inv;
}

async function confirmApprove() {
  if (!selectedRoleUuid.value) return;
  try {
    await apiFetch(`/api/member-groups/${selectedRequest.value.uuid}/approve/`, {
      method: 'POST',
      body: { role_uuid: selectedRoleUuid.value }
    });
    pendingRequests.value = pendingRequests.value.filter(r => r.uuid !== selectedRequest.value.uuid);
    selectedRequest.value = null;
  } catch (err) {
    console.error("Erreur approve:", err);
    alert("Une erreur est survenue lors de l'approbation.");
  }
}

async function confirmCancel() {
  if (!selectedInvitation.value) return;
  isCancelling.value = true;
  try {
    await apiFetch(`/api/member-groups/${selectedInvitation.value.uuid}/cancel/`, { method: 'POST' });
    pendingInvitations.value = pendingInvitations.value.filter(i => i.uuid !== selectedInvitation.value.uuid);
    selectedInvitation.value = null;
  } catch (err) {
    console.error("Erreur cancel:", err);
    alert("Une erreur est survenue lors de l'annulation.");
  } finally {
    isCancelling.value = false;
  }
}

async function handleReject(req: any) {
  try {
    await apiFetch(`/api/member-groups/${req.uuid}/reject/`, { method: 'POST' });
    pendingRequests.value = pendingRequests.value.filter(r => r.uuid !== req.uuid);
  } catch (err) {
    console.error("Erreur reject:", err);
    alert("Une erreur est survenue lors du refus.");
  }
}

onMounted(() => {
  fetchRoles();
  fetchRequests();
});
</script>