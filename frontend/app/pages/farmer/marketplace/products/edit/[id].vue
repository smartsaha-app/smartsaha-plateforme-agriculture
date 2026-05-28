<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8">

    <!-- ===== HEADER ===== -->
    <PageHeader title="Modifier l'annonce">
      <template #subtitle>
        <i class="bx bx-edit"></i>
        Mettez à jour les informations de votre article en vente
      </template>
      <template #breadcrumb>
        <NuxtLink to="/farmer/dashboard" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
          <span>Accueil</span>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <NuxtLink to="/farmer/marketplace/products" class="hover:text-[#10b481] transition-colors">Mes ventes</NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">Modifier</span>
      </template>
    </PageHeader>

    <div v-if="pending" class="flex items-center justify-center p-20">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-[#10b481]"></div>
    </div>

    <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <div class="lg:col-span-2 space-y-6">
        <div class="bg-white rounded-2xl border border-gray-100 p-8 shadow-sm space-y-6">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div class="space-y-2">
              <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Nom du produit</label>
              <input v-model="form.name" type="text" class="w-full px-5 py-4 bg-gray-50 border-none rounded-xl text-sm font-bold text-[#112830] outline-none focus:ring-4 focus:ring-[#10b481]/10 transition-all" />
            </div>
            <div class="space-y-2">
              <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Type de produit</label>
              <select v-model="form.source_type" class="w-full px-5 py-4 bg-gray-50 border-none rounded-xl text-sm font-bold text-[#112830] outline-none focus:ring-4 focus:ring-[#10b481]/10 transition-all">
                <option value="HARVEST">Récolte (Mise en vente)</option>
                <option value="RESALE">Revente</option>
              </select>
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-3 gap-6">
            <div class="space-y-2">
              <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Prix (Ar)</label>
              <input v-model="form.price" type="number" class="w-full px-5 py-4 bg-gray-50 border-none rounded-xl text-sm font-bold text-[#112830] outline-none focus:ring-4 focus:ring-[#10b481]/10 transition-all" />
            </div>
            <div class="space-y-2">
              <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Stock disponible</label>
              <input v-model="form.stock" type="number" class="w-full px-5 py-4 bg-gray-50 border-none rounded-xl text-sm font-bold text-[#112830] outline-none focus:ring-4 focus:ring-[#10b481]/10 transition-all" />
            </div>
            <div class="space-y-2">
              <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Unité</label>
              <input v-model="form.unit" type="text" class="w-full px-5 py-4 bg-gray-50 border-none rounded-xl text-sm font-bold text-[#112830] outline-none focus:ring-4 focus:ring-[#10b481]/10 transition-all" />
            </div>
          </div>

          <div class="space-y-2">
            <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Description</label>
            <textarea v-model="form.description" rows="4" class="w-full px-5 py-4 bg-gray-50 border-none rounded-xl text-sm font-bold text-[#112830] outline-none resize-none focus:ring-4 focus:ring-[#10b481]/10 transition-all"></textarea>
          </div>
        </div>
      </div>

      <div class="space-y-6">
        <div class="bg-white rounded-2xl border border-gray-100 p-8 shadow-sm">
          <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest block mb-4">Photos du produit</label>

          <div v-if="existingImages.length" class="grid grid-cols-3 gap-2 mb-4">
            <div v-for="img in existingImages" :key="img.id" class="relative group aspect-square rounded-xl overflow-hidden border border-gray-100">
              <img :src="img.image" class="w-full h-full object-cover" />
              <button @click="deleteImage(img.id)" class="absolute top-1 right-1 w-6 h-6 bg-rose-500 text-white rounded-lg flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                <i class="bx bx-x"></i>
              </button>
            </div>
          </div>

          <div @click="($refs.fileInput as HTMLInputElement).click()" class="group cursor-pointer border-2 border-dashed border-gray-100 rounded-2xl p-6 text-center hover:border-[#10b481] hover:bg-[#10b481]/5 transition-all">
            <input type="file" ref="fileInput" multiple accept="image/*" class="hidden" @change="handleFiles" />
            <div class="w-10 h-10 bg-gray-50 rounded-xl flex items-center justify-center mx-auto mb-2 group-hover:scale-110 transition-transform">
              <i class="bx bx-plus text-xl text-gray-300 group-hover:text-[#10b481]"></i>
            </div>
            <p class="text-[10px] font-black text-[#112830] uppercase tracking-widest">Ajouter des photos</p>
          </div>

          <div v-if="previews.length" class="grid grid-cols-4 gap-2 mt-4">
            <div v-for="(img, i) in previews" :key="i" class="relative group aspect-square rounded-xl overflow-hidden border border-[#10b481]/20">
              <img :src="img" class="w-full h-full object-cover" />
              <button @click="removeNewImage(i)" class="absolute inset-0 bg-red-500/80 text-white opacity-0 group-hover:opacity-100 flex items-center justify-center transition-opacity">
                <i class="bx bx-trash text-lg"></i>
              </button>
            </div>
          </div>

          <div class="mt-6 pt-6 border-t border-gray-50">
            <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest mb-4">Statut de l'annonce</p>
            <div class="flex items-center justify-between p-4 bg-gray-50 rounded-xl">
              <span class="text-sm font-bold text-[#112830]">{{ form.is_active ? 'Active' : 'Masquée' }}</span>
              <input type="checkbox" v-model="form.is_active" class="w-5 h-5 rounded accent-[#10b481]" />
            </div>
          </div>
        </div>

        <button @click="handleUpdate" :disabled="submitting" class="w-full py-4 bg-[#10b481] text-white rounded-xl font-black text-[12px] uppercase tracking-widest shadow-lg hover:-translate-y-0.5 transition-all disabled:opacity-50">
          {{ submitting ? 'Enregistrement...' : 'Mettre à jour' }}
        </button>
        <NuxtLink to="/farmer/marketplace/products" class="block w-full py-4 bg-white text-[#112830] border border-gray-100 rounded-xl font-black text-[12px] uppercase tracking-widest text-center hover:bg-gray-50 transition-all">
          Annuler
        </NuxtLink>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useApi } from '~/composables/useApi'
