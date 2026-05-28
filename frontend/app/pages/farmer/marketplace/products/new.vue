<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8">

    <!-- ===== HEADER ===== -->
    <PageHeader title="Mettre en vente">
      <template #subtitle>
        <i class="bx bx-plus-circle"></i>
        Publiez un produit agricole sur le marketplace SmartSaha
      </template>
      <template #breadcrumb>
        <NuxtLink to="/farmer/dashboard" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
          <span>Accueil</span>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <NuxtLink to="/farmer/marketplace/products" class="hover:text-[#10b481] transition-colors">Mes ventes</NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">Nouvelle annonce</span>
      </template>
    </PageHeader>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- FORMULAIRE -->
      <div class="lg:col-span-2 space-y-6">
        <div class="bg-white rounded-2xl border border-gray-100 p-8 shadow-sm space-y-6">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div class="space-y-2">
              <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Nom du produit</label>
              <input
                v-model="form.name"
                type="text"
                placeholder="Ex: Riz Tsipala – Récolte 2025"
                class="w-full px-5 py-4 bg-gray-50 border-none rounded-xl text-sm font-bold text-[#112830] focus:ring-4 focus:ring-[#10b481]/10 transition-all outline-none"
              />
            </div>
            <div class="space-y-2">
              <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Type de produit</label>
              <select v-model="form.source_type" class="w-full px-5 py-4 bg-gray-50 border-none rounded-xl text-sm font-bold text-[#112830] focus:ring-4 focus:ring-[#10b481]/10 transition-all outline-none">
                <option value="HARVEST">Récolte (Vente directe)</option>
                <option value="RESALE">Revente</option>
              </select>
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-3 gap-6">
            <div class="space-y-2">
              <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Prix de vente (Ar)</label>
              <input v-model="form.price" type="number" placeholder="0" class="w-full px-5 py-4 bg-gray-50 border-none rounded-xl text-sm font-bold text-[#112830] focus:ring-4 focus:ring-[#10b481]/10 transition-all outline-none" />
            </div>
            <div class="space-y-2">
              <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Quantité disponible</label>
              <input v-model="form.stock" type="number" placeholder="0" class="w-full px-5 py-4 bg-gray-50 border-none rounded-xl text-sm font-bold text-[#112830] focus:ring-4 focus:ring-[#10b481]/10 transition-all outline-none" />
            </div>
            <div class="space-y-2">
              <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Unité</label>
              <input v-model="form.unit" type="text" placeholder="kg, sacs, tonnes..." class="w-full px-5 py-4 bg-gray-50 border-none rounded-xl text-sm font-bold text-[#112830] focus:ring-4 focus:ring-[#10b481]/10 transition-all outline-none" />
            </div>
          </div>

          <div class="space-y-2">
            <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Catégorie</label>
            <select v-model="form.category" class="w-full px-5 py-4 bg-gray-50 border-none rounded-xl text-sm font-bold text-[#112830] focus:ring-4 focus:ring-[#10b481]/10 transition-all outline-none">
              <option :value="null">Choisir une catégorie</option>
              <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
            </select>
          </div>

          <div class="space-y-2">
            <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Description</label>
            <textarea
              v-model="form.description"
              rows="4"
              class="w-full px-5 py-4 bg-gray-50 border-none rounded-xl text-sm font-bold text-[#112830] focus:ring-4 focus:ring-[#10b481]/10 transition-all outline-none resize-none"
              placeholder="Décrivez votre produit : origine, qualité, conditions de livraison..."
            ></textarea>
          </div>
        </div>
      </div>

      <!-- UPLOAD & ACTIONS -->
      <div class="space-y-6">
        <div class="bg-white rounded-2xl border border-gray-100 p-8 shadow-sm">
          <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1 block mb-4">Photos du produit</label>

          <div @click="($refs.fileInput as HTMLInputElement).click()" class="group cursor-pointer border-2 border-dashed border-gray-100 rounded-2xl p-8 text-center hover:border-[#10b481] hover:bg-[#10b481]/5 transition-all">
            <input type="file" ref="fileInput" multiple accept="image/*" class="hidden" @change="handleFiles" />
            <div class="w-14 h-14 bg-gray-50 rounded-xl flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform">
              <i class="bx bx-cloud-upload text-2xl text-gray-300 group-hover:text-[#10b481]"></i>
            </div>
            <p class="text-sm font-bold text-[#112830]">Cliquez pour uploader</p>
            <p class="text-[10px] text-gray-400 font-medium mt-1 uppercase tracking-wider">JPG, PNG (Max. 5MB)</p>
          </div>

          <div v-if="previews.length" class="grid grid-cols-4 gap-2 mt-4">
            <div v-for="(img, i) in previews" :key="i" class="relative group aspect-square rounded-xl overflow-hidden border border-gray-100">
              <img :src="img" class="w-full h-full object-cover" />
              <button @click="removeImage(i)" class="absolute inset-0 bg-red-500/80 text-white opacity-0 group-hover:opacity-100 flex items-center justify-center transition-opacity">
                <i class="bx bx-trash text-lg"></i>
              </button>
            </div>
          </div>
        </div>

        <!-- Tip -->
        <div class="bg-emerald-50 rounded-2xl border border-emerald-100 p-5 flex gap-3">
          <i class="bx bx-bulb text-emerald-500 text-xl flex-shrink-0 mt-0.5"></i>
          <p class="text-[13px] text-emerald-700 leading-relaxed">Ajoutez des photos de qualité et une description détaillée pour attirer plus d'acheteurs.</p>
        </div>

        <button
          @click="handleSubmit"
          :disabled="submitting"
          class="w-full py-4 bg-[#10b481] text-white rounded-xl font-black text-[12px] uppercase tracking-widest shadow-lg hover:-translate-y-0.5 transition-all disabled:opacity-50"
        >
          <span v-if="submitting">Publication en cours...</span>
          <span v-else>Publier l'annonce</span>
        </button>

        <NuxtLink
          to="/farmer/marketplace/products"
          class="block w-full py-4 bg-white text-[#112830] border border-gray-100 rounded-xl font-black text-[12px] uppercase tracking-widest text-center hover:bg-gray-50 transition-all"
        >
          Annuler
        </NuxtLink>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useApi } from '~/composables/useApi'

