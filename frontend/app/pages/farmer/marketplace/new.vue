<template>
  <ClientOnly>
    <div class="p-1 sm:p-6 mb-10">
      <!-- ===== BREADCRUMB & TITRE ===== -->
      <div class="mb-8">
        <nav class="flex items-center gap-2 text-[10px] font-black uppercase tracking-widest text-gray-400 mb-4">
          <NuxtLink to="/farmer/marketplace" class="hover:text-[#10b481] transition-colors">Marketplace</NuxtLink>
          <i class="bx bx-chevron-right text-base"></i>
          <span class="text-[#10b481]">{{ t("newProduct") }}</span>
        </nav>
        <h2 class="text-3xl font-black text-[#112830] tracking-tight">Ajouter un produit</h2>
        <p class="text-gray-500 font-medium text-sm mt-1">Remplissez les détails pour publier votre article sur le marché.</p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- FORMULAIRE -->
        <div class="lg:col-span-2 space-y-6">
          <div class="bg-white rounded-3xl border border-gray-100 p-8 shadow-sm space-y-6">
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
              <div class="space-y-2">
                <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">{{ t("productName") }}</label>
                <input 
                  v-model="form.title"
                  type="text" 
                  placeholder="Ex: Riz de luxe premium"
                  class="w-full px-5 py-4 bg-gray-50 border-none rounded-2xl text-sm font-bold text-[#112830] focus:ring-4 focus:ring-[#10b481]/10 transition-all outline-none"
                />
              </div>
              <div class="space-y-2">
                <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Type de produit</label>
                <select 
                  v-model="form.post_type"
                  class="w-full px-5 py-4 bg-gray-50 border-none rounded-2xl text-sm font-bold text-[#112830] focus:ring-4 focus:ring-[#10b481]/10 transition-all outline-none"
                >
                  <option value="HARVEST">Récolte (Vente directe)</option>
                  <option value="RESALE">Revente</option>
                  <option value="PURCHASE">Demande d'achat</option>
                </select>
              </div>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-3 gap-6">
              <div class="space-y-2">
                <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">{{ t("price") }} (Ar)</label>
                <input 
                  v-model="form.price"
                  type="number" 
                  class="w-full px-5 py-4 bg-gray-50 border-none rounded-2xl text-sm font-bold text-[#112830] focus:ring-4 focus:ring-[#10b481]/10 transition-all outline-none"
                />
              </div>
              <div class="space-y-2">
                <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">{{ t("quantity") }}</label>
                <input 
                  v-model="form.quantity"
                  type="number" 
                  class="w-full px-5 py-4 bg-gray-50 border-none rounded-2xl text-sm font-bold text-[#112830] focus:ring-4 focus:ring-[#10b481]/10 transition-all outline-none"
                />
              </div>
              <div class="space-y-2">
                <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">{{ t("productUnit") }}</label>
                <input 
                  v-model="form.unit"
                  type="text" 
                  placeholder="kg, tonnes, sacs..."
                  class="w-full px-5 py-4 bg-gray-50 border-none rounded-2xl text-sm font-bold text-[#112830] focus:ring-4 focus:ring-[#10b481]/10 transition-all outline-none"
                />
              </div>
            </div>

            <div class="space-y-2">
              <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">{{ t("productLocation") }} (Ville / Village)</label>
              <div class="relative">
                <i class="bx bx-map absolute left-5 top-1/2 -translate-y-1/2 text-xl text-[#10b481]"></i>
                <input 
                  v-model="form.location"
                  type="text" 
                  class="w-full pl-14 pr-5 py-4 bg-gray-50 border-none rounded-2xl text-sm font-bold text-[#112830] focus:ring-4 focus:ring-[#10b481]/10 transition-all outline-none"
                />
              </div>
            </div>

            <div class="space-y-2">
              <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">{{ t("productDescription") }}</label>
              <textarea 
                v-model="form.description"
                rows="4" 
                class="w-full px-5 py-4 bg-gray-50 border-none rounded-2xl text-sm font-bold text-[#112830] focus:ring-4 focus:ring-[#10b481]/10 transition-all outline-none resize-none"
                placeholder="Décrivez votre produit, sa qualité, les conditions de livraison..."
              ></textarea>
            </div>
          </div>
        </div>

        <!-- UPLOAD IMAGES & ACTIONS -->
        <div class="space-y-6">
          <div class="bg-white rounded-3xl border border-gray-100 p-8 shadow-sm">
            <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1 block mb-4">Photos du produit</label>
            
            <div 
              @click="$refs.fileInput.click()"
              class="group cursor-pointer border-2 border-dashed border-gray-100 rounded-3xl p-8 text-center hover:border-[#10b481] hover:bg-[#10b481]/5 transition-all"
            >
              <input 
                type="file" 
                ref="fileInput" 
                multiple 
                accept="image/*" 
                class="hidden" 
                @change="handleFiles"
              />
              <div class="w-16 h-16 bg-gray-50 rounded-2xl flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform">
                <i class="bx bx-cloud-upload text-3xl text-gray-300 group-hover:text-[#10b481]"></i>
              </div>
              <p class="text-sm font-bold text-[#112830]">Cliquez pour uploader</p>
              <p class="text-[10px] text-gray-400 font-medium mt-1 uppercase tracking-wider">JPG, PNG (Max. 5MB)</p>
            </div>

            <!-- Preview Tiny -->
            <div v-if="previews.length" class="grid grid-cols-4 gap-2 mt-4">
              <div v-for="(img, i) in previews" :key="i" class="relative group aspect-square rounded-xl overflow-hidden border border-gray-100">
                <img :src="img" class="w-full h-full object-cover" />
                <button @click="removeImage(i)" class="absolute inset-0 bg-red-500/80 text-white opacity-0 group-hover:opacity-100 flex items-center justify-center transition-opacity">
                  <i class="bx bx-trash text-lg"></i>
                </button>
              </div>
            </div>
          </div>

          <button 
            @click="handleSubmit"
            :disabled="submitting"
            class="w-full py-5 bg-[#10b481] text-white rounded-2xl font-black text-[12px] uppercase tracking-[0.2em] shadow-xl shadow-[#10b481]/30 hover:-translate-y-1 active:scale-95 transition-all disabled:opacity-50 disabled:translate-y-0"
          >
            <span v-if="submitting">Publication en cours...</span>
            <span v-else>{{ t("saveProduct") }}</span>
          </button>
          
          <button 
            @click="navigateTo('/farmer/marketplace')"
            class="w-full py-5 bg-white text-[#112830] border border-gray-100 rounded-2xl font-black text-[12px] uppercase tracking-[0.2em] hover:bg-gray-50 transition-all"
          >
            Annuler
          </button>
        </div>
      </div>
    </div>
  </ClientOnly>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useApi } from "~/composables/useApi";

