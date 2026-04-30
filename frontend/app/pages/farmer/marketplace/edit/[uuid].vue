<template>
  <ClientOnly>
    <div class="p-1 sm:p-6 mb-10">
      <div class="mb-8">
        <nav class="flex items-center gap-2 text-[10px] font-black uppercase tracking-widest text-gray-400 mb-4">
          <NuxtLink to="/farmer/marketplace" class="hover:text-[#10b481] transition-colors">Marketplace</NuxtLink>
          <i class="bx bx-chevron-right text-base"></i>
          <span class="text-[#10b481]">Modifier le produit</span>
        </nav>
        <h2 class="text-3xl font-black text-[#112830] tracking-tight">Modifier votre produit</h2>
        <p class="text-gray-500 font-medium text-sm mt-1">Mettez à jour les informations de votre article.</p>
      </div>

      <div v-if="pending" class="flex items-center justify-center p-20">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-[#10b481]"></div>
      </div>

      <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div class="lg:col-span-2 space-y-6">
          <div class="bg-white rounded-3xl border border-gray-100 p-8 shadow-sm space-y-6">
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
              <div class="space-y-2">
                <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">{{ t("productName") }}</label>
                <input v-model="form.title" type="text" class="w-full px-5 py-4 bg-gray-50 border-none rounded-2xl text-sm font-bold text-[#112830] outline-none" />
              </div>
              <div class="space-y-2">
                <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Type d'annonce</label>
                <select v-model="form.post_type" class="w-full px-5 py-4 bg-gray-50 border-none rounded-2xl text-sm font-bold text-[#112830] outline-none">
                  <option value="HARVEST">Récolte (Mise en vente)</option>
                  <option value="RESALE">Revente</option>
                  <option value="PURCHASE">Achat (Appel d'offre)</option>
                </select>
              </div>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-6">
              <div class="space-y-2">
                <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">{{ t("price") }}</label>
                <input v-model="form.price" type="number" class="w-full px-5 py-4 bg-gray-50 border-none rounded-2xl text-sm font-bold text-[#112830] outline-none" />
              </div>
              <div class="space-y-2">
                <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">{{ t("quantity") }}</label>
                <input v-model="form.quantity" type="number" class="w-full px-5 py-4 bg-gray-50 border-none rounded-2xl text-sm font-bold text-[#112830] outline-none" />
              </div>
              <div class="space-y-2">
                <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">{{ t("productUnit") }}</label>
                <input v-model="form.unit" type="text" class="w-full px-5 py-4 bg-gray-50 border-none rounded-2xl text-sm font-bold text-[#112830] outline-none" />
              </div>
            </div>
            <div class="space-y-2">
              <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">{{ t("productLocation") }}</label>
              <input v-model="form.location" type="text" class="w-full px-5 py-4 bg-gray-50 border-none rounded-2xl text-sm font-bold text-[#112830] outline-none" />
            </div>
            <div class="space-y-2">
              <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">{{ t("productDescription") }}</label>
              <textarea v-model="form.description" rows="4" class="w-full px-5 py-4 bg-gray-50 border-none rounded-2xl text-sm font-bold text-[#112830] outline-none resize-none"></textarea>
            </div>
          </div>
        </div>

        <div class="space-y-6">
          <div class="bg-white rounded-3xl border border-gray-100 p-8 shadow-sm">
            <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest mb-4">Statut de l'annonce</p>
            <div class="flex items-center justify-between p-4 bg-gray-50 rounded-2xl">
              <span class="text-sm font-bold text-[#112830]">Active</span>
              <input type="checkbox" v-model="form.is_active" class="toggle-checkbox" />
            </div>
          </div>

          <button @click="handleUpdate" :disabled="submitting" class="w-full py-5 bg-[#10b481] text-white rounded-2xl font-black text-[12px] uppercase tracking-[0.2em] shadow-xl hover:-translate-y-1 transition-all disabled:opacity-50">
            {{ submitting ? 'Enregistrement...' : 'Mettre à jour' }}
          </button>
          <button @click="navigateTo('/farmer/marketplace')" class="w-full py-5 bg-white text-[#112830] border border-gray-100 rounded-2xl font-black text-[12px] uppercase tracking-[0.2em] hover:bg-gray-50 transition-all">
            Annuler
          </button>
        </div>
      </div>
    </div>
  </ClientOnly>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useApi } from "~/composables/useApi";
import { useRoute } from 'vue-router';

definePageMeta({ layout: "dashboard" });

const route = useRoute();
const { t: nuxtT } = useI18n();
const t = (key: string) => nuxtT(`dashboard.${key}`);
const { apiFetch } = useApi();

const uuid = route.params.uuid;
const pending = ref(true);
const submitting = ref(false);

const form = ref({
  title: '',
  post_type: '',
  price: '',
  quantity: '',
  unit: '',
  location: '',
  description: '',
  is_active: true
});

onMounted(async () => {
  try {
    const data: any = await apiFetch(`/api/marketplace/posts/${uuid}/`);
    form.value = {
      title: data.title,
      post_type: data.post_type,
      price: data.price,
      quantity: data.quantity,
      unit: data.unit,
      location: data.location,
      description: data.description,
      is_active: data.is_active
    };
  } catch (err) {
    console.error("Erreur chargement annonce", err);
    navigateTo('/farmer/marketplace');
  } finally {
    pending.value = false;
  }
});

async function handleUpdate() {
  submitting.value = true;
  try {
    await apiFetch(`/api/marketplace/posts/${uuid}/`, {
      method: 'PATCH',
      body: form.value
    });
    navigateTo('/farmer/marketplace');
  } catch (err) {
    alert("Erreur lors de la mise à jour");
  } finally {
    submitting.value = false;
  }
}
</script>
