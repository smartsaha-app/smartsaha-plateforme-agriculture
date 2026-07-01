<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8 space-y-6">

    <!-- HEADER -->
    <PageHeader title="Base de connaissances Sesily">
      <template #subtitle>
        <i class="bx bx-brain"></i>
        Enrichissez le contexte de Sesily AI sans toucher au code
      </template>
      <template #breadcrumb>
        <NuxtLink to="/admin" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
          <span>Tableau de bord</span>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">Base de connaissances</span>
      </template>
    </PageHeader>

    <!-- STATS -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div v-for="stat in statsCards" :key="stat.label"
        class="bg-white rounded-2xl border border-gray-100 shadow-sm p-5 flex items-center gap-4">
        <div :class="['w-11 h-11 rounded-xl flex items-center justify-center flex-shrink-0', stat.bg]">
          <i :class="['text-xl', stat.icon, stat.color]"></i>
        </div>
        <div>
          <p class="text-2xl font-black text-[#112830]">{{ stat.value }}</p>
          <p class="text-[10px] font-bold text-gray-400 uppercase tracking-widest">{{ stat.label }}</p>
        </div>
      </div>
    </div>

    <!-- FILTRES -->
    <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-4 flex flex-wrap gap-3 items-center">
      <div class="relative flex-1 min-w-[200px]">
        <i class="bx bx-search absolute left-3 top-1/2 -translate-y-1/2 text-gray-300"></i>
        <input v-model="search" placeholder="Rechercher par titre ou contenu…"
          class="w-full pl-9 pr-4 py-2.5 bg-gray-50 border border-gray-100 rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/30" />
      </div>
      <select v-model="filterCategory"
        class="px-3 py-2.5 bg-gray-50 border border-gray-100 rounded-xl text-sm font-medium outline-none focus:ring-2 focus:ring-[#10b481]/20">
        <option value="">Toutes les catégories</option>
        <option v-for="c in CATEGORIES" :key="c.value" :value="c.value">{{ c.label }}</option>
      </select>
      <select v-model="filterStatus"
        class="px-3 py-2.5 bg-gray-50 border border-gray-100 rounded-xl text-sm font-medium outline-none focus:ring-2 focus:ring-[#10b481]/20">
        <option value="">Tous les statuts</option>
        <option value="PUBLISHED">Publié</option>
        <option value="DRAFT">Brouillon</option>
      </select>
      <div class="ml-auto flex items-center gap-2 flex-shrink-0">
        <button @click="showImportModal = true"
          class="flex items-center gap-2 px-4 py-2.5 bg-white border border-gray-200 text-[#112830] rounded-xl text-sm font-bold hover:bg-gray-50 transition-all">
          <i class="bx bx-upload text-base"></i>
          Importer
        </button>
        <button @click="openCreate"
          class="flex items-center gap-2 px-4 py-2.5 bg-[#112830] text-white rounded-xl text-sm font-bold hover:bg-[#10b481] transition-all">
          <i class="bx bx-plus text-base"></i>
          Nouvelle entrée
        </button>
      </div>
    </div>

    <!-- LISTE DES ENTRÉES -->
    <div v-if="isLoading" class="flex justify-center py-16">
      <div class="w-8 h-8 border-4 border-[#10b481] border-t-transparent rounded-full animate-spin"></div>
    </div>

    <div v-else-if="entries.length === 0"
      class="bg-white rounded-2xl border border-gray-100 shadow-sm p-12 text-center">
      <div class="w-16 h-16 bg-gray-50 rounded-2xl flex items-center justify-center mx-auto mb-4">
        <i class="bx bx-book-open text-3xl text-gray-300"></i>
      </div>
      <p class="text-sm font-bold text-gray-400">Aucune entrée trouvée</p>
      <p class="text-xs text-gray-300 mt-1">Ajoutez votre première entrée de connaissance pour enrichir Sesily</p>
    </div>

    <div v-else class="space-y-3">
      <div v-for="entry in entries" :key="entry.id"
        class="bg-white rounded-2xl border border-gray-100 shadow-sm p-5 flex items-start gap-4 hover:border-gray-200 transition-all">

        <!-- Icône catégorie -->
        <div :class="['w-11 h-11 rounded-xl flex items-center justify-center flex-shrink-0 text-lg', categoryStyle(entry.category).bg]">
          {{ categoryStyle(entry.category).emoji }}
        </div>

        <!-- Contenu -->
        <div class="flex-1 min-w-0">
          <div class="flex items-start justify-between gap-3 flex-wrap">
            <div>
              <h3 class="text-sm font-black text-[#112830]">{{ entry.title }}</h3>
              <div class="flex flex-wrap items-center gap-2 mt-1">
                <span :class="['text-[9px] font-black px-2 py-0.5 rounded-full uppercase tracking-widest', categoryStyle(entry.category).badge]">
                  {{ entry.category_label }}
                </span>
                <span v-if="entry.region" class="text-[9px] font-bold text-gray-400 flex items-center gap-1">
                  <i class="bx bx-map-pin"></i> {{ entry.region }}
                </span>
                <span v-if="entry.crops?.length" class="text-[9px] font-bold text-emerald-600 flex items-center gap-1">
                  <i class="bx bx-leaf"></i> {{ entry.crops.join(', ') }}
                </span>
              </div>
            </div>
            <div class="flex items-center gap-2 flex-shrink-0">
              <!-- Statut toggle -->
              <button @click="toggleStatus(entry)"
                :class="['text-[9px] font-black px-2.5 py-1 rounded-full uppercase tracking-widest transition-all',
                  entry.status === 'PUBLISHED'
                    ? 'bg-emerald-100 text-emerald-700 hover:bg-rose-100 hover:text-rose-700'
                    : 'bg-amber-100 text-amber-700 hover:bg-emerald-100 hover:text-emerald-700']">
                {{ entry.status === 'PUBLISHED' ? '✅ Publié' : '⏸ Brouillon' }}
              </button>
              <button @click="openEdit(entry)" class="w-8 h-8 rounded-lg bg-gray-50 hover:bg-blue-50 hover:text-blue-600 flex items-center justify-center transition-all">
                <i class="bx bx-edit text-sm"></i>
              </button>
              <button @click="confirmDelete(entry)" class="w-8 h-8 rounded-lg bg-gray-50 hover:bg-rose-50 hover:text-rose-600 flex items-center justify-center transition-all">
                <i class="bx bx-trash text-sm"></i>
              </button>
            </div>
          </div>
          <p class="text-xs text-gray-400 mt-2 line-clamp-2">{{ entry.content.slice(0, 180) }}{{ entry.content.length > 180 ? '…' : '' }}</p>
          <p class="text-[10px] text-gray-300 mt-1.5">Mis à jour {{ formatDate(entry.updated_at) }} {{ entry.created_by ? `· par ${entry.created_by}` : '' }}</p>
        </div>
      </div>
    </div>

    <!-- ═══════════════════════════════════════════════════════════════════════
         MODAL IMPORT SOURCE
    ════════════════════════════════════════════════════════════════════════ -->
    <Transition name="pop-modal">
      <div v-if="showImportModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm">
        <div class="bg-white rounded-2xl shadow-2xl w-full max-w-xl">

          <!-- En-tête -->
          <div class="p-6 border-b border-gray-100 flex items-center justify-between">
            <div>
              <h2 class="text-base font-black text-[#112830]">Importer une source de données</h2>
              <p class="text-xs text-gray-400 mt-0.5">Sesily AI structurera automatiquement le contenu en entrées</p>
            </div>
            <button @click="closeImportModal" class="w-8 h-8 rounded-lg bg-gray-100 hover:bg-gray-200 flex items-center justify-center">
              <i class="bx bx-x text-lg"></i>
            </button>
          </div>

          <div class="p-6 space-y-5">
            <!-- Sélecteur de type -->
            <div>
              <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest mb-2">Type de source</p>
              <div class="grid grid-cols-3 gap-2">
                <button v-for="t in SOURCE_TYPES" :key="t.type" @click="importType = t.type"
                  :class="['p-3 rounded-xl border-2 text-center transition-all cursor-pointer',
                    importType === t.type
                      ? 'border-[#10b481] bg-emerald-50'
                      : 'border-gray-100 hover:border-gray-200 bg-gray-50']">
                  <span class="text-xl block leading-none">{{ t.emoji }}</span>
                  <span class="text-[10px] font-black text-[#112830] mt-1.5 block">{{ t.label }}</span>
                </button>
              </div>
            </div>

            <!-- Champ selon le type -->
            <!-- Fichier (PDF / Excel / Word / Image) -->
            <div v-if="['pdf','excel','docx','image'].includes(importType)" class="space-y-2">
              <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest">
                Fichier {{ currentSourceType?.label }}
              </label>
              <div
                @dragover.prevent @drop.prevent="onFileDrop"
                :class="['border-2 border-dashed rounded-xl p-6 text-center transition-all cursor-pointer',
                  importFile ? 'border-[#10b481] bg-emerald-50' : 'border-gray-200 hover:border-gray-300 bg-gray-50']"
                @click="() => (fileInputRef as HTMLInputElement)?.click()">
                <div v-if="importFile" class="flex items-center justify-center gap-3">
                  <i class="bx bx-file text-2xl text-[#10b481]"></i>
                  <div class="text-left">
                    <p class="text-sm font-bold text-[#112830]">{{ importFile.name }}</p>
                    <p class="text-xs text-gray-400">{{ formatFileSize(importFile.size) }}</p>
                  </div>
                  <button @click.stop="importFile = null" class="ml-2 w-6 h-6 rounded-full bg-gray-200 hover:bg-rose-100 hover:text-rose-600 flex items-center justify-center">
                    <i class="bx bx-x text-sm"></i>
                  </button>
                </div>
                <div v-else>
                  <i class="bx bx-cloud-upload text-3xl text-gray-300 mb-2 block"></i>
                  <p class="text-sm text-gray-400 font-medium">Glissez votre fichier ou cliquez pour parcourir</p>
                  <p class="text-[10px] text-gray-300 mt-1">{{ currentSourceType?.accept?.split(',').join(' · ') }}</p>
                </div>
                <input ref="fileInputRef" type="file" :accept="currentSourceType?.accept ?? ''" class="hidden" @change="onFileChange" />
              </div>
            </div>

            <!-- URL -->
            <div v-else-if="importType === 'url'" class="space-y-1.5">
              <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest">URL de la page web</label>
              <div class="relative">
                <i class="bx bx-link absolute left-3 top-1/2 -translate-y-1/2 text-gray-300"></i>
                <input v-model="importUrl" placeholder="https://exemple.mg/page-agricole"
                  class="w-full pl-9 pr-4 py-2.5 bg-gray-50 border border-gray-100 rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/30" />
              </div>
            </div>

            <!-- Texte brut -->
            <div v-else-if="importType === 'text'" class="space-y-1.5">
              <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest">Texte à analyser</label>
              <textarea v-model="importText" rows="8"
                placeholder="Collez ici votre texte agricole (rapport, fiche technique, notes de terrain…)"
                class="w-full px-4 py-3 bg-gray-50 border border-gray-100 rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/30 resize-none"></textarea>
            </div>
          </div>

          <!-- Pied -->
          <div class="p-6 border-t border-gray-100 flex gap-3 justify-end">
            <button @click="closeImportModal" class="px-5 py-2.5 rounded-xl text-sm font-bold text-gray-500 hover:bg-gray-100 transition-all">
              Annuler
            </button>
            <button @click="analyzeSource" :disabled="isAnalyzing || !canAnalyze"
              class="px-5 py-2.5 bg-[#10b481] text-white rounded-xl text-sm font-bold hover:bg-[#0d9e70] transition-all flex items-center gap-2 disabled:opacity-40">
              <div v-if="isAnalyzing" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              <i v-else class="bx bx-brain text-base"></i>
              {{ isAnalyzing ? 'Analyse en cours…' : 'Analyser avec Sesily AI' }}
            </button>
          </div>
        </div>
      </div>
    </Transition>

    <!-- ═══════════════════════════════════════════════════════════════════════
         MODAL PRÉVISUALISATION — entrées extraites
    ════════════════════════════════════════════════════════════════════════ -->
    <Transition name="pop-modal">
      <div v-if="showPreviewModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm">
        <div class="bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] flex flex-col">

          <!-- En-tête -->
          <div class="p-6 border-b border-gray-100 flex items-center justify-between flex-shrink-0">
            <div>
              <h2 class="text-base font-black text-[#112830]">
                {{ proposedEntries.length }} entrée(s) extraite(s)
              </h2>
              <p class="text-xs text-gray-400 mt-0.5">
                {{ proposedEntries.filter(e => e.selected).length }} sélectionnée(s) — décochez celles à ignorer
              </p>
            </div>
            <button @click="showPreviewModal = false" class="w-8 h-8 rounded-lg bg-gray-100 hover:bg-gray-200 flex items-center justify-center">
              <i class="bx bx-x text-lg"></i>
            </button>
          </div>

          <!-- Liste des entrées -->
          <div class="overflow-y-auto flex-1 p-4 space-y-2">
            <div v-for="(entry, idx) in proposedEntries" :key="idx"
              :class="['rounded-xl border-2 transition-all',
                entry.selected ? 'border-[#10b481]/30 bg-emerald-50/30' : 'border-gray-100 bg-white opacity-60']">

              <!-- Ligne principale -->
              <div class="p-3 flex items-start gap-3">
                <input type="checkbox" v-model="entry.selected" class="mt-0.5 w-4 h-4 accent-[#10b481] flex-shrink-0" />
                <div :class="['w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0 text-base', categoryStyle(entry.category).bg]">
                  {{ categoryStyle(entry.category).emoji }}
                </div>
                <div class="flex-1 min-w-0">
                  <input v-model="entry.title"
                    class="w-full text-sm font-black text-[#112830] bg-transparent outline-none border-b border-transparent hover:border-gray-200 focus:border-[#10b481] py-0.5 transition-all"
                    placeholder="Titre de l'entrée" />
                  <div class="flex flex-wrap items-center gap-1.5 mt-1">
                    <span :class="['text-[9px] font-black px-2 py-0.5 rounded-full uppercase tracking-widest', categoryStyle(entry.category).badge]">
                      {{ entry.category }}
                    </span>
                    <span class="text-[9px] font-bold text-gray-400 bg-gray-100 px-2 py-0.5 rounded-full">{{ entry.language }}</span>
                    <span v-if="entry.region" class="text-[9px] font-bold text-gray-400 flex items-center gap-1">
                      <i class="bx bx-map-pin"></i> {{ entry.region }}
                    </span>
                    <span v-if="entry.crops?.length" class="text-[9px] font-bold text-emerald-600 flex items-center gap-1">
                      <i class="bx bx-leaf"></i> {{ entry.crops.join(', ') }}
                    </span>
                  </div>
                </div>
                <button @click="entry.expanded = !entry.expanded"
                  class="w-7 h-7 rounded-lg bg-gray-100 hover:bg-gray-200 flex items-center justify-center flex-shrink-0 transition-all">
                  <i :class="['bx text-sm transition-transform', entry.expanded ? 'bx-chevron-up' : 'bx-chevron-down']"></i>
                </button>
              </div>

              <!-- Contenu expandable -->
              <div v-if="entry.expanded" class="px-3 pb-3 pl-[52px]">
                <textarea v-model="entry.content" rows="6"
                  class="w-full px-3 py-2 bg-white border border-gray-100 rounded-xl text-xs font-mono outline-none focus:ring-2 focus:ring-[#10b481]/20 resize-none"></textarea>
              </div>
            </div>
          </div>

          <!-- Pied -->
          <div class="p-6 border-t border-gray-100 flex-shrink-0">
            <div class="flex items-center gap-3 p-3 bg-amber-50 border border-amber-100 rounded-xl mb-4">
              <input type="checkbox" id="publish-import-check" v-model="publishImport" class="w-4 h-4 accent-[#10b481]" />
              <label for="publish-import-check" class="text-xs font-bold text-amber-800 cursor-pointer">
                Publier immédiatement (disponible pour Sesily dès l'import)
              </label>
            </div>
            <div class="flex gap-3 justify-between">
              <button @click="showImportModal = true; showPreviewModal = false"
                class="px-4 py-2.5 rounded-xl text-sm font-bold text-gray-500 hover:bg-gray-100 transition-all flex items-center gap-2">
                <i class="bx bx-arrow-back"></i> Retour
              </button>
              <button @click="confirmImport"
                :disabled="isImporting || proposedEntries.filter(e => e.selected).length === 0"
                class="px-5 py-2.5 bg-[#112830] text-white rounded-xl text-sm font-bold hover:bg-[#10b481] transition-all flex items-center gap-2 disabled:opacity-40">
                <div v-if="isImporting" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                <i v-else class="bx bx-check-double text-base"></i>
                Importer {{ proposedEntries.filter(e => e.selected).length }} entrée(s)
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <!-- MODAL CRÉER / MODIFIER -->
    <Transition name="pop-modal">
      <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm">
        <div class="bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
          <div class="p-6 border-b border-gray-100 flex items-center justify-between">
            <div>
              <h2 class="text-base font-black text-[#112830]">
                {{ editingEntry ? 'Modifier l\'entrée' : 'Nouvelle entrée de connaissance' }}
              </h2>
              <p class="text-xs text-gray-400 mt-0.5">Ce contenu enrichira le contexte de Sesily lors des conversations</p>
            </div>
            <button @click="closeModal" class="w-8 h-8 rounded-lg bg-gray-100 hover:bg-gray-200 flex items-center justify-center">
              <i class="bx bx-x text-lg"></i>
            </button>
          </div>

          <div class="p-6 space-y-4">
            <!-- Titre -->
            <div class="space-y-1.5">
              <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest">Titre *</label>
              <input v-model="form.title" placeholder="Ex: Pyriculariose du riz — traitement local"
                class="w-full px-4 py-2.5 bg-gray-50 border border-gray-100 rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/30" />
            </div>

            <!-- Catégorie + Langue -->
            <div class="grid grid-cols-2 gap-3">
              <div class="space-y-1.5">
                <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest">Catégorie *</label>
                <select v-model="form.category"
                  class="w-full px-3 py-2.5 bg-gray-50 border border-gray-100 rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#10b481]/20">
                  <option v-for="c in CATEGORIES" :key="c.value" :value="c.value">{{ c.label }}</option>
                </select>
              </div>
              <div class="space-y-1.5">
                <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest">Langue</label>
                <select v-model="form.language"
                  class="w-full px-3 py-2.5 bg-gray-50 border border-gray-100 rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#10b481]/20">
                  <option value="fr">Français</option>
                  <option value="en">English</option>
                  <option value="mg">Malagasy</option>
                </select>
              </div>
            </div>

            <!-- Cultures + Région -->
            <div class="grid grid-cols-2 gap-3">
              <div class="space-y-1.5">
                <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest">Cultures concernées</label>
                <input v-model="cropsInput" placeholder="riz, maïs, manioc (séparés par virgule)"
                  class="w-full px-4 py-2.5 bg-gray-50 border border-gray-100 rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/30" />
                <p class="text-[9px] text-gray-300">Laisser vide = toutes les cultures</p>
              </div>
              <div class="space-y-1.5">
                <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest">Région</label>
                <input v-model="form.region" placeholder="Ex: Hautes Terres, Fianarantsoa…"
                  class="w-full px-4 py-2.5 bg-gray-50 border border-gray-100 rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/30" />
                <p class="text-[9px] text-gray-300">Laisser vide = tout Madagascar</p>
              </div>
            </div>

            <!-- Contenu (Markdown) -->
            <div class="space-y-1.5">
              <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest">Contenu *</label>
              <p class="text-[10px] text-gray-300">Rédigez en Markdown. Ce texte sera injecté dans le contexte de Sesily lors des conversations correspondantes.</p>
              <textarea v-model="form.content" rows="10"
                placeholder="## Pyriculariose du riz&#10;**Symptômes :** taches ovales brun-grisâtre sur feuilles...&#10;**Traitement :** pulvérisation de fongicide à base de tricyclazole..."
                class="w-full px-4 py-3 bg-gray-50 border border-gray-100 rounded-xl text-sm font-mono outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/30 resize-none"></textarea>
            </div>

            <!-- Statut -->
            <div class="flex items-center gap-3 p-3 bg-amber-50 border border-amber-100 rounded-xl">
              <input type="checkbox" id="publish-check" v-model="publishNow" class="w-4 h-4 accent-[#10b481]" />
              <label for="publish-check" class="text-xs font-bold text-amber-800 cursor-pointer">
                Publier immédiatement (disponible pour Sesily dès l'enregistrement)
              </label>
            </div>
          </div>

          <div class="p-6 border-t border-gray-100 flex gap-3 justify-end">
            <button @click="closeModal" class="px-5 py-2.5 rounded-xl text-sm font-bold text-gray-500 hover:bg-gray-100 transition-all">
              Annuler
            </button>
            <button @click="saveEntry" :disabled="isSaving || !form.title || !form.content"
              class="px-5 py-2.5 bg-[#112830] text-white rounded-xl text-sm font-bold hover:bg-[#10b481] transition-all flex items-center gap-2 disabled:opacity-40">
              <div v-if="isSaving" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              <template v-else>
                <i class="bx bx-check text-base"></i>
                {{ editingEntry ? 'Enregistrer' : 'Créer l\'entrée' }}
              </template>
            </button>
          </div>
        </div>
      </div>
    </Transition>

    <!-- TOAST -->
    <Transition name="pop-notification">
      <div v-if="toast.visible" class="fixed top-6 left-1/2 -translate-x-1/2 z-[200] w-full max-w-sm px-4">
        <div :class="['bg-white rounded-2xl shadow-xl p-4 flex items-center gap-3 border',
          toast.type === 'success' ? 'border-l-4 border-l-[#10b481] border-gray-100' : 'border-l-4 border-l-rose-500 border-gray-100']">
          <i :class="['text-xl', toast.type === 'success' ? 'bx bx-check-circle text-[#10b481]' : 'bx bx-error-circle text-rose-500']"></i>
          <p class="text-sm font-bold text-[#112830]">{{ toast.message }}</p>
        </div>
      </div>
    </Transition>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { useApi } from '~/composables/useApi'

definePageMeta({ layout: 'dashboard' })

const { apiFetch } = useApi()

const CATEGORIES = [
  { value: 'maladie',    label: '🦠 Maladie / Ravageur' },
  { value: 'calendrier', label: '📅 Calendrier cultural' },
  { value: 'pratique',   label: '🌱 Bonne pratique' },
  { value: 'variete',    label: '🌾 Variété / Semence' },
  { value: 'marche',     label: '💰 Marché / Prix' },
  { value: 'sol',        label: '🪨 Sol / Fertilisation' },
  { value: 'meteo',      label: '🌦️ Météo / Climat' },
  { value: 'stockage',   label: '🏚️ Stockage / Post-récolte' },
  { value: 'elevage',    label: '🐄 Élevage' },
  { value: 'general',    label: '📖 Général' },
]

const CAT_STYLES: Record<string, { bg: string; badge: string; emoji: string }> = {
  maladie:    { bg: 'bg-red-50',    badge: 'bg-red-100 text-red-700',     emoji: '🦠' },
  calendrier: { bg: 'bg-blue-50',   badge: 'bg-blue-100 text-blue-700',   emoji: '📅' },
  pratique:   { bg: 'bg-emerald-50',badge: 'bg-emerald-100 text-emerald-700', emoji: '🌱' },
  variete:    { bg: 'bg-amber-50',  badge: 'bg-amber-100 text-amber-700', emoji: '🌾' },
  marche:     { bg: 'bg-purple-50', badge: 'bg-purple-100 text-purple-700',emoji: '💰' },
  sol:        { bg: 'bg-orange-50', badge: 'bg-orange-100 text-orange-700',emoji: '🪨' },
  meteo:      { bg: 'bg-sky-50',    badge: 'bg-sky-100 text-sky-700',     emoji: '🌦️' },
  stockage:   { bg: 'bg-gray-50',   badge: 'bg-gray-100 text-gray-700',   emoji: '🏚️' },
  elevage:    { bg: 'bg-yellow-50', badge: 'bg-yellow-100 text-yellow-700',emoji: '🐄' },
  general:    { bg: 'bg-slate-50',  badge: 'bg-slate-100 text-slate-700', emoji: '📖' },
}

// ── State ────────────────────────────────────────────────────────────────────
const entries      = ref<any[]>([])
const stats        = ref({ total: 0, published: 0, draft: 0, by_category: [] as any[] })
const isLoading    = ref(false)
const isSaving     = ref(false)
const search       = ref('')
const filterCategory = ref('')
const filterStatus   = ref('')
const showModal    = ref(false)
const editingEntry = ref<any>(null)
const cropsInput   = ref('')
const publishNow   = ref(false)

const form = ref({
  title: '', category: 'maladie', content: '',
  region: '', language: 'fr',
})

const toast = ref({ visible: false, message: '', type: 'success' })

// ── Computed ─────────────────────────────────────────────────────────────────
const statsCards = computed(() => [
  { label: 'Total entrées',  value: stats.value.total,     icon: 'bx bx-book-open',   bg: 'bg-blue-50',    color: 'text-blue-500' },
  { label: 'Publiées',       value: stats.value.published, icon: 'bx bx-check-circle',bg: 'bg-emerald-50', color: 'text-emerald-500' },
  { label: 'Brouillons',     value: stats.value.draft,     icon: 'bx bx-edit',        bg: 'bg-amber-50',   color: 'text-amber-500' },
  { label: 'Catégories',     value: stats.value.by_category.length, icon: 'bx bx-category', bg: 'bg-purple-50', color: 'text-purple-500' },
])

// ── Utils ────────────────────────────────────────────────────────────────────
type CatStyle = { bg: string; badge: string; emoji: string }
const FALLBACK_STYLE: CatStyle = { bg: 'bg-slate-50', badge: 'bg-slate-100 text-slate-700', emoji: '📖' }

function categoryStyle(cat: string): CatStyle {
  const s = CAT_STYLES[cat]
  if (s !== undefined) return s
  const g = CAT_STYLES['general']
  if (g !== undefined) return g
  return FALLBACK_STYLE
}

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' })
}