definePageMeta({ layout: "dashboard" });

const { t: nuxtT } = useI18n();
const t = (key: string) => nuxtT(`dashboard.${key}`);
const { apiFetch } = useApi();

const submitting = ref(false);
const previews = ref<string[]>([]);
const files = ref<File[]>([]);

const form = ref({
  title: '',
  post_type: 'HARVEST',
  price: '',
  quantity: '',
  unit: '',
  location: '',
  description: ''
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

function removeImage(index: number) {
  files.value.splice(index, 1);
  previews.value.splice(index, 1);
}

async function handleSubmit() {
  if (!form.value.title || !form.value.price) return alert("Veuillez remplir les champs obligatoires");
  
  submitting.value = true;
  try {
    const formData = new FormData();
    formData.append('title', form.value.title);
    formData.append('post_type', form.value.post_type);
    formData.append('price', form.value.price);
    formData.append('quantity', form.value.quantity);
    formData.append('unit', form.value.unit);
    formData.append('location', form.value.location);
    formData.append('description', form.value.description);
    
    files.value.forEach(file => {
      formData.append('uploaded_images', file);
    });

    await apiFetch('/api/marketplace/posts/', {
      method: 'POST',
      body: formData
    });

    navigateTo('/farmer/marketplace');
  } catch (err) {
    console.error("Erreur lors de la création de l'annonce :", err);
    alert("Une erreur est survenue lors de la publication.");
  } finally {
    submitting.value = false;
  }
}
</script>
