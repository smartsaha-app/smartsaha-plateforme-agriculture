<template>
  <div class="p-6 space-y-8 max-w-[1400px] mx-auto">

    <!-- ===== HEADER ===== -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-6">
      <div>
        <h1 class="text-3xl font-extrabold text-[#112830]">Recrutement</h1>
        <p class="text-gray-500 font-medium">Découvrez des profils d'agriculteurs pour renforcer vos groupes de production.</p>
      </div>
      <button @click="router.back()" class="px-6 py-3 bg-white text-gray-500 rounded-2xl font-bold border border-gray-100 hover:bg-gray-50 transition-all flex items-center gap-2 w-fit">
        <i class="bx bx-left-arrow-alt text-xl"></i> Retour
      </button>
    </div>

    <!-- ===== LOADING ===== -->
    <div v-if="isLoading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="i in 6" :key="i" class="h-80 bg-gray-50 rounded-[2.5rem] animate-pulse"></div>
    </div>

    <!-- ===== FARMERS LIST ===== -->
    <div v-else-if="farmers.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      <div v-for="farmer in farmers" :key="farmer.uuid"
           class="group bg-white rounded-[3rem] border border-gray-100 shadow-sm hover:shadow-2xl transition-all duration-500 overflow-hidden flex flex-col relative">

        <!-- Header carte -->
        <div class="h-24 bg-[#f8f9fa] relative border-b border-gray-50 flex items-end px-8">
          <div class="absolute inset-0 opacity-5 flex items-center justify-center pointer-events-none">
            <i class="bx bx-leaf text-[80px]"></i>
          </div>
          <div class="w-20 h-20 rounded-3xl bg-[#112830] text-white flex items-center justify-center text-3xl font-black shadow-xl translate-y-6 relative z-10 border-4 border-white group-hover:bg-[#10b481] transition-colors">
            {{ (farmer.email || farmer.username || 'A')[0].toUpperCase() }}
          </div>
        </div>

        <div class="p-8 pt-10 space-y-4 flex-1 flex flex-col">

          <!-- Nom -->
          <div>
            <h3 class="text-2xl font-black text-[#112830] group-hover:text-[#10b481] transition-colors">
              {{ farmer.first_name }} {{ farmer.last_name }}
            </h3>
            <p class="text-sm text-gray-400 font-bold">{{ farmer.username }}</p>
          </div>

          <!-- Cultures -->
          <div class="flex flex-wrap gap-2 min-h-[28px]">
            <span v-for="crop in farmer.crops" :key="crop"
              class="px-3 py-1 bg-gray-50 text-gray-500 rounded-lg text-[10px] font-black uppercase tracking-tighter">
              {{ crop }}
            </span>
            <span v-if="!farmer.crops || farmer.crops.length === 0"
              class="text-[11px] text-gray-300 italic font-medium">Aucune culture renseignée</span>
          </div>

          <!-- ✅ Groupes déjà rejoints (affichage direct sur la carte) -->
          <div v-if="farmer.memberships.length > 0" class="space-y-1">
            <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest">Déjà dans vos groupes</p>
            <div class="flex flex-wrap gap-1.5">
              <span v-for="m in farmer.memberships" :key="m.groupId"
                class="px-2.5 py-1 rounded-xl text-[10px] font-black border flex items-center gap-1"
                :class="m.status === 'ACTIVE'
                  ? 'bg-blue-50 text-blue-600 border-blue-100'
                  : 'bg-amber-50 text-amber-600 border-amber-100'">
                <i :class="m.status === 'ACTIVE' ? 'bx bx-check-circle' : 'bx bx-time'"></i>
                {{ m.groupName }}
              </span>
            </div>
          </div>

          <!-- Bouton Inviter -->
          <div class="mt-auto pt-2">
            <button @click="openInviteModal(farmer)"
              :disabled="eligibleGroupsFor(farmer).length === 0"
              class="w-full py-4 rounded-2xl font-black text-xs uppercase tracking-widest transition-all flex items-center justify-center gap-2"
              :class="eligibleGroupsFor(farmer).length === 0
                ? 'bg-gray-100 text-gray-400 cursor-not-allowed border border-gray-200'
                : 'bg-[#112830] text-white hover:bg-[#10b481] shadow-xl shadow-[#112830]/10'">
              <i class="bx bx-plus-circle text-lg"></i>
              {{ eligibleGroupsFor(farmer).length === 0 ? 'Membre de tous vos groupes' : 'Inviter dans un groupe' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- ===== EMPTY STATE ===== -->
    <div v-else class="py-20 text-center space-y-4">
      <div class="w-24 h-24 bg-gray-50 rounded-full flex items-center justify-center mx-auto text-gray-200">
        <i class="bx bx-user-x text-5xl"></i>
      </div>
      <p class="text-gray-400 font-medium italic">Aucun agriculteur trouvé.</p>
    </div>


    <!-- ═══════════════════════════════════════════
         MODALE INVITATION
         ═══════════════════════════════════════════ -->
    <div v-if="selectedFarmer" class="fixed inset-0 z-[100] flex items-center justify-center p-6 backdrop-blur-md bg-black/20" @click.self="selectedFarmer = null">
      <div class="bg-white w-full max-w-lg rounded-[2.5rem] p-10 shadow-2xl space-y-6 relative border border-white/20">
        <button @click="selectedFarmer = null" class="absolute top-6 right-6 w-10 h-10 rounded-full hover:bg-gray-100 flex items-center justify-center transition-colors">
          <i class="bx bx-x text-2xl"></i>
        </button>

        <div class="text-center space-y-2">
          <div class="w-20 h-20 rounded-3xl bg-emerald-50 text-[#10b481] flex items-center justify-center mx-auto mb-4">
            <i class="bx bx-send text-4xl"></i>
          </div>
          <h2 class="text-2xl font-black text-[#112830]">Envoyer une invitation</h2>
          <p class="text-sm text-gray-400">
            Vous invitez <b>{{ selectedFarmer.first_name }} {{ selectedFarmer.last_name }}</b> à rejoindre un de vos groupes.
          </p>
        </div>

        <!-- Groupes déjà liés (rappel dans la modale) -->
        <div v-if="selectedFarmer.memberships.length > 0" class="bg-gray-50 rounded-2xl px-5 py-4 space-y-2">
          <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest">Déjà présent dans</p>
          <div class="flex flex-wrap gap-1.5">
            <span v-for="m in selectedFarmer.memberships" :key="m.groupId"
              class="px-2.5 py-1 rounded-xl text-[10px] font-black border flex items-center gap-1"
              :class="m.status === 'ACTIVE'
                ? 'bg-blue-50 text-blue-600 border-blue-100'
                : 'bg-amber-50 text-amber-600 border-amber-100'">
              <i :class="m.status === 'ACTIVE' ? 'bx bx-check-circle' : 'bx bx-time'"></i>
              {{ m.groupName }}
            </span>
          </div>
        </div>

        <div class="space-y-4">
          <div class="space-y-1">
            <label class="text-xs font-black text-gray-400 uppercase tracking-widest">Choisir le groupe</label>
            <select v-model="inviteData.group_uuid"
              class="w-full p-4 bg-gray-50 rounded-2xl border-none outline-none focus:ring-2 focus:ring-[#10b481]/30 font-medium cursor-pointer">
              <option value="" disabled>Sélectionner un groupe...</option>
              <!-- ✅ Uniquement les groupes où il n'est pas encore présent -->
              <option v-for="group in eligibleGroupsFor(selectedFarmer)" :key="group.uuid" :value="group.uuid">
                {{ group.name }}
              </option>
            </select>
          </div>
          <div class="space-y-1">
            <label class="text-xs font-black text-gray-400 uppercase tracking-widest">Rôle proposé</label>
            <select v-model="inviteData.role_uuid"
              class="w-full p-4 bg-gray-50 rounded-2xl border-none outline-none focus:ring-2 focus:ring-[#10b481]/30 font-medium cursor-pointer">
              <option v-for="role in roles" :key="role.uuid" :value="role.uuid">{{ role.name }}</option>
            </select>
          </div>
        </div>

        <div class="flex gap-3 pt-2">
          <button @click="selectedFarmer = null" class="flex-1 py-4 text-gray-400 font-bold hover:text-gray-600 transition">
            Annuler
          </button>
          <button @click="sendInvitation"
            :disabled="!inviteData.group_uuid || !inviteData.role_uuid || isSending"
            class="flex-2 py-4 px-10 bg-[#112830] text-white rounded-2xl font-bold disabled:opacity-50 hover:bg-[#10b481] transition-all duration-300">
            {{ isSending ? 'Envoi...' : "Envoyer l'invitation" }}
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

definePageMeta({ layout: 'dashboard' });

const router       = useRouter();
const { apiFetch } = useApi();

// ─── État global ──────────────────────────────────────────────────────────────
const isLoading = ref(true);
const isSending = ref(false);
const farmers   = ref<any[]>([]);
const myGroups  = ref<any[]>([]);
const roles     = ref<any[]>([]);

// ─── Modale invitation ────────────────────────────────────────────────────────
const selectedFarmer = ref<any>(null);
const inviteData     = ref({ group_uuid: '', role_uuid: '' });

// ─── Groupes éligibles pour un agriculteur donné ──────────────────────────────
// ✅ Exclut tous les groupes où il est déjà présent (ACTIVE ou PENDING)
function eligibleGroupsFor(farmer: any) {
  if (!farmer) return myGroups.value;
  const occupiedGroupIds = new Set(farmer.memberships.map((m: any) => m.groupId));
  return myGroups.value.filter(g => !occupiedGroupIds.has(g.uuid));
}

// ─── Chargement ───────────────────────────────────────────────────────────────
async function fetchMyGroups() {
  try {
    const data: any = await apiFetch('/api/groups/');
    myGroups.value = data.results || data || [];
  } catch (err) {
    console.error("Erreur fetchMyGroups:", err);
  }
}

async function fetchRoles() {
  try {
    const data: any = await apiFetch('/api/group-roles/');
    roles.value = data.results || data || [];
    const memberRole = roles.value.find(r =>
      r.name.toUpperCase() === 'MEMBRE' || r.name.toUpperCase() === 'MEMBER'
    );
    inviteData.value.role_uuid = memberRole?.uuid ?? roles.value[0]?.uuid ?? '';
  } catch (err) {
    console.error("Erreur fetchRoles:", err);
  }
}

async function fetchFarmers() {
  isLoading.value = true;
  try {
    const data: any = await apiFetch('/api/discovery-farmers/');
    const allFarmers: any[] = data.results || data || [];

    // ✅ Récupérer toutes les adhésions de tous mes groupes en une fois
    const memberships = await Promise.all(
      myGroups.value.map((g: any) => apiFetch(`/api/member-groups/?group=${g.uuid}`))
    );
    const allMemberships = memberships.flatMap((m: any) => m.results || m || []);

    // ✅ Pour chaque agriculteur, lister TOUTES ses adhésions dans mes groupes
    farmers.value = allFarmers.map((f: any) => {
      const farmerMemberships = allMemberships
        .filter((m: any) => m.user?.uuid === f.uuid)
        .map((m: any) => ({
          groupId:   m.group?.uuid  ?? '',
          groupName: m.group?.name  ?? '',
          status:    m.status,        // 'ACTIVE' ou 'PENDING'
        }));

      return {
        ...f,
        memberships: farmerMemberships, // ✅ tableau de toutes ses adhésions
      };
    });
  } catch (err) {
    console.error("Erreur fetchFarmers:", err);
  } finally {
    isLoading.value = false;
  }
}

// ─── Modale invitation ────────────────────────────────────────────────────────
function openInviteModal(farmer: any) {
  if (eligibleGroupsFor(farmer).length === 0) return;
  selectedFarmer.value        = farmer;
  inviteData.value.group_uuid = '';
}

async function sendInvitation() {
  if (!inviteData.value.group_uuid || !inviteData.value.role_uuid) return;
  isSending.value = true;
  try {
    await apiFetch('/api/member-groups/', {
      method: 'POST',
      body: {
        user_id:  selectedFarmer.value.uuid,
        group_id: inviteData.value.group_uuid,
        role_id:  inviteData.value.role_uuid,
      }
    });

    // ✅ Mise à jour locale : ajouter la nouvelle adhésion PENDING
    const group = myGroups.value.find(g => g.uuid === inviteData.value.group_uuid);
    const f = farmers.value.find(f => f.uuid === selectedFarmer.value.uuid);
    if (f && group) {
      f.memberships.push({
        groupId:   group.uuid,
        groupName: group.name,
        status:    'PENDING',
      });
    }
    selectedFarmer.value = null;
  } catch (err) {
    console.error("Erreur sendInvitation:", err);
    alert("Erreur lors de l'envoi de l'invitation.");
  } finally {
    isSending.value = false;
  }
}

// ─── Init ─────────────────────────────────────────────────────────────────────
onMounted(async () => {
  await Promise.all([fetchMyGroups(), fetchRoles()]);
  await fetchFarmers();
});
</script>