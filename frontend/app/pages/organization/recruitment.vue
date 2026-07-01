<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8 space-y-6">

    <!-- ===== HEADER ===== -->
    <PageHeader :title="t('organization.recruitmentTitle')">
      <template #subtitle>
        <i class="bx bx-search-alt"></i>
        {{ t('organization.recruitmentDesc') }}
      </template>
      <template #breadcrumb>
        <NuxtLink to="/organization/dashboard" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
          <span>{{ t('dashboard.home') }}</span>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">{{ t('organization.recruitmentTitle') }}</span>
      </template>
    </PageHeader>

    <!-- Barre de recherche agriculteurs -->
    <div class="flex items-center gap-2 bg-white rounded-2xl border border-gray-100 shadow-sm p-3">
      <div class="flex-1 relative">
        <i class="bx bx-search absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-base pointer-events-none"></i>
        <input v-model="searchFarmer" type="text" :placeholder="t('organization.searchFarmer')"
          class="w-full pl-9 pr-4 py-2.5 bg-gray-50 border border-gray-100 rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#10b481]/20 font-medium text-[#112830]" />
      </div>
      <span class="text-xs font-bold text-gray-400 whitespace-nowrap">
        {{ filteredFarmers.length }} {{ filteredFarmers.length !== 1 ? t('organization.profilePlural') : t('organization.profileSingular') }}
      </span>
    </div>

    <!-- ===== LOADING ===== -->
    <div v-if="isLoading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="i in 6" :key="i" class="h-80 bg-gray-50 rounded-2xl animate-pulse"></div>
    </div>

    <!-- ===== FARMERS LIST ===== -->
    <div v-else-if="filteredFarmers.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="farmer in filteredFarmers" :key="farmer.uuid"
           class="group bg-white rounded-2xl border border-gray-100 shadow-sm hover:shadow-2xl transition-all duration-500 overflow-hidden flex flex-col relative">

        <!-- Header carte -->
        <div class="h-24 bg-[#f8f9fa] relative border-b border-gray-50 flex items-end px-8">
          <div class="absolute inset-0 opacity-5 flex items-center justify-center pointer-events-none">
            <i class="bx bx-leaf text-[80px]"></i>
          </div>
          <div class="w-20 h-20 rounded-xl bg-[#112830] text-white flex items-center justify-center text-3xl font-black shadow-xl translate-y-6 relative z-10 border-4 border-white group-hover:bg-[#10b481] transition-colors">
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
              class="text-[11px] text-gray-300 italic font-medium">{{ t('organization.noCrops') }}</span>
          </div>

          <!-- ✅ Groupes déjà rejoints (affichage direct sur la carte) -->
          <div v-if="farmer.memberships.length > 0" class="space-y-1">
            <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest">{{ t('organization.alreadyInGroups') }}</p>
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
              {{ eligibleGroupsFor(farmer).length === 0 ? t('organization.allGroupsMember') : t('organization.inviteBtn') }}
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
      <p class="text-gray-400 font-medium italic">{{ t('organization.noFarmers') }}</p>
    </div>


    <!-- ═══════════════════════════════════════════
         MODALE INVITATION
         ═══════════════════════════════════════════ -->
    <div v-if="selectedFarmer" class="fixed inset-0 z-[100] flex items-center justify-center p-6 backdrop-blur-md bg-black/20" @click.self="selectedFarmer = null">
      <div class="bg-white w-full max-w-lg rounded-2xl p-10 shadow-2xl space-y-6 relative border border-white/20">
        <button @click="selectedFarmer = null" class="absolute top-6 right-6 w-10 h-10 rounded-full hover:bg-gray-100 flex items-center justify-center transition-colors">
          <i class="bx bx-x text-2xl"></i>
        </button>

        <div class="text-center space-y-2">
          <div class="w-20 h-20 rounded-xl bg-emerald-50 text-[#10b481] flex items-center justify-center mx-auto mb-4">
            <i class="bx bx-send text-4xl"></i>
          </div>
          <h2 class="text-2xl font-black text-[#112830]">{{ t('organization.inviteModalTitle') }}</h2>
          <p class="text-sm text-gray-400">
            {{ t('organization.inviteModalDesc') }} <b>{{ selectedFarmer.first_name }} {{ selectedFarmer.last_name }}</b> {{ t('organization.inviteModalDesc2') }}
          </p>
        </div>

        <!-- Groupes déjà liés (rappel dans la modale) -->
        <div v-if="selectedFarmer.memberships.length > 0" class="bg-gray-50 rounded-2xl px-5 py-4 space-y-2">
          <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest">{{ t('organization.alreadyIn') }}</p>
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
            <label class="text-xs font-black text-gray-400 uppercase tracking-widest">{{ t('organization.chooseGroup') }}</label>
            <select v-model="inviteData.group_uuid"
              class="w-full p-4 bg-gray-50 rounded-2xl border-none outline-none focus:ring-2 focus:ring-[#10b481]/30 font-medium cursor-pointer">
              <option value="" disabled>{{ t('organization.selectGroup') }}</option>
              <!-- ✅ Uniquement les groupes où il n'est pas encore présent -->
              <option v-for="group in eligibleGroupsFor(selectedFarmer)" :key="group.uuid" :value="group.uuid">
                {{ group.name }}
              </option>
            </select>
          </div>
          <div class="space-y-1">
            <label class="text-xs font-black text-gray-400 uppercase tracking-widest">{{ t('organization.proposedRole') }}</label>
            <select v-model="inviteData.role_uuid"
              class="w-full p-4 bg-gray-50 rounded-2xl border-none outline-none focus:ring-2 focus:ring-[#10b481]/30 font-medium cursor-pointer">
              <option v-for="role in roles" :key="role.uuid" :value="role.uuid">{{ role.name }}</option>
            </select>
          </div>
        </div>

        <div class="flex gap-3 pt-2">
          <button @click="selectedFarmer = null" class="flex-1 py-4 text-gray-400 font-bold hover:text-gray-600 transition">
            {{ t('dashboard.cancel') }}
          </button>
          <button @click="sendInvitation"
            :disabled="!inviteData.group_uuid || !inviteData.role_uuid || isSending"
            class="flex-2 py-4 px-10 bg-[#112830] text-white rounded-2xl font-bold disabled:opacity-50 hover:bg-[#10b481] transition-all duration-300">
            {{ isSending ? t('dashboard.loading') : t('organization.inviteModalTitle') }}
          </button>
        </div>
      </div>
    </div>

    <!-- Toast -->
    <transition name="slide-up">
      <div v-if="toast.visible"
        class="fixed bottom-6 left-1/2 -translate-x-1/2 z-[100] px-5 py-3 rounded-2xl shadow-xl flex items-center gap-3 text-sm font-bold"
        :class="toast.type === 'success' ? 'bg-[#112830] text-white' : 'bg-rose-500 text-white'">
        <i :class="toast.type === 'success' ? 'bx bx-check-circle' : 'bx bx-error-circle'" class="text-lg"
          :style="toast.type === 'success' ? 'color:#10b481' : ''"></i>
        {{ toast.message }}
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useApi } from '~/composables/useApi';
import { useKycGuard } from '~/composables/useKycGuard';

