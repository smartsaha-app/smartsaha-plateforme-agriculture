<template>
  <div class="p-6 space-y-8 max-w-[1500px] mx-auto text-[#112830]">
    <!-- ===== HEADER ===== -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-6">
      <div>
        <h1 class="text-3xl font-extrabold tracking-tight">Validation des Audits S&E</h1>
        <p class="text-gray-500 font-medium tracking-tight">Vérifiez les preuves de conformité et validez les certifications des partenaires.</p>
      </div>
      <div class="flex bg-white p-1.5 rounded-2xl border border-gray-100 shadow-sm">
        <button v-for="s in statusFilters" :key="s" 
                @click="selectedStatus = s"
                :class="['px-6 py-2 rounded-xl text-xs font-black uppercase tracking-widest transition-all', selectedStatus === s ? 'bg-[#112830] text-white shadow-lg' : 'text-gray-400 hover:text-gray-600']">
          {{ s }}
        </button>
      </div>
    </div>

    <!-- ===== AUDIT QUEUE ===== -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- Left: List of Pending Audits -->
      <div class="bg-white rounded-[2.5rem] p-8 border border-gray-100 shadow-sm flex flex-col space-y-6">
        <div class="flex items-center justify-between">
          <h3 class="text-xl font-black">Audit Queue</h3>
          <span class="text-[10px] font-black text-emerald-600 bg-emerald-50 px-2 py-1 rounded uppercase tracking-widest">{{ filteredAudits.length }} Dossiers</span>
        </div>

        <div class="space-y-4 overflow-y-auto max-h-[600px] pr-2 custom-scrollbar">
          <div v-for="audit in filteredAudits" :key="audit.id" 
               @click="selectedAudit = audit"
               :class="['p-6 rounded-[2rem] border transition-all cursor-pointer group relative overflow-hidden', selectedAudit?.id === audit.id ? 'border-[#10b481] bg-emerald-50/30' : 'border-gray-50 bg-gray-50/30 hover:bg-white hover:border-gray-200']">
            <!-- (Content of audit card) -->
            <div class="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity">
              <i class="bx bx-shield-quarter text-5xl"></i>
            </div>

            <div class="flex justify-between items-start mb-3">
              <span class="px-2 py-0.5 bg-blue-100 text-blue-600 text-[9px] font-black uppercase rounded tracking-widest">{{ audit.type }}</span>
              <span class="text-[10px] font-bold text-gray-400">{{ audit.date }}</span>
            </div>
            
            <h4 class="font-black text-lg mb-1 group-hover:text-[#10b481] transition-colors">{{ audit.org }}</h4>
            <p class="text-xs text-gray-500 mb-4 px-2 border-l-2 border-gray-200">{{ audit.summary }}</p>
            
            <div class="flex items-center justify-between pt-4 border-t border-gray-100/50">
               <div class="flex items-center gap-2 text-[10px] font-bold text-gray-400">
                 <i class="bx bx-user-circle"></i>
                 <span>Auditeur: {{ audit.auditor }}</span>
               </div>
               <div class="flex items-center gap-1 font-black text-sm" :class="audit.score >= 90 ? 'text-emerald-600' : 'text-amber-600'">
                 {{ audit.score }}%
               </div>
            </div>
          </div>
        </div>

        <!-- Pagination Component -->
        <div v-if="!isLoading && totalCount > 20" class="pt-4 border-t border-gray-100">
           <PaginationBase 
              :totalCount="totalCount" 
              :perPage="20" 
              v-model:currentPage="currentPage" 
              @change-page="(p) => currentPage = p" 
           />
        </div>
      </div>

      <!-- Right: Detailed Review Panel -->
      <div v-if="selectedAudit" class="bg-[#112830] rounded-[2.5rem] p-10 text-white shadow-xl relative flex flex-col overflow-hidden animate-in fade-in slide-in-from-right duration-500">
        <div class="relative z-10 space-y-8 flex-1">
          <div class="flex justify-between items-start">
            <div class="space-y-1">
              <p class="text-[#10b481] text-[10px] font-black uppercase tracking-[0.2em]">Détails du Dossier</p>
              <h2 class="text-3xl font-black">{{ selectedAudit.org }}</h2>
            </div>
            <div class="w-16 h-16 rounded-2xl bg-white/10 flex items-center justify-center text-3xl text-[#10b481] border border-white/10">
              <i class="bx bx-file-find"></i>
            </div>
          </div>

          <!-- Proof Checklist -->
          <div class="space-y-4 bg-white/5 p-6 rounded-[2rem] border border-white/5">
            <h4 class="text-xs font-black uppercase tracking-widest text-white/40 mb-2">Documents à vérifier :</h4>
            <div v-for="doc in selectedAudit.docs" :key="doc.name" class="flex items-center justify-between group/doc">
              <div class="flex items-center gap-3">
                <i :class="['bx text-xl', doc.checked ? 'bx-check-circle text-[#10b481]' : 'bx-circle text-white/20']"></i>
                <span class="text-sm font-bold text-white/80">{{ doc.name }}</span>
              </div>
              <button class="text-[10px] font-black uppercase text-white/40 group-hover/doc:text-[#10b481] transition-colors underline">Voir</button>
            </div>
          </div>

          <div class="space-y-4">
            <h4 class="text-xs font-black uppercase tracking-widest text-white/40">Note de l'Auditeur :</h4>
            <p class="text-sm text-white/60 leading-relaxed italic bg-black/20 p-5 rounded-2xl border-l-4 border-[#10b481]">
              "{{ selectedAudit.notes }}"
            </p>
          </div>
        </div>

        <div class="mt-10 pt-10 border-t border-white/10 flex gap-4 relative z-10">
          <button @click="approveAudit" class="flex-1 py-5 bg-[#10b481] hover:bg-white hover:text-[#112830] text-white rounded-[1.5rem] font-black transition-all duration-500 shadow-2xl flex items-center justify-center gap-2">
            <i class="bx bx-check-shield text-xl"></i> Approuver
          </button>
          <button @click="rejectAudit" class="px-8 py-5 bg-white/10 hover:bg-rose-500 text-white rounded-[1.5rem] font-black transition-all border border-white/10 flex items-center justify-center gap-2">
            <i class="bx bx-x-circle text-xl"></i> Rejeter
          </button>
        </div>

        <i class="bx bx-badge-check absolute bottom-[-10%] right-[-10%] text-[20rem] text-white/5 pointer-events-none"></i>
      </div>

      <!-- Detail Placeholder -->
      <div v-else class="bg-gray-50 rounded-[2.5rem] border-2 border-dashed border-gray-200 flex flex-col items-center justify-center py-20 text-center space-y-4">
        <div class="w-20 h-20 rounded-full bg-white flex items-center justify-center text-gray-200 text-4xl shadow-sm">
          <i class="bx bx-mouse-alt"></i>
        </div>
        <div>
          <h3 class="text-xl font-bold text-gray-400">Aucun dossier sélectionné</h3>
          <p class="text-sm text-gray-300">Sélectionnez un audit dans la liste pour réviser les documents.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useApi } from '~/composables/useApi';
