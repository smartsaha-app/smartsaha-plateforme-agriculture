<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8 space-y-6">

    <!-- ===== HEADER ===== -->
    <PageHeader :title="t('organization.groupsTitle')">
      <template #subtitle>
        <i class="bx bx-group"></i>
        {{ t('organization.groupsDesc') }}
      </template>
      <template #breadcrumb>
        <NuxtLink to="/organization/dashboard" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
          <span>{{ t('dashboard.home') }}</span>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">{{ t('organization.groupsTitle') }}</span>
      </template>
    </PageHeader>

    <div class="flex justify-end -mt-2">
      <button @click="openCreateModal()"
        class="flex items-center gap-2 px-4 py-2.5 bg-[#112830] text-white rounded-xl text-sm font-bold hover:bg-[#10b481] transition-all shadow-sm">
        <i class="bx bx-plus text-base"></i>
        {{ t('organization.createGroup') }}
      </button>
    </div>

    <!-- ===== STATS FAST VIEW ===== -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div v-for="stat in quickStats" :key="stat.label" class="bg-white p-6 rounded-xl border border-gray-100 shadow-sm flex items-center gap-4">
        <div :class="['w-12 h-12 rounded-2xl flex items-center justify-center text-xl shadow-sm', stat.bg, stat.text]">
          <i :class="stat.icon"></i>
        </div>
        <div>
          <p class="text-xs font-bold text-gray-400 uppercase tracking-widest">{{ stat.label }}</p>
          <p class="text-2xl font-black text-[#112830]">{{ stat.value }}</p>
        </div>
      </div>
    </div>

    <!-- ===== SEARCH & FILTERS ===== -->
    <div class="bg-white p-4 rounded-xl border border-gray-100 shadow-sm flex flex-col md:flex-row gap-4">
      <div class="flex-1 relative">
        <i class="bx bx-search absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"></i>
        <input
          v-model="searchQuery"
          type="text"
          :placeholder="t('organization.searchGroup')"
          class="w-full pl-12 pr-4 py-3 bg-gray-50 rounded-2xl border-none focus:ring-2 focus:ring-[#10b481]/20 outline-none transition-all"
        />
      </div>
      <div class="flex gap-2">
        <select v-model="filterType" class="px-4 py-3 bg-gray-50 rounded-2xl border-none focus:ring-2 focus:ring-[#10b481]/20 outline-none cursor-pointer text-sm font-medium text-gray-600">
          <option value="all">{{ t('organization.allTypes') }}</option>
          <option v-for="gt in groupTypes" :key="gt.uuid" :value="gt.uuid">{{ gt.name }}</option>
        </select>
      </div>
    </div>

    <!-- ===== GROUPS GRID ===== -->
    <div v-if="isLoading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="i in 6" :key="i" class="h-64 bg-gray-50 rounded-xl animate-pulse"></div>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="group in filteredGroups" :key="group.uuid" 
          class="group bg-white rounded-2xl border border-gray-100 shadow-sm hover:shadow-xl transition-all duration-500 overflow-hidden flex flex-col relative">

        <div class="p-8 space-y-4 flex-1">
          <!-- Header: icône + actions toujours visibles -->
          <div class="flex items-start justify-between">
            <div @click="viewDetails(group)" class="w-14 h-14 rounded-2xl bg-gray-50 flex items-center justify-center text-[#112830] group-hover:bg-[#10b481] group-hover:text-white transition-all duration-500 shadow-sm border border-gray-100 cursor-pointer">
              <i class="bx bx-group text-2xl"></i>
            </div>

            <!-- Boutons Edit / Delete toujours visibles -->
            <div class="flex items-center gap-2">
              <button @click.stop="openEditModal(group)" 
                      class="w-8 h-8 rounded-lg bg-blue-50 flex items-center justify-center text-blue-400 hover:bg-blue-500 hover:text-white transition-all duration-200 shadow-sm">
                <i class="bx bx-edit text-lg"></i>
              </button>
              <button @click.stop="confirmDelete(group)" 
                      class="w-8 h-8 rounded-lg bg-rose-50 flex items-center justify-center text-rose-400 hover:bg-rose-500 hover:text-white transition-all duration-200 shadow-sm">
                <i class="bx bx-trash text-lg"></i>
              </button>
            </div>
          </div>

          <!-- Badge type -->
          <div>
            <span class="px-3 py-1 bg-blue-50 text-blue-600 rounded-full text-[10px] font-black uppercase tracking-widest">
              {{ group.type?.name || 'Standard' }}
            </span>
          </div>

          <!-- Nom + description -->
          <div @click="viewDetails(group)" class="cursor-pointer">
            <h3 class="text-xl font-black text-[#112830] mb-1">{{ group.name }}</h3>
            <p class="text-sm text-gray-400 line-clamp-2">{{ group.description || 'Aucune description fournie.' }}</p>
          </div>

          <!-- Membres -->
          <div class="flex items-center gap-4 pt-2">
            <span class="text-xs font-bold text-gray-500">{{ group.active_members_count || 0 }} {{ t('organization.groupMembers') }}</span>
          </div>
        </div>

        <!-- Footer -->
        <div class="px-8 py-5 bg-gray-50/50 border-t border-gray-50 flex items-center justify-between">
          <div class="flex items-center gap-2 text-xs font-bold text-gray-400">
            <i class="bx bx-calendar"></i>
            <span>{{ new Date(group.created_at).toLocaleDateString() }}</span>
          </div>
          <button @click="viewDetails(group)" class="text-[#10b481] text-sm font-bold hover:underline flex items-center gap-1">
            {{ t('organization.manage') }} <i class="bx bx-right-arrow-alt"></i>
          </button>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="!isLoading && filteredGroups.length === 0" class="py-20 text-center space-y-4">
      <div class="w-24 h-24 bg-gray-50 rounded-full flex items-center justify-center mx-auto text-gray-200">
        <i class="bx bx-folder-open text-5xl"></i>
      </div>
      <p class="text-gray-400 font-medium italic">{{ t('organization.noGroups') }}</p>
    </div>

    <!-- CRUD MODAL -->
    <div v-if="showModal" class="fixed inset-0 z-[100] flex items-center justify-center p-6 backdrop-blur-md bg-black/20">
       <div class="bg-white w-full max-w-lg rounded-2xl p-10 shadow-2xl space-y-6 relative border border-white/20">
          <button @click="showModal = false" class="absolute top-6 right-6 w-10 h-10 rounded-full hover:bg-gray-100 flex items-center justify-center transition-colors">
            <i class="bx bx-x text-2xl"></i>
          </button>
          
          <h2 class="text-2xl font-black text-[#112830]">{{ isEditing ? t('organization.editGroupTitle') : t('organization.newGroupTitle') }}</h2>
          
          <div class="space-y-4">
            <div class="space-y-1">
              <label class="text-xs font-black text-gray-400 uppercase tracking-widest">{{ t('organization.groupNameLabel') }}</label>
              <input v-model="formGroup.name" type="text" :placeholder="t('organization.groupNamePlaceholder')" class="w-full p-4 bg-gray-50 rounded-2xl border-none outline-none focus:ring-2 focus:ring-[#10b481]/30 transition-all font-medium" />
            </div>
            <div class="space-y-1">
              <label class="text-xs font-black text-gray-400 uppercase tracking-widest">{{ t('organization.groupTypeLabel') }}</label>
              <select v-model="formGroup.type_id" class="w-full p-4 bg-gray-50 rounded-2xl border-none outline-none focus:ring-2 focus:ring-[#10b481]/30 transition-all font-medium">
                <option v-for="gt in groupTypes" :key="gt.uuid" :value="gt.uuid">{{ gt.name }}</option>
              </select>
            </div>
            <div class="space-y-1">
              <label class="text-xs font-black text-gray-400 uppercase tracking-widest">{{ t('organization.groupDescLabel') }}</label>
              <textarea v-model="formGroup.description" :placeholder="t('organization.groupDescPlaceholder')" class="w-full p-4 bg-gray-50 rounded-2xl border-none outline-none focus:ring-2 focus:ring-[#10b481]/30 transition-all font-medium h-24 resize-none"></textarea>
            </div>
          </div>
          
          <div class="flex gap-3 pt-4">
            <button @click="showModal = false" class="flex-1 py-3 text-gray-400 font-bold hover:text-gray-600 transition border border-gray-100 rounded-xl">{{ t('dashboard.cancel') }}</button>
            <button @click="saveGroup" :disabled="isSaving" class="flex-1 py-3 px-8 bg-[#112830] text-white rounded-xl font-bold hover:bg-[#10b481] transition-all disabled:opacity-50 flex items-center justify-center gap-2">
              <div v-if="isSaving" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              <i v-else class="bx bx-save"></i>
              {{ isEditing ? t('organization.saveGroup') : t('organization.createGroupBtn') }}
            </button>
          </div>
       </div>
    </div>

    <!-- DELETE MODAL -->
    <div v-if="groupToDelete" class="fixed inset-0 z-[100] flex items-center justify-center p-6 backdrop-blur-sm bg-black/20">
      <div class="bg-white w-full max-w-sm rounded-2xl p-8 shadow-2xl space-y-5 border border-gray-100">
        <div class="text-center space-y-3">
          <div class="w-14 h-14 bg-rose-50 rounded-2xl flex items-center justify-center mx-auto">
            <i class="bx bx-trash text-2xl text-rose-500"></i>
          </div>
          <div>
            <h2 class="text-base font-black text-[#112830]">{{ t('organization.deleteGroupTitle') }}</h2>
            <p class="text-sm text-gray-400 mt-1">
              "<span class="font-bold text-[#112830]">{{ groupToDelete.name }}</span>" {{ t('organization.deleteGroupDesc') }}
            </p>
          </div>
        </div>
        <div class="flex gap-3">
          <button @click="groupToDelete = null" class="flex-1 py-3 rounded-xl border border-gray-100 text-gray-500 font-bold text-sm hover:bg-gray-50 transition-colors">{{ t('dashboard.cancel') }}</button>
          <button @click="executeDelete" :disabled="isDeleting"
            class="flex-1 py-3 rounded-xl bg-rose-500 text-white font-bold text-sm hover:bg-rose-600 transition-colors disabled:opacity-50 flex items-center justify-center gap-2">
            <div v-if="isDeleting" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            <i v-else class="bx bx-trash"></i>
            {{ t('dashboard.delete') }}
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
import { useRouter } from 'vue-router';
import { ref, computed, onMounted } from 'vue';
import { useApi } from '~/composables/useApi';
import { useAuthStore } from '~/stores/auth';
import { useKycGuard } from '~/composables/useKycGuard';

definePageMeta({ layout: 'dashboard' });
const { t } = useI18n();

const router = useRouter();
const { apiFetch } = useApi();
const authStore = useAuthStore();
const { requireKyc } = useKycGuard();

const isLoading    = ref(true);
const isSaving     = ref(false);
const isDeleting   = ref(false);
const showModal    = ref(false);
const isEditing    = ref(false);
const searchQuery  = ref('');
const filterType   = ref('all');
const groupToDelete = ref<any>(null);
const toast = ref({ visible: false, message: '', type: 'success' as 'success' | 'error' });

function showToast(message: string, type: 'success' | 'error' = 'success') {
  toast.value = { visible: true, message, type };
  setTimeout(() => (toast.value.visible = false), 3000);
}

const groups = ref<any[]>([]);
const groupTypes = ref<any[]>([]);

const formGroup = ref({
  uuid: '',
  name: '',
  description: '',
  type_id: '',
  organisation_id: ''
});

const quickStats = computed(() => [
  { label: t('organization.totalGroups'),   value: groups.value.length.toString(), icon: 'bx bx-layer', bg: 'bg-emerald-50', text: 'text-emerald-600' },
  { label: t('organization.activeMembers'), value: groups.value.reduce((acc, g) => acc + (g.active_members_count || 0), 0).toString(), icon: 'bx bx-user-check', bg: 'bg-blue-50', text: 'text-blue-600' },
  { label: t('dashboard.status'),           value: t('organization.statusOperational'), icon: 'bx bx-check-shield', bg: 'bg-amber-50', text: 'text-amber-600' },
]);

const filteredGroups = computed(() => {
  let result = groups.value;
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase();
    result = result.filter(g => 
      g.name.toLowerCase().includes(q) ||
      (g.description && g.description.toLowerCase().includes(q))
    );
  }
  if (filterType.value !== 'all') {
    result = result.filter(g => g.type?.uuid === filterType.value);
  }
  return result;
});