definePageMeta({ layout: 'dashboard' });
const { t } = useI18n();

const { apiFetch } = useApi();
const { requireKyc } = useKycGuard();

// ─── État global ──────────────────────────────────────────────────────────────
const isLoading    = ref(true);
const isSending    = ref(false);
const farmers      = ref<any[]>([]);
const myGroups     = ref<any[]>([]);
const roles        = ref<any[]>([]);
const searchFarmer = ref('');
const toast = ref({ visible: false, message: '', type: 'success' as 'success' | 'error' });

function showToast(message: string, type: 'success' | 'error' = 'success') {
  toast.value = { visible: true, message, type };
  setTimeout(() => (toast.value.visible = false), 3000);
}

const filteredFarmers = computed(() => {
  if (!searchFarmer.value.trim()) return farmers.value;
  const q = searchFarmer.value.toLowerCase();
  return farmers.value.filter(f =>
    (f.first_name + ' ' + f.last_name).toLowerCase().includes(q) ||
    (f.email || '').toLowerCase().includes(q) ||
    (f.username || '').toLowerCase().includes(q)
  );
});

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
  if (!requireKyc()) return;
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
    showToast(t('organization.inviteSent'));
  } catch (err) {
    console.error("Erreur sendInvitation:", err);
    showToast(t('organization.inviteError'), 'error');
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