import { useRoute } from 'vue-router'

definePageMeta({ layout: 'dashboard' })

const route = useRoute()
const { apiFetch } = useApi()
const id = route.params.id

const pending = ref(true)
const submitting = ref(false)
const previews = ref<string[]>([])
const files = ref<File[]>([])
const existingImages = ref<any[]>([])

const form = ref({
  name: '',
  source_type: '',
  price: '',
  stock: '',
  unit: '',
  description: '',
  is_active: true,
})

onMounted(async () => {
  try {
    const data: any = await apiFetch(`/api/catalogue/products/${id}/`)
    form.value = {
      name: data.name,
      source_type: data.source_type,
      price: data.price,
      stock: data.stock,
      unit: data.unit,
      description: data.description,
      is_active: data.is_active,
    }
    existingImages.value = data.images || []
  } catch (err) {
    console.error('Erreur chargement produit', err)
    navigateTo('/farmer/marketplace/products')
  } finally {
    pending.value = false
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

function removeNewImage(index: number) {
  files.value.splice(index, 1)
  previews.value.splice(index, 1)
}

function deleteImage(imageId: number) {
  existingImages.value = existingImages.value.filter(img => img.id !== imageId)
}

async function handleUpdate() {
  submitting.value = true
  try {
    const formData = new FormData()
    formData.append('name', form.value.name)
    formData.append('source_type', form.value.source_type)
    formData.append('price', form.value.price)
    formData.append('stock', form.value.stock)
    formData.append('unit', form.value.unit)
    formData.append('description', form.value.description)
    formData.append('is_active', form.value.is_active.toString())
    files.value.forEach(file => formData.append('uploaded_images', file))

    await apiFetch(`/api/catalogue/products/${id}/`, { method: 'PATCH', body: formData })
    navigateTo('/farmer/marketplace/products')
  } catch (err) {
    alert('Erreur lors de la mise à jour')
  } finally {
    submitting.value = false
  }
}
</script>