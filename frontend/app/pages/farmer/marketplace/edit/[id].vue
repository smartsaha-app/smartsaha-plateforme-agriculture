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
                <input v-model="form.name" type="text" class="w-full px-5 py-4 bg-gray-50 border-none rounded-2xl text-sm font-bold text-[#112830] outline-none focus:ring-4 focus:ring-[#10b481]/10 transition-all" />
              </div>
              <div class="space-y-2">
                <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Type de produit</label>
                <select v-model="form.source_type" class="w-full px-5 py-4 bg-gray-50 border-none rounded-2xl text-sm font-bold text-[#112830] outline-none focus:ring-4 focus:ring-[#10b481]/10 transition-all">
                  <option value="HARVEST">Récolte (Mise en vente)</option>
                  <option value="RESALE">Revente</option>
                </select>
              </div>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-6">
              <div class="space-y-2">
                <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">{{ t("price") }} (Ar)</label>
                <input v-model="form.price" type="number" class="w-full px-5 py-4 bg-gray-50 border-none rounded-2xl text-sm font-bold text-[#112830] outline-none focus:ring-4 focus:ring-[#10b481]/10 transition-all" />
              </div>
              <div class="space-y-2">
                <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Stock disponible</label>
                <input v-model="form.stock" type="number" class="w-full px-5 py-4 bg-gray-50 border-none rounded-2xl text-sm font-bold text-[#112830] outline-none focus:ring-4 focus:ring-[#10b481]/10 transition-all" />
              </div>
              <div class="space-y-2">
                <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">{{ t("productUnit") }}</label>
                <input v-model="form.unit" type="text" class="w-full px-5 py-4 bg-gray-50 border-none rounded-2xl text-sm font-bold text-[#112830] outline-none focus:ring-4 focus:ring-[#10b481]/10 transition-all" />
              </div>
            </div>

            <div class="space-y-2">
              <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">{{ t("productDescription") }}</label>
              <textarea v-model="form.description" rows="4" class="w-full px-5 py-4 bg-gray-50 border-none rounded-2xl text-sm font-bold text-[#112830] outline-none resize-none focus:ring-4 focus:ring-[#10b481]/10 transition-all"></textarea>
            </div>
          </div>
        </div>

        <div class="space-y-6">
          <div class="bg-white rounded-3xl border border-gray-100 p-8 shadow-sm">
            <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest block mb-4">Photos du produit</label>
            
            <!-- Existing Images -->
            <div v-if="existingImages.length" class="grid grid-cols-3 gap-2 mb-4">
              <div v-for="img in existingImages" :key="img.id" class="relative aspect-square rounded-xl overflow-hidden border border-gray-100">
                <img :src="img.image" class="w-full h-full object-cover" />
                <button @click="deleteImage(img.id)" class="absolute top-1 right-1 w-6 h-6 bg-rose-500 text-white rounded-lg flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                  <i class="bx bx-x"></i>
                </button>
              </div>
            </div>

            <div 
              @click="$refs.fileInput.click()"
              class="group cursor-pointer border-2 border-dashed border-gray-100 rounded-3xl p-6 text-center hover:border-[#10b481] hover:bg-[#10b481]/5 transition-all"
            >
              <input 
                type="file" 
                ref="fileInput" 
                multiple 
                accept="image/*" 
                class="hidden" 
                @change="handleFiles"
              />
              <div class="w-12 h-12 bg-gray-50 rounded-xl flex items-center justify-center mx-auto mb-2 group-hover:scale-110 transition-transform">
                <i class="bx bx-plus text-2xl text-gray-300 group-hover:text-[#10b481]"></i>
              </div>
              <p class="text-[10px] font-black text-[#112830] uppercase tracking-widest">Ajouter des photos</p>
            </div>

            <!-- New Previews -->
            <div v-if="previews.length" class="grid grid-cols-4 gap-2 mt-4">
              <div v-for="(img, i) in previews" :key="i" class="relative group aspect-square rounded-xl overflow-hidden border border-[#10b481]/20">
                <img :src="img" class="w-full h-full object-cover" />
                <button @click="removeNewImage(i)" class="absolute inset-0 bg-red-500/80 text-white opacity-0 group-hover:opacity-100 flex items-center justify-center transition-opacity">
                  <i class="bx bx-trash text-lg"></i>
                </button>
              </div>
            </div>

            <div class="mt-8 pt-6 border-t border-gray-50">
              <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest mb-4">Statut de l'annonce</p>
              <div class="flex items-center justify-between p-4 bg-gray-50 rounded-2xl">
                <span class="text-sm font-bold text-[#112830]">Active</span>
                <input type="checkbox" v-model="form.is_active" class="toggle-checkbox" />
              </div>
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

const id = route.params.id;
const pending = ref(true);
const submitting = ref(false);
const previews = ref<string[]>([]);
const files = ref<File[]>([]);
const existingImages = ref<any[]>([]);

const form = ref({
  name: '',
  source_type: '',
  price: '',
  stock: '',
  unit: '',
  description: '',
  is_active: true
});

onMounted(async () => {
  try {
    const data: any = await apiFetch(`/api/marketplace/products/${id}/`);
    form.value = {
      name: data.name,
      source_type: data.source_type,
      price: data.price,
      stock: data.stock,
      unit: data.unit,
      description: data.description,
      is_active: data.is_active
    };
    existingImages.value = data.images || [];
  } catch (err) {
    console.error("Erreur chargement produit", err);
    navigateTo('/farmer/marketplace');
  } finally {
    pending.value = false;
  }
});

function handleFiles(event: any) {
  const selectedFiles = Array.from(event.target.files) as File[];
  selectedFiles.forEach(file => {
    files.value.push(file);
    const reader = new FileReader();
    reader.onload = (e) => previews.value.push(e.target?.result as string);
    reader.readAsDataURL(file);
  });
}

function removeNewImage(index: number) {
  files.value.splice(index, 1);
  previews.value.splice(index, 1);
}

async function deleteImage(imageId: number) {
  // Optionnel: API call direct pour supprimer l'image ou juste marquer pour suppression
  // Pour faire simple, on va juste filtrer localement pour cette démo
  existingImages.value = existingImages.value.filter(img => img.id !== imageId);
}

async function handleUpdate() {
  submitting.value = true;
  try {
    const formData = new FormData();
    formData.append('name', form.value.name);
    formData.append('source_type', form.value.source_type);
    formData.append('price', form.value.price);
    formData.append('stock', form.value.stock);
    formData.append('unit', form.value.unit);
    formData.append('description', form.value.description);
    formData.append('is_active', form.value.is_active.toString());
    
    files.value.forEach(file => {
      formData.append('uploaded_images', file);
    });

    await apiFetch(`/api/marketplace/products/${id}/`, {
      method: 'PATCH',
      body: formData
    });
    navigateTo('/farmer/marketplace');
  } catch (err) {
    alert("Erreur lors de la mise à jour");
  } finally {
    submitting.value = false;
  }
}
</script>
