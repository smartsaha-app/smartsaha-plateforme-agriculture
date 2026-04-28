<template>
  <div class="p-6 space-y-8 max-w-[1400px] mx-auto">
    <!-- ===== HEADER ===== -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-6">
      <div>
        <h1 class="text-3xl font-extrabold text-[#112830]">Certifications & Conformité</h1>
        <p class="text-gray-500 font-medium">Suivez l'état de vos labels et préparez vos audits de certification.</p>
      </div>
      <div class="flex gap-3">
        <button class="px-5 py-3 bg-white border border-gray-100 text-gray-600 rounded-2xl font-bold hover:bg-gray-50 transition shadow-sm flex items-center gap-2">
          <i class="bx bx-download"></i> Rapport Global
        </button>
        <button @click="showAddModal = true" class="px-6 py-3 bg-[#10b481] text-white rounded-2xl font-bold hover:bg-[#0da06a] transition shadow-xl shadow-[#10b481]/20 flex items-center gap-2">
          <i class="bx bx-shield-plus"></i> Nouvelle Demande
        </button>
      </div>
    </div>

    <!-- ===== NOUVELLE DEMANDE MODAL ===== -->
    <div v-if="showAddModal" class="fixed inset-0 z-[100] flex items-center justify-center p-6 backdrop-blur-md bg-black/20">
      <div class="bg-white w-full max-w-lg rounded-[2.5rem] p-10 shadow-2xl space-y-6 relative border border-white/20">
        <button @click="showAddModal = false" class="absolute top-6 right-6 w-10 h-10 rounded-full hover:bg-gray-100 flex items-center justify-center transition-colors">
          <i class="bx bx-x text-2xl"></i>
        </button>
        <h2 class="text-2xl font-black text-[#112830]">Nouvelle Demande</h2>
        <div class="space-y-4">
          <div class="space-y-1">
            <label class="text-xs font-black text-gray-400 uppercase tracking-widest ml-2">Type de Certification</label>
            <select v-model="newCert.cert_type" class="w-full p-4 bg-gray-50 rounded-2xl border-none outline-none focus:ring-2 focus:ring-[#10b481]/30">
              <option v-for="t in certTypes" :key="t.uuid" :value="t.uuid">{{ t.name }}</option>
            </select>
          </div>
          <div class="space-y-1">
            <label class="text-xs font-black text-gray-400 uppercase tracking-widest ml-2">Organisme Émetteur</label>
            <input v-model="newCert.issued_by" type="text" placeholder="ex: Ecocert" class="w-full p-4 bg-gray-50 rounded-2xl border-none outline-none focus:ring-2 focus:ring-[#10b481]/30" />
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div class="space-y-1">
              <label class="text-xs font-black text-gray-400 uppercase tracking-widest ml-2">Date Émission</label>
              <input v-model="newCert.issued_at" type="date" class="w-full p-4 bg-gray-50 rounded-2xl border-none outline-none" />
            </div>
            <div class="space-y-1">
              <label class="text-xs font-black text-gray-400 uppercase tracking-widest ml-2">Date Expiration</label>
              <input v-model="newCert.expires_at" type="date" class="w-full p-4 bg-gray-50 rounded-2xl border-none outline-none" />
            </div>
          </div>
        </div>
        <div class="flex gap-4 pt-4">
          <button @click="showAddModal = false" class="flex-1 py-4 text-gray-400 font-bold hover:text-gray-600 transition">Annuler</button>
          <button @click="createCertification" :disabled="isSubmitting" class="flex-2 py-4 px-10 bg-[#112830] text-white rounded-2xl font-bold shadow-xl hover:bg-[#10b481] transition-all">
            {{ isSubmitting ? 'Envoi...' : 'Soumettre' }}
          </button>
        </div>
      </div>
    </div>

    <!-- ===== CERTIFICATION STATUS CARDS ===== -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
      <div v-for="cert in certifications" :key="cert.name" 
           class="group bg-white p-8 rounded-[2.5rem] border border-gray-100 shadow-sm hover:shadow-2xl transition-all duration-500 relative overflow-hidden">
        
        <div class="absolute top-0 right-0 p-6 opacity-5 group-hover:opacity-10 transition-opacity">
          <i :class="[cert.icon, 'text-7xl']"></i>
        </div>

        <div class="flex items-center gap-4 mb-6">
          <div :class="['w-14 h-14 rounded-2xl flex items-center justify-center text-2xl shadow-sm', cert.statusBg, cert.statusText]">
            <i :class="cert.icon"></i>
          </div>
          <div>
            <h3 class="text-xl font-black text-[#112830]">{{ cert.name }}</h3>
            <span :class="['text-[10px] font-black uppercase tracking-widest px-2 py-0.5 rounded-full', cert.statusBadgeBg, cert.statusBadgeText]">
              {{ cert.status }}
            </span>
          </div>
        </div>

        <div class="space-y-4">
          <div class="flex justify-between text-xs font-bold text-gray-400">
            <span>Score de Conformité</span>
            <span>{{ cert.score }}%</span>
          </div>
          <div class="h-2 bg-gray-50 rounded-full overflow-hidden">
            <div :class="['h-full transition-all duration-1000', cert.progressBarBg]" :style="{ width: cert.score + '%' }"></div>
          </div>
        </div>

        <div class="mt-8 flex items-center justify-between border-t border-gray-50 pt-5">
          <div class="text-xs text-gray-400 font-medium">
            <p>Expire le : <span class="text-[#112830] font-bold">{{ cert.expiry }}</span></p>
          </div>
          <button class="text-sm font-bold text-[#10b481] hover:underline">Documents</button>
        </div>
      </div>
    </div>

    <!-- ===== TIMELINE & DOCUMENTS ===== -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 text-[#112830]">
      <!-- Audits Timeline -->
      <div class="lg:col-span-1 bg-[#112830] rounded-[2.5rem] p-8 text-white shadow-xl">
        <h3 class="text-2xl font-bold mb-6 flex items-center gap-3">
          <i class="bx bx-calendar-event text-[#10b481]"></i> Prochains Audits
        </h3>
        
        <div class="space-y-8 relative before:absolute before:left-[11px] before:top-2 before:bottom-2 before:w-[2px] before:bg-white/10">
          <div v-for="audit in audits" :key="audit.id" class="relative pl-10 group">
            <div class="absolute left-0 top-1.5 w-[24px] h-[24px] rounded-full border-4 border-[#112830] bg-[#10b481] z-10 shadow-lg group-hover:scale-120 transition-transform"></div>
            <div class="space-y-1">
              <span class="text-xs font-black text-[#10b481] uppercase tracking-widest">{{ audit.date }}</span>
              <h4 class="font-bold text-lg leading-tight">{{ audit.title }}</h4>
              <p class="text-white/40 text-sm italic">{{ audit.location }}</p>
            </div>
            <div class="mt-4 p-4 bg-white/5 rounded-2xl border border-white/5 hover:bg-white/10 transition-colors">
              <p class="text-xs text-white/60 mb-2">Inspecteurs assignés :</p>
              <div class="flex -space-x-2">
                <div v-for="i in 2" :key="i" class="w-8 h-8 rounded-full border-2 border-[#112830] bg-gray-600 flex items-center justify-center text-[10px] font-bold overflow-hidden">
                  <img :src="`https://i.pravatar.cc/150?u=inspector${audit.id}${i}`" alt="" />
                </div>
              </div>
            </div>
          </div>
        </div>

        <button class="w-full mt-10 py-4 bg-white/10 hover:bg-white/20 rounded-2xl text-sm font-bold transition-all border border-white/10">
          Voir tout le calendrier
        </button>
      </div>

      <!-- Compliance Documents -->
      <div class="lg:col-span-2 bg-white rounded-[2.5rem] p-8 border border-gray-100 shadow-sm flex flex-col">
        <div class="flex items-center justify-between mb-8">
           <div>
             <h3 class="text-2xl font-bold">Base de Conformité</h3>
             <p class="text-sm text-gray-400 font-medium">Documents et preuves archivés par certificat.</p>
           </div>
           <button class="text-sm font-bold text-[#10b481] flex items-center gap-1">
             <i class="bx bx-plus"></i> Ajouter un document
           </button>
        </div>

        <div class="space-y-3 flex-1 overflow-y-auto max-h-[500px] pr-2 custom-scrollbar">
          <div v-for="doc in documents" :key="doc.name" class="flex items-center gap-4 p-5 rounded-[1.5rem] bg-gray-50 border border-gray-100 hover:border-[#10b481]/30 hover:bg-white transition-all group">
            <div class="w-12 h-12 rounded-2xl bg-white shadow-sm flex items-center justify-center text-2xl text-rose-500">
              <i :class="doc.icon"></i>
            </div>
            <div class="flex-1">
              <h4 class="font-bold text-sm group-hover:text-[#10b481] transition-colors">{{ doc.name }}</h4>
              <p class="text-xs text-gray-400 uppercase tracking-tighter">{{ doc.size }} • Ajouté par {{ doc.user }}</p>
            </div>
            <div class="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
              <button class="w-8 h-8 rounded-lg bg-gray-100 hover:bg-emerald-100 hover:text-emerald-600 flex items-center justify-center transition-colors">
                <i class="bx bx-show"></i>
              </button>
              <button class="w-8 h-8 rounded-lg bg-gray-100 hover:bg-blue-100 hover:text-blue-600 flex items-center justify-center transition-colors">
                <i class="bx bx-download"></i>
              </button>
            </div>
          </div>
        </div>

        <div class="mt-8 pt-6 border-t border-gray-50 flex items-center justify-between">
           <div class="flex items-center gap-2">
             <i class="bx bx-shield-quarter text-2xl text-[#10b481]"></i>
             <span class="text-sm font-bold text-gray-500">Stockage Sécurisé & Chiffré</span>
           </div>
           <p class="text-[10px] text-gray-400 uppercase font-black">Mis à jour il y a 5 min</p>
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
const showAddModal = ref(false);
const isSubmitting = ref(false);

const certifications = ref<any[]>([]);
const certTypes = ref<any[]>([]);
const audits = ref<any[]>([]);
const documents = ref<any[]>([]);

const newCert = ref({
  cert_type: '',
  issued_by: '',
  issued_at: new Date().toISOString().split('T')[0],
  expires_at: '',
  status: 'PENDING'
});

async function fetchData() {
  isLoading.value = true;
  try {
    const [certData, auditData, typeData] = await Promise.all([
      apiFetch('/api/suivi-evaluation/api/certifications/'),
      apiFetch('/api/suivi-evaluation/api/certification-audits/'),
      apiFetch('/api/suivi-evaluation/api/certification-types/')
    ]);
    
    certTypes.value = (typeData as any).results || typeData || [];
    
    certifications.value = ((certData as any).results || certData || []).map((c: any) => ({
      name: c.cert_type?.name || 'Label Bio',
      status: c.status === 'VALID' ? 'Actif' : c.status === 'PENDING' ? 'En cours' : 'Expiré',
      score: c.status === 'VALID' ? 100 : 45,
      expiry: c.expires_at,
      icon: 'bx bx-badge-check',
      statusBg: c.status === 'VALID' ? 'bg-emerald-50' : 'bg-rose-50',
      statusText: c.status === 'VALID' ? 'text-emerald-600' : 'text-rose-600',
      statusBadgeBg: c.status === 'VALID' ? 'bg-emerald-500' : 'bg-rose-500',
      statusBadgeText: 'text-white',
      progressBarBg: c.status === 'VALID' ? 'bg-emerald-500' : 'bg-rose-500'
    }));

    audits.value = ((auditData as any).results || auditData || []).map((a: any) => ({
      id: a.uuid,
      date: new Date(a.date_audit).toLocaleDateString(),
      title: `Audit ${a.cert_type?.name || 'Qualité'}`,
      location: a.auditor || 'Organisme externe'
    }));

    // Placeholder documents for now as backend 'file' handling needs careful integration
    documents.value = [
      { name: 'Manuel des procédures.pdf', size: '2.4 MB', user: 'Admin', icon: 'bx bxs-file-pdf' },
      { name: 'Registre des intrants 2025.pdf', size: '1.8 MB', user: 'Fermier', icon: 'bx bxs-file-pdf' }
    ];

  } catch (err) {
    console.error("Erreur fetchData Certifications:", err);
  } finally {
    isLoading.value = false;
  }
}

async function createCertification() {
  if (!newCert.value.cert_type || !newCert.value.issued_by) {
    alert("Veuillez remplir les informations requises.");
    return;
  }
  isSubmitting.value = true;
  try {
    await apiFetch('/api/suivi-evaluation/api/certifications/', {
      method: 'POST',
      body: newCert.value
    });
    showAddModal.value = false;
    fetchData();
    newCert.value = { cert_type: '', issued_by: '', issued_at: new Date().toISOString().split('T')[0], expires_at: '', status: 'PENDING' };
  } catch (err) {
    console.error("Erreur createCertification:", err);
    alert("Erreur lors de l'envoi de la demande.");
  } finally {
    isSubmitting.value = false;
  }
}

onMounted(() => {
  fetchData();
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