function showToast(message: string, type: 'success' | 'error' = 'success') {
  toast.value = { visible: true, message, type }
  setTimeout(() => { toast.value.visible = false }, 3500)
}

// ── API ───────────────────────────────────────────────────────────────────────
async function fetchEntries() {
  isLoading.value = true
  try {
    const params = new URLSearchParams()
    if (search.value)         params.set('search', search.value)
    if (filterCategory.value) params.set('category', filterCategory.value)
    if (filterStatus.value)   params.set('status', filterStatus.value)
    const qs = params.toString() ? `?${params}` : ''
    const data: any = await apiFetch(`/api/v2/knowledge-base/${qs}`)
    entries.value = data.results || []
  } finally {
    isLoading.value = false
  }
}

async function fetchStats() {
  try {
    const data: any = await apiFetch('/api/v2/knowledge-base/stats/')
    stats.value = data
  } catch (_) {}
}

async function toggleStatus(entry: any) {
  const action = entry.status === 'PUBLISHED' ? 'unpublish' : 'publish'
  try {
    const updated: any = await apiFetch(`/api/v2/knowledge-base/${entry.id}/${action}/`, { method: 'POST' })
    const idx = entries.value.findIndex(e => e.id === entry.id)
    if (idx !== -1) entries.value[idx] = updated
    await fetchStats()
    showToast(action === 'publish' ? 'Entrée publiée — Sesily peut l\'utiliser.' : 'Entrée mise en brouillon.')
  } catch (_) {
    showToast('Erreur lors du changement de statut.', 'error')
  }
}

