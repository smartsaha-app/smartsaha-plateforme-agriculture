<template>
  <div class="p-6 space-y-8 max-w-[1400px] mx-auto">
    <!-- ===== HEADER ===== -->
    <div v-if="group" class="flex flex-col md:flex-row md:items-center justify-between gap-6">
      <div class="flex items-center gap-6">
        <button @click="router.back()" class="w-12 h-12 rounded-2xl bg-white border border-gray-100 shadow-sm flex items-center justify-center text-gray-400 hover:text-[#112830] transition-colors">
          <i class="bx bx-left-arrow-alt text-2xl"></i>
        </button>
        <div>
           <h1 class="text-4xl font-black text-[#112830] tracking-tight">{{ group.name }}</h1>
           <div class="flex items-center gap-3 mt-2">
              <span class="px-4 py-1.5 bg-emerald-50 text-emerald-600 rounded-full text-xs font-black uppercase tracking-widest shadow-sm">
                 {{ group.type?.name }}
              </span>
              <span class="text-sm text-gray-400 font-bold ml-2">
                 <i class="bx bx-buildings mr-1"></i> {{ group.organisation?.name }}
              </span>
           </div>
        </div>
      </div>
      <!-- <div class="flex gap-4">
         <button @click="router.push('/group')" class="px-6 py-3 bg-white border border-gray-100 text-gray-600 rounded-2xl font-bold hover:bg-gray-50 transition shadow-sm">
            Retour à la liste
         </button>
      </div> -->
    </div>

    <!-- ===== TABS ===== -->
    <div class="flex items-center gap-2 border-b border-gray-100">
      <button 
        @click="activeTab = 'members'"
        :class="['px-6 py-4 font-black uppercase tracking-widest text-[10px] transition-all relative', activeTab === 'members' ? 'text-[#112830]' : 'text-gray-400 hover:text-gray-600']"
      >
        Membres
        <div v-if="activeTab === 'members'" class="absolute bottom-0 left-0 right-0 h-1 bg-[#10b481] rounded-t-full"></div>
      </button>
      <button 
        @click="activeTab = 'supervision'"
        :class="['px-6 py-4 font-black uppercase tracking-widest text-[10px] transition-all relative', activeTab === 'supervision' ? 'text-[#112830]' : 'text-gray-400 hover:text-gray-600']"
      >
        Supervision Agricole
        <div v-if="activeTab === 'supervision'" class="absolute bottom-0 left-0 right-0 h-1 bg-[#10b481] rounded-t-full"></div>
      </button>
    </div>

    <div v-if="isLoading" class="space-y-6">
      <div v-for="i in 3" :key="i" class="h-20 bg-gray-50 rounded-3xl animate-pulse"></div>
    </div>

    <div v-else-if="group">
      <!-- ===== MEMBERS TAB ===== -->
      <div v-if="activeTab === 'members'" class="space-y-8">
        
        <!-- PENDING REQUESTS / INVITATIONS -->
        <div v-if="pendingMembers.length > 0" class="bg-amber-50/30 rounded-[2.5rem] border border-amber-100 overflow-hidden">
          <div class="p-8 border-b border-amber-100 flex items-center justify-between">
            <h3 class="text-xl font-black text-amber-800 flex items-center gap-2">
              <i class="bx bx-time-five"></i>
              Demandes et Invitations en attente ({{ pendingMembers.length }})
            </h3>
          </div>
          <div class="p-6 grid grid-cols-1 md:grid-cols-2 gap-4">
             <div v-for="m in pendingMembers" :key="m.uuid" class="bg-white p-6 rounded-3xl border border-amber-100 shadow-sm flex items-center justify-between">
                <div class="flex items-center gap-4">
                   <div class="w-12 h-12 rounded-xl bg-[#112830] text-white flex items-center justify-center font-black text-lg overflow-hidden">
                      {{ (m.user.email || m.user.username || 'A')[0].toUpperCase() }}
                   </div>
                   <div>
                      <p class="font-bold text-[#112830]">{{ m.user.first_name }} {{ m.user.last_name }}</p>
                      <p class="text-[10px] text-gray-400">@{{ m.user.username }} • Rôle: {{ m.role.name }}</p>
                   </div>
                </div>
                <div class="flex gap-2">
                   <button @click="handleMemberAction(m, 'approve')" class="w-10 h-10 rounded-xl bg-emerald-500 text-white hover:bg-emerald-600 transition-colors flex items-center justify-center tooltip" title="Approuver">
                      <i class="bx bx-check text-xl"></i>
                   </button>
                   <button @click="handleMemberAction(m, 'reject')" class="w-10 h-10 rounded-xl bg-rose-50 text-rose-500 hover:bg-rose-100 transition-colors flex items-center justify-center" title="Rejeter">
                      <i class="bx bx-x text-xl"></i>
                   </button>
                </div>
             </div>
          </div>
        </div>

        <!-- ACTIVE MEMBERS LIST -->
        <div class="bg-white rounded-[2.5rem] border border-gray-100 shadow-sm overflow-hidden">
          <div class="p-8 border-b border-gray-50 flex items-center justify-between">
            <h3 class="text-xl font-black text-[#112830]">Membres Actifs ({{ activeMembers.length }})</h3>
          </div>
          
          <div class="overflow-x-auto">
            <table class="w-full text-left">
              <thead>
                <tr class="bg-gray-50/50">
                  <th class="px-8 py-5 text-[10px] font-black text-gray-400 uppercase tracking-widest">Membre</th>
                  <th class="px-8 py-5 text-[10px] font-black text-gray-400 uppercase tracking-widest">Rôle</th>
                  <th class="px-8 py-5 text-[10px] font-black text-gray-400 uppercase tracking-widest">Action</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-50">
                <tr v-for="member in activeMembers" :key="member.uuid" class="hover:bg-gray-50/30 transition-colors group">
                  <td class="px-8 py-5">
                    <div class="flex items-center gap-4">
                      <div class="w-10 h-10 rounded-xl bg-[#112830] text-white flex items-center justify-center font-black text-sm overflow-hidden border border-white/10">
                        {{ (member.user.email || member.user.username || 'A')[0].toUpperCase() }}
                      </div>
                      <div>
                        <p class="font-bold text-[#112830]">{{ member.user.first_name }} {{ member.user.last_name }}</p>
                        <p class="text-[10px] text-gray-400">{{ member.user.email }}</p>
                      </div>
                    </div>
                  </td>
                  <td class="px-8 py-5">
                    <select 
                      v-if="!member.is_leader"
                      v-model="member.role.uuid"
                      @change="updateMemberRole(member)"
                      class="px-3 py-1 bg-gray-100 text-[#112830] rounded-lg text-[10px] font-black uppercase tracking-tighter border-none outline-none cursor-pointer hover:bg-gray-200 transition-colors"
                    >
                      <option v-for="r in roles" :key="r.uuid" :value="r.uuid">
                        {{ r.name }}
                      </option>
                    </select>
                    <span v-else class="px-3 py-1 bg-gray-100 text-[#112830] rounded-lg text-[10px] font-black uppercase tracking-tighter">
                      {{ member.role.name }}
                    </span>
                  </td>
                  <td class="px-8 py-5">
                     <button v-if="!member.is_leader" @click="removeMember(member)" class="text-gray-300 hover:text-rose-500 transition-colors" title="Retirer">
                        <i class="bx bx-trash text-lg"></i>
                     </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- ===== SUPERVISION TAB ===== -->
      <div v-else-if="activeTab === 'supervision'" class="space-y-8">
         <!-- Supervision content (already implemented in previous step) -->
         <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="p-8 bg-white rounded-[2.5rem] border border-gray-100 shadow-sm group hover:border-[#10b481] transition-all duration-500">
             <div class="w-14 h-14 rounded-2xl bg-emerald-50 text-[#10b481] flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
               <i class="bx bx-area text-2xl"></i>
             </div>
             <p class="text-xs font-black text-gray-400 uppercase tracking-widest mb-1">Superficie Totale</p>
             <h4 class="text-3xl font-black text-[#112830]">{{ totalArea.toFixed(1) }} <span class="text-sm font-medium text-gray-400">ha</span></h4>
          </div>
          <div class="p-8 bg-white rounded-[2.5rem] border border-gray-100 shadow-sm group hover:border-[#10b481] transition-all duration-500">
             <div class="w-14 h-14 rounded-2xl bg-amber-50 text-amber-500 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
               <i class="bx bx-leaf text-2xl"></i>
             </div>
             <p class="text-xs font-black text-gray-400 uppercase tracking-widest mb-1">Cultures Actives</p>
             <h4 class="text-3xl font-black text-[#112830]">{{ groupCrops.length }}</h4>
          </div>
          <div class="p-8 bg-white rounded-[2.5rem] border border-gray-100 shadow-sm group hover:border-[#10b481] transition-all duration-500">
             <div class="w-14 h-14 rounded-2xl bg-blue-50 text-blue-500 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
               <i class="bx bx-task text-2xl"></i>
             </div>
             <p class="text-xs font-black text-gray-400 uppercase tracking-widest mb-1">Tâches en cours</p>
             <h4 class="text-3xl font-black text-[#112830]">{{ pendingTasks }}</h4>
          </div>
        </div>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div class="bg-white rounded-[2.5rem] border border-gray-100 shadow-sm overflow-hidden">
             <div class="p-8 border-b border-gray-50"><h3 class="text-xl font-black text-[#112830]">Parcelles du Groupe</h3></div>
             <div class="p-4 overflow-y-auto max-h-[400px]">
               <div v-for="p in groupParcels" :key="p.uuid" class="p-4 hover:bg-gray-50 rounded-2xl flex items-center justify-between group transition-colors">
                  <div class="flex items-center gap-4">
                    <div class="w-12 h-12 rounded-xl bg-gray-50 flex items-center justify-center text-[#112830] font-black group-hover:bg-[#112830] group-hover:text-white transition-all">{{ p.area }}</div>
                    <div><p class="font-bold text-[#112830]">{{ p.parcel_name || p.name }}</p><p class="text-[10px] text-gray-400">Propriétaire: {{ p.owner?.username || 'Inconnu' }}</p></div>
                  </div>
               </div>
               <div v-if="groupParcels.length === 0" class="py-12 text-center text-gray-400 italic">Aucune parcelle enregistrée.</div>
             </div>
          </div>
          <div class="bg-white rounded-[2.5rem] border border-gray-100 shadow-sm overflow-hidden">
             <div class="p-8 border-b border-gray-50"><h3 class="text-xl font-black text-[#112830]">Urgences Terrain</h3></div>
             <div class="p-4 overflow-y-auto max-h-[400px]">
               <div v-for="t in groupTasks" :key="t.uuid" class="p-4 flex items-center justify-between border-b border-gray-50 last:border-0">
                  <div class="flex items-center gap-4">
                    <div :class="['w-2 h-2 rounded-full', t.priority?.name === 'HIGH' ? 'bg-rose-500' : 'bg-amber-500']"></div>
                    <div><p class="font-bold text-[#112830] text-sm">{{ t.name }}</p></div>
                  </div>
               </div>
               <div v-if="groupTasks.length === 0" class="py-12 text-center text-gray-400 italic">Aucune tâche en attente.</div>
             </div>
          </div>
        </div>
      </div>
    </div>

    <!-- MODAL: ADD MEMBER -->
    <div v-if="showAddMemberModal" class="fixed inset-0 z-[100] flex items-center justify-center p-6 backdrop-blur-md bg-black/20">
       <div class="bg-white w-full max-w-xl rounded-[3rem] p-10 shadow-2xl relative">
          <button @click="showAddMemberModal = false" class="absolute top-8 right-8 text-gray-400 hover:text-gray-600">
            <i class="bx bx-x text-3xl"></i>
          </button>
          <h2 class="text-2xl font-black text-[#112830] mb-2 text-center">Ajouter un Membre</h2>
          <p class="text-sm text-gray-400 text-center mb-8">Recherchez un utilisateur pour l'inviter dans <b>{{ group.name }}</b></p>
          
          <div class="space-y-6">
            <div class="relative">
              <i class="bx bx-search absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"></i>
              <input v-model="userSearchQuery" type="text" placeholder="Nom d'utilisateur ou email..." class="w-full pl-12 pr-4 py-4 bg-gray-50 rounded-2xl border-none outline-none focus:ring-2 focus:ring-[#10b481]/30 transition-all font-medium" @input="searchUsers" />
              
              <!-- Search Results Dropdown -->
              <div v-if="searchResults.length > 0" class="absolute left-0 right-0 top-full mt-2 bg-white rounded-3xl border border-gray-100 shadow-2xl z-10 max-h-60 overflow-y-auto">
                 <div v-for="u in searchResults" :key="u.uuid" @click="selectUser(u)" class="p-4 hover:bg-gray-50 cursor-pointer flex items-center gap-4 border-b border-gray-50 last:border-0">
                    <div class="w-10 h-10 rounded-xl bg-gray-100 flex items-center justify-center font-bold">{{ u.username[0] }}</div>
                    <div>
                      <p class="font-bold text-sm">{{ u.first_name }} {{ u.last_name }}</p>
                      <p class="text-[10px] text-gray-400">@{{ u.username }}</p>
                    </div>
                 </div>
              </div>
            </div>

            <div v-if="selectedUserForAdd" class="p-4 bg-emerald-50 rounded-2xl flex items-center justify-between animate-in slide-in-from-top-4 duration-300">
               <div class="flex items-center gap-3">
                  <i class="bx bx-user-check text-[#10b481] text-xl"></i>
                  <span class="font-bold text-[#10b481]">{{ selectedUserForAdd.username }} sélectionné</span>
               </div>
               <button @click="selectedUserForAdd = null" class="text-emerald-300 hover:text-emerald-500"><i class="bx bx-x text-xl"></i></button>
            </div>

            <div class="space-y-1">
              <label class="text-xs font-black text-gray-400 uppercase tracking-widest pl-2">Rôle</label>
              <select v-model="newMemberRole" class="w-full p-4 bg-gray-50 rounded-2xl border-none outline-none focus:ring-2 focus:ring-[#10b481]/30 transition-all font-medium">
                <option v-for="r in roles" :key="r.uuid" :value="r.uuid">{{ r.name }}</option>
              </select>
            </div>

            <div class="pt-4">
              <button @click="addMember" :disabled="!selectedUserForAdd || !newMemberRole || isSubmitting" class="w-full py-5 bg-[#112830] text-white rounded-2xl font-bold disabled:opacity-50 hover:bg-[#10b481] transition-all duration-500 shadow-xl shadow-[#112830]/10">
                {{ isSubmitting ? 'Envoi...' : 'Envoyer l\'invitation' }}
              </button>
            </div>
          </div>
       </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useApi } from '~/composables/useApi';