import PaginationBase from '~/components/ui/PaginationBase.vue';

definePageMeta({ layout: 'dashboard' });

const { apiFetch } = useApi();
const isLoading = ref(true);
const selectedStatus = ref('En attente');
const statusFilters = ['En attente', 'Validés', 'Rejetés'];

const audits = ref<any[]>([]);
const selectedAudit = ref<any>(null);
const totalCount = ref(0);
const currentPage = ref(1);

const statusMap: Record<string, string> = {
  'En attente': 'PENDING',
  'Validés': 'PASS',
  'Rejetés': 'FAIL'
};

const reverseStatusMap: Record<string, string> = {
  'PENDING': 'En attente',
  'PASS': 'Validés',
  'FAIL': 'Rejetés'
};

async function fetchAudits() {
  isLoading.value = true;
  try {
    const statusVal = statusMap[selectedStatus.value];
    const data: any = await apiFetch(`/api/suivi-evaluation/api/certification-audits/?page=${currentPage.value}&result=${statusVal}`);
    const results = data.results || data || [];
    totalCount.value = data.count || results.length;
    audits.value = results.map((a: any) => ({
      id: a.uuid,
      org: a.report?.name || 'Inconnu',
      auditor: a.auditor,
      score: 100,
      date: new Date(a.date_audit).toLocaleDateString(),
      type: a.cert_type?.name || 'Audit',
      status: reverseStatusMap[a.result] || 'En attente',
      summary: a.remarks || 'Aucune remarque.',
      notes: a.remarks || '',
      docs: []
    }));
  } catch (err) {
    console.error("Erreur fetchAudits:", err);
  } finally {
    isLoading.value = false;
  }
}

watch(selectedStatus, () => {
  currentPage.value = 1;
  fetchAudits();
});

watch(currentPage, () => {
  fetchAudits();
});

const filteredAudits = computed(() => {
  return audits.value; // Déjà filtré par le serveur
});

async function updateAuditStatus(result: string) {
  if (!selectedAudit.value) return;
  try {
    await apiFetch(`/api/suivi-evaluation/api/certification-audits/${selectedAudit.value.id}/`, {
      method: 'PATCH',
      body: { result }
    });
    alert(`Audit mis à jour : ${result === 'PASS' ? 'Approuvé' : 'Rejeté'}`);
    selectedAudit.value = null;
    fetchAudits();
  } catch (err) {
    console.error("Erreur updateAuditStatus:", err);
    alert("Erreur lors de la mise à jour.");
  }
}

function approveAudit() {
  updateAuditStatus('PASS');
}

function rejectAudit() {
  updateAuditStatus('FAIL');
}

onMounted(() => {
  fetchAudits();
});
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #e5e7eb;
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #d1d5db;
}
</style>