async function confirmDelete(entry: any) {
  if (!confirm(`Supprimer définitivement "${entry.title}" ?`)) return
  try {
    await apiFetch(`/api/v2/knowledge-base/${entry.id}/`, { method: 'DELETE' })
    entries.value = entries.value.filter(e => e.id !== entry.id)
    await fetchStats()
    showToast('Entrée supprimée.')
  } catch (_) {
    showToast('Erreur lors de la suppression.', 'error')
  }
}

// ── Modal ────────────────────────────────────────────────────────────────────
function openCreate() {
  editingEntry.value = null
  form.value = { title: '', category: 'maladie', content: '', region: '', language: 'fr' }
  cropsInput.value = ''
  publishNow.value = false
  showModal.value = true
}

function openEdit(entry: any) {
  editingEntry.value = entry
  form.value = {
    title: entry.title, category: entry.category, content: entry.content,
    region: entry.region || '', language: entry.language || 'fr',
  }
  cropsInput.value = (entry.crops || []).join(', ')
  publishNow.value = entry.status === 'PUBLISHED'
  showModal.value = true
}

function closeModal() {
  showModal.value = false
  editingEntry.value = null
}

async function saveEntry() {
  if (!form.value.title || !form.value.content) return
  isSaving.value = true
  try {
    const payload = {
      ...form.value,
      crops: cropsInput.value ? cropsInput.value.split(',').map(c => c.trim().toLowerCase()).filter(Boolean) : [],
      status: publishNow.value ? 'PUBLISHED' : 'DRAFT',
    }
    if (editingEntry.value) {
      const updated: any = await apiFetch(`/api/v2/knowledge-base/${editingEntry.value.id}/`, {
        method: 'PUT', body: payload,
      })
      const idx = entries.value.findIndex(e => e.id === editingEntry.value.id)
      if (idx !== -1) entries.value[idx] = updated
      showToast('Entrée mise à jour avec succès.')
    } else {
      const created: any = await apiFetch('/api/v2/knowledge-base/', { method: 'POST', body: payload })
      entries.value.unshift(created)
      showToast('Entrée créée.' + (publishNow.value ? ' Sesily peut déjà l\'utiliser.' : ' En brouillon.'))
    }
    await fetchStats()
    closeModal()
  } catch (_) {
    showToast('Erreur lors de l\'enregistrement.', 'error')
  } finally {
    isSaving.value = false
  }
}

// ── Watchers ──────────────────────────────────────────────────────────────────
let debounceTimer: ReturnType<typeof setTimeout>
watch([search, filterCategory, filterStatus], () => {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(fetchEntries, 350)
})

onMounted(() => {
  fetchEntries()
  fetchStats()
})

// ════════════════════════════════════════════════════════════════════════════
// IMPORT MULTI-SOURCE
// ════════════════════════════════════════════════════════════════════════════

interface ProposedEntry {
  title:    string
  category: string
  content:  string
  crops:    string[]
  region:   string
  language: string
  selected: boolean
  expanded: boolean
}

const SOURCE_TYPES = [
  { type: 'pdf',   emoji: '📄', label: 'PDF',        accept: '.pdf' },
  { type: 'excel', emoji: '📊', label: 'Excel / CSV', accept: '.xlsx,.xls,.csv' },
  { type: 'docx',  emoji: '📝', label: 'Word',        accept: '.docx,.doc' },
  { type: 'url',   emoji: '🌐', label: 'URL Web',     accept: null },
  { type: 'image', emoji: '🖼️', label: 'Image',       accept: '.jpg,.jpeg,.png,.webp' },
  { type: 'text',  emoji: '✏️', label: 'Texte',       accept: null },
] as const

type ImportSourceType = (typeof SOURCE_TYPES)[number]['type']

const showImportModal  = ref(false)
const showPreviewModal = ref(false)
const importType       = ref<ImportSourceType>('pdf')
const importFile       = ref<File | null>(null)
const importUrl        = ref('')
const importText       = ref('')
const isAnalyzing      = ref(false)
const isImporting      = ref(false)
const proposedEntries  = ref<ProposedEntry[]>([])
const publishImport    = ref(false)
const fileInputRef     = ref<HTMLInputElement | null>(null)

const currentSourceType = computed(() => SOURCE_TYPES.find(t => t.type === importType.value))

const canAnalyze = computed(() => {
  if (['pdf', 'excel', 'docx', 'image'].includes(importType.value)) return !!importFile.value
  if (importType.value === 'url')  return !!importUrl.value.trim()
  if (importType.value === 'text') return !!importText.value.trim()
  return false
})

function closeImportModal() {
  showImportModal.value = false
  importFile.value = null
  importUrl.value  = ''
  importText.value = ''
}

function onFileChange(e: Event) {
  const input = e.target as HTMLInputElement
  importFile.value = input.files?.[0] ?? null
}

function onFileDrop(e: DragEvent) {
  const file = e.dataTransfer?.files?.[0]
  if (file) importFile.value = file
}

function formatFileSize(bytes: number): string {
  if (bytes < 1024)       return `${bytes} o`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} Ko`
  return `${(bytes / (1024 * 1024)).toFixed(1)} Mo`
}

async function analyzeSource() {
  if (!canAnalyze.value) return
  isAnalyzing.value = true
  try {
    const formData = new FormData()
    formData.append('type', importType.value)
    if (['pdf', 'excel', 'docx', 'image'].includes(importType.value) && importFile.value) {
      formData.append('file', importFile.value)
    } else if (importType.value === 'url') {
      formData.append('url', importUrl.value.trim())
    } else {
      formData.append('text', importText.value.trim())
    }

    const data: any = await apiFetch('/api/v2/knowledge-base/import-source/', {
      method: 'POST',
      body:   formData,
    })

    const entries: ProposedEntry[] = (data.entries ?? []).map((e: any) => ({
      ...e,
      selected: true,
      expanded: false,
    }))

    if (entries.length === 0) {
      showToast('Aucune entrée extraite depuis cette source. Essayez une autre.', 'error')
      return
    }

    proposedEntries.value = entries
    showImportModal.value  = false
    showPreviewModal.value = true
  } catch (e: any) {
    showToast(e?.data?.error ?? "Erreur lors de l'analyse.", 'error')
  } finally {
    isAnalyzing.value = false
  }
}

async function confirmImport() {
  const selected = proposedEntries.value.filter(e => e.selected)
  if (selected.length === 0) {
    showToast('Sélectionnez au moins une entrée.', 'error')
    return
  }
  isImporting.value = true
  try {
    const payload = selected.map(({ selected: _s, expanded: _e, ...rest }) => ({
      ...rest,
      status: publishImport.value ? 'PUBLISHED' : 'DRAFT',
    }))
    const data: any = await apiFetch('/api/v2/knowledge-base/import-confirm/', {
      method: 'POST',
      body:   { entries: payload },
    })
    showPreviewModal.value = false
    proposedEntries.value  = []
    publishImport.value    = false
    await fetchEntries()
    await fetchStats()
    showToast(`${data.imported} entrée(s) importée(s) avec succès !`)
  } catch (e: any) {
    showToast(e?.data?.error ?? "Erreur lors de l'import.", 'error')
  } finally {
    isImporting.value = false
  }
}
</script>

<style scoped>
.pop-modal-enter-active, .pop-modal-leave-active { transition: all 0.2s ease; }
.pop-modal-enter-from, .pop-modal-leave-to { opacity: 0; transform: scale(0.95); }
.pop-notification-enter-active, .pop-notification-leave-active { transition: all 0.3s ease; }
.pop-notification-enter-from, .pop-notification-leave-to { opacity: 0; transform: translateY(-12px); }
.line-clamp-2 { display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
</style>