definePageMeta({ layout: 'dashboard' });

const route = useRoute();
const router = useRouter();
const { apiFetch } = useApi();

const uuid = route.params.uuid as string;
const isLoading = ref(true);
const isSubmitting = ref(false);
const activeTab = ref('members');

const group = ref<any>(null);
const members = ref<any[]>([]);
const roles = ref<any[]>([]);

// Search/Add logic
const showAddMemberModal = ref(false);
const userSearchQuery = ref('');
const searchResults = ref<any[]>([]);
const selectedUserForAdd = ref<any>(null);
const newMemberRole = ref('');

// Supervision data
const groupParcels = ref<any[]>([]);
const groupCrops = ref<any[]>([]);
const groupTasks = ref<any[]>([]);

const activeMembers = computed(() => members.value.filter(m => m.status === 'ACTIVE'));
const pendingMembers = computed(() => members.value.filter(m => m.status === 'PENDING'));

async function fetchGroupDetails() {
  isLoading.value = true;
  try {
    const [groupData, memberData] = await Promise.all([
      apiFetch(`/api/groups/${uuid}/`),
      apiFetch(`/api/member-groups/?group=${uuid}`)
    ]);
    group.value = groupData;
    members.value = (memberData as any).results || memberData || [];
  } catch (err) {
    console.error("Erreur fetchGroupDetails:", err);
  } finally {
    isLoading.value = false;
  }
}

async function fetchRoles() {
  try {
    const data: any = await apiFetch('/api/group-roles/');
    roles.value = data.results || data || [];
    const memberRole = roles.value.find(r => r.name.toUpperCase().includes('MEMBRE'));
    if (memberRole) newMemberRole.value = memberRole.uuid;
  } catch (err) {
    console.error("Erreur fetchRoles:", err);
  }
}

async function handleMemberAction(member: any, action: 'approve' | 'reject') {
  try {
    const endpoint = action === 'approve' ? 'approve' : 'reject';
    await apiFetch(`/api/member-groups/${member.uuid}/${endpoint}/`, { method: 'POST' });
    if (action === 'approve') {
       member.status = 'ACTIVE';
    } else {
       members.value = members.value.filter(m => m.uuid !== member.uuid);
    }
    alert(action === 'approve' ? "Membre approuvé !" : "Membre retiré/rejeté.");
  } catch (err) {
    console.error(`Erreur ${action}:`, err);
    alert("Une erreur est survenue.");
  }
}

async function updateMemberRole(member: any) {
  try {
    const newRoleUuid = member.role.uuid;
    await apiFetch(`/api/member-groups/${member.uuid}/`, {
      method: 'PATCH',
      body: { role_id: newRoleUuid }
    });
    const roleObj = roles.value.find((r: any) => r.uuid === newRoleUuid);
    if (roleObj) {
      member.role = { ...member.role, ...roleObj };
    }
  } catch (err) {
    console.error("Erreur updateMemberRole:", err);
    alert("Impossible de mettre à jour le rôle.");
  }
}

async function removeMember(member: any) {
  if (!confirm(`Voulez-vous vraiment retirer ce membre du groupe ?`)) return;
  try {
    await apiFetch(`/api/member-groups/${member.uuid}/`, { method: 'DELETE' });
    members.value = members.value.filter(m => m.uuid !== member.uuid);
  } catch (err) {
    console.error("Erreur removeMember:", err);
    alert("Impossible de retirer le membre.");
  }
}

async function openAddMemberModal() {
  showAddMemberModal.value = true;
  if (roles.value.length === 0) await fetchRoles();
}

let searchTimeout: any;
function searchUsers() {
  if (userSearchQuery.value.length < 3) {
    searchResults.value = [];
    return;
  }
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(async () => {
    try {
      const data: any = await apiFetch(`/api/users/?search=${encodeURIComponent(userSearchQuery.value)}`);
      searchResults.value = (data.results || data || []).filter((u: any) => 
         !members.value.some(m => m.user?.uuid === u.uuid || m.user === u.uuid)
      );
    } catch (err) {
       console.error("Erreur searchUsers:", err);
    }
  }, 500);
}

function selectUser(user: any) {
  selectedUserForAdd.value = user;
  userSearchQuery.value = '';
  searchResults.value = [];
}

async function addMember() {
  if (!selectedUserForAdd.value || !newMemberRole.value) return;
  isSubmitting.value = true;
  try {
    const newMember: any = await apiFetch('/api/member-groups/', {
      method: 'POST',
      body: {
        user_id: selectedUserForAdd.value.uuid,
        group_id: uuid,
        role_id: newMemberRole.value
      }
    });
    members.value.unshift(newMember);
    showAddMemberModal.value = false;
    selectedUserForAdd.value = null;
    alert("Invitation envoyée ! Le membre apparaîtra en attente jusqu'à acceptation.");
  } catch (err) {
    console.error("Erreur addMember:", err);
    alert("Impossible d'ajouter ce membre (déjà invité ?)");
  } finally {
    isSubmitting.value = false;
  }
}

