<template>
  <div class="p-1 sm:p-6 mb-10">
    <!-- Header -->
    <div class="mb-8">
      <nav class="flex items-center gap-2 text-[10px] font-black uppercase tracking-widest text-gray-400 mb-4">
        <NuxtLink to="/seller/products" class="hover:text-[#10b481] transition-colors">Mes Produits</NuxtLink>
        <i class="bx bx-chevron-right text-base"></i>
        <span class="text-[#10b481]">Nouveau Produit</span>
      </nav>
      <h2 class="text-3xl font-black text-[#112830] tracking-tight">Vendre un nouveau produit</h2>
      <p class="text-gray-500 font-medium text-sm mt-1">Remplissez les informations ci-dessous pour mettre votre produit en vente.</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-10">
      <!-- Form Section -->
      <div class="lg:col-span-2 space-y-6">
        <div class="bg-white rounded-[2.5rem] border border-gray-50 p-10 shadow-sm space-y-8">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div class="space-y-2">
              <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Nom du produit</label>
              <input v-model="form.name" type="text" placeholder="Ex: Sac d'engrais organique" class="w-full px-6 py-4 bg-gray-50 border-none rounded-2xl text-sm font-bold text-[#112830] focus:ring-4 focus:ring-[#10b481]/10 transition-all outline-none">
            </div>
            <div class="space-y-2">
              <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Catégorie</label>
              <select v-model="form.category" class="w-full px-6 py-4 bg-gray-50 border-none rounded-2xl text-sm font-bold text-[#112830] focus:ring-4 focus:ring-[#10b481]/10 transition-all outline-none">
                <option :value="null">Sélectionner une catégorie</option>
                <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
              </select>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div class="space-y-2">
              <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Prix de vente (Ar)</label>
              <input v-model="form.price" type="number" class="w-full px-6 py-4 bg-gray-50 border-none rounded-2xl text-sm font-bold text-[#112830] focus:ring-4 focus:ring-[#10b481]/10 transition-all outline-none">
            </div>
            <div class="space-y-2">
              <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Quantité en stock</label>
              <input v-model="form.stock" type="number" class="w-full px-6 py-4 bg-gray-50 border-none rounded-2xl text-sm font-bold text-[#112830] focus:ring-4 focus:ring-[#10b481]/10 transition-all outline-none">
            </div>
            <div class="space-y-2">
              <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Unité</label>
              <input v-model="form.unit" type="text" placeholder="Pcs, Sacs, Litres..." class="w-full px-6 py-4 bg-gray-50 border-none rounded-2xl text-sm font-bold text-[#112830] focus:ring-4 focus:ring-[#10b481]/10 transition-all outline-none">
            </div>
          </div>

          <div class="space-y-2">
            <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Description détaillée</label>
            <textarea v-model="form.description" rows="5" class="w-full px-6 py-4 bg-gray-50 border-none rounded-2xl text-sm font-bold text-[#112830] focus:ring-4 focus:ring-[#10b481]/10 transition-all outline-none resize-none" placeholder="Donnez plus de détails sur votre produit pour attirer les acheteurs..."></textarea>
          </div>
        </div>
      </div>

      <!-- Actions & Media Section -->
      <div class="space-y-6">
        <div class="bg-white rounded-[2.5rem] border border-gray-50 p-8 shadow-sm">
          <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1 block mb-4">Photos du produit</label>
          
          <div @click="$refs.fileInput.click()" class="group cursor-pointer border-2 border-dashed border-gray-100 rounded-3xl p-8 text-center hover:border-[#10b481] hover:bg-[#10b481]/5 transition-all">
            <input type="file" ref="fileInput" multiple accept="image/*" class="hidden" @change="handleFiles" />
            <div class="w-16 h-16 bg-gray-50 rounded-2xl flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform">
              <i class="bx bx-cloud-upload text-3xl text-gray-300 group-hover:text-[#10b481]"></i>
            </div>
            <p class="text-sm font-black text-[#112830]">Choisir des fichiers</p>
            <p class="text-[10px] text-gray-400 font-bold mt-1 uppercase tracking-wider">PNG ou JPG jusqu'à 5MB</p>
          </div>

          <div v-if="previews.length" class="grid grid-cols-3 gap-2 mt-6">
            <div v-for="(img, i) in previews" :key="i" class="relative group aspect-square rounded-xl overflow-hidden border border-gray-100 shadow-sm">
              <img :src="img" class="w-full h-full object-cover" />
              <button @click="removeImage(i)" class="absolute inset-0 bg-rose-500/80 text-white opacity-0 group-hover:opacity-100 flex items-center justify-center transition-opacity">
                <i class="bx bx-trash text-xl"></i>
              </button>
            </div>
          </div>
        </div>

        <div class="p-2 space-y-4">
          <button @click="handleSubmit" :disabled="submitting" class="w-full py-5 bg-[#10b481] text-white rounded-2xl font-black text-xs uppercase tracking-widest shadow-xl shadow-[#10b481]/20 hover:-translate-y-1 active:scale-95 transition-all flex items-center justify-center gap-3">
            <i v-if="submitting" class="bx bx-loader-alt animate-spin text-xl"></i>
            Publier mon produit
          </button>
          <button @click="navigateTo('/seller/products')" class="w-full py-5 bg-white text-[#112830] border border-gray-100 rounded-2xl font-black text-xs uppercase tracking-widest hover:bg-gray-50 transition-all">
            Annuler
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';

definePageMeta({
  layout: 'dashboard'
});

const { apiFetch } = useApi();

const submitting = ref(false);
const categories = ref<any[]>([]);
const previews = ref<string[]>([]);
const files = ref<File[]>([]);

const form = ref({
  name: '',
  price: '',
  stock: '',
  unit: '',
  category: null,
  description: '',
  source_type: 'RESALE'
});

onMounted(async () => {
  try {
    const res = await apiFetch('/api/catalogue/categories/');
    categories.value = res.results || res;
  } catch (err) {
    console.error("Failed to load categories", err);
  }
});

const handleFiles = (event: any) => {
  const selectedFiles = Array.from(event.target.files) as File[];
  selectedFiles.forEach(file => {
    files.value.push(file);
    const reader = new FileReader();
    reader.onload = (e) => previews.value.push(e.target?.result as string);
    reader.readAsDataURL(file);
  });
};

const removeImage = (index: number) => {
  files.value.splice(index, 1);
  previews.value.splice(index, 1);
};

const handleSubmit = async () => {
  if (!form.value.name || !form.value.price) {
    alert("Veuillez remplir les informations essentielles.");
    return;
  }

  submitting.value = true;
  try {
    const formData = new FormData();
    Object.entries(form.value).forEach(([key, value]) => {
      if (value !== null) formData.append(key, value.toString());
    });
    
    files.value.forEach(file => {
      formData.append('uploaded_images', file);
    });

    await apiFetch('/api/catalogue/products/', {
      method: 'POST',
      body: formData
    });

    navigateTo('/seller/products');
  } catch (err) {
    console.error("Failed to create product", err);
    alert("Erreur lors de la création du produit.");
  } finally {
    submitting.value = false;
  }
};
</script>