definePageMeta({ layout: 'dashboard' })

const { apiFetch } = useApi()

const submitting = ref(false)
const categories = ref<any[]>([])
const previews = ref<string[]>([])
const files = ref<File[]>([])

const form = ref({
  name: '',
  source_type: 'HARVEST',
  price: '',
  stock: '',
  unit: '',
  category: null as number | null,
  description: '',
})

onMounted(async () => {
  try {
    const res = await apiFetch('/api/catalogue/categories/')
    categories.value = res.results || res
  } catch (err) {
    console.error('Erreur chargement catégories', err)
  }
})

function handleFiles(event: any) {
  const selectedFiles = Array.from(event.target.files) as File[]
  selectedFiles.forEach(file => {
    files.value.push(file)
    const reader = new FileReader()
    reader.onload = (e) => previews.value.push(e.target?.result as string)
    reader.readAsDataURL(file)
  })
}

function removeImage(index: number) {
  files.value.splice(index, 1)
  previews.value.splice(index, 1)
}

async function handleSubmit() {
  if (!form.value.name || !form.value.price) return alert('Veuillez remplir les champs obligatoires')

  submitting.value = true
  try {
    const formData = new FormData()
    formData.append('name', form.value.name)
    formData.append('source_type', form.value.source_type)
    formData.append('price', form.value.price)
    formData.append('stock', form.value.stock)
    formData.append('unit', form.value.unit)
    if (form.value.category) formData.append('category', form.value.category.toString())
    formData.append('description', form.value.description)
    files.value.forEach(file => formData.append('uploaded_images', file))

    await apiFetch('/api/catalogue/products/', { method: 'POST', body: formData })
    navigateTo('/farmer/marketplace/products')
  } catch (err) {
    console.error('Erreur création produit', err)
    alert("Une erreur est survenue lors de la publication.")
  } finally {
    submitting.value = false
  }
}
</script>