async function fetchSupervisionData() {
  try {
    const [parcelData, cropData, taskData] = await Promise.all([
      apiFetch('/api/parcels/'),
      apiFetch('/api/parcel-crops/'),
      apiFetch('/api/tasks/')
    ]);
    const memberUserIds = members.value.map(m => m.user?.uuid || m.user);
    groupParcels.value = ((parcelData as any).results || parcelData || []).filter((p: any) => memberUserIds.includes(p.owner?.uuid));
    groupCrops.value = ((cropData as any).results || cropData || []).filter((c: any) => memberUserIds.includes(c.parcel?.owner?.uuid));
    groupTasks.value = ((taskData as any).results || taskData || []).filter((t: any) => memberUserIds.includes(t.parcelCrop?.parcel?.owner?.uuid));
  } catch (err) {
    console.error("Erreur fetchSupervisionData:", err);
  }
}

const totalArea = computed(() => groupParcels.value.reduce((acc, p) => acc + (parseFloat(p.area) || 0), 0));
const pendingTasks = computed(() => groupTasks.value.filter(t => t.status?.name !== 'COMPLETED').length);

watch(activeTab, (newTab) => { if (newTab === 'supervision') fetchSupervisionData(); });

onMounted(() => {
  fetchRoles();
  fetchGroupDetails();
});
</script>