async function fetchGroups() {
  isLoading.value = true;
  try {
    const data: any = await apiFetch('/api/groups/');
    groups.value = data.results || data || [];
  } catch (err) {
    console.error("Erreur fetchGroups:", err);
  } finally {
    isLoading.value = false;
  }
}

async function fetchTypes() {
  try {
    const data: any = await apiFetch('/api/group-types/');
    groupTypes.value = data.results || data || [];
  } catch (err) {
    console.error("Erreur fetchTypes:", err);
  }
}

function openCreateModal() {
  if (!requireKyc()) return
  isEditing.value = false;
  formGroup.value = { uuid: '', name: '', description: '', type_id: groupTypes.value[0]?.uuid || '', organisation_id: '' };
  showModal.value = true;
}

function openEditModal(group: any) {
  isEditing.value = true;
  formGroup.value = {
    uuid: group.uuid,
    name: group.name,
    description: group.description,
    type_id: group.type?.uuid,
    organisation_id: group.organisation?.uuid
  };
  showModal.value = true;
}

async function saveGroup() {
  isSaving.value = true;
  try {
    const userData: any = await apiFetch(`/api/users/${authStore.uuid}/`);
    const orgId = userData.organisations_created?.[0]?.uuid;
    if (!orgId) { showToast(t('organization.groupSaveError'), 'error'); return; }

    const payload = {
      name: formGroup.value.name,
      description: formGroup.value.description,
      type_id: formGroup.value.type_id,
      organisation_id: orgId,
    };

    if (isEditing.value) {
      await apiFetch(`/api/groups/${formGroup.value.uuid}/`, { method: 'PATCH', body: payload });
      showToast(t('organization.groupSaved'));
    } else {
      await apiFetch('/api/groups/', { method: 'POST', body: payload });
      showToast(t('organization.groupCreated'));
    }
    showModal.value = false;
    fetchGroups();
  } catch (err) {
    console.error('Erreur saveGroup:', err);
    showToast(t('organization.groupSaveError'), 'error');
  } finally {
    isSaving.value = false;
  }
}

function confirmDelete(group: any) { groupToDelete.value = group; }

async function executeDelete() {
  if (!groupToDelete.value) return;
  isDeleting.value = true;
  try {
    await apiFetch(`/api/groups/${groupToDelete.value.uuid}/`, { method: 'DELETE' });
    showToast(t('organization.groupDeleted'));
    groupToDelete.value = null;
    fetchGroups();
  } catch (err) {
    console.error('Erreur deleteGroup:', err);
    showToast(t('organization.groupDeleteError'), 'error');
  } finally {
    isDeleting.value = false;
  }
}

function viewDetails(group: any) {
  router.push(`/organization/groups/${group.uuid}`);
}

onMounted(() => {
  fetchGroups();
  fetchTypes();
});
</script>

