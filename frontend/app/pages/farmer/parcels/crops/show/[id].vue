<template>
  <div class="p-8 bg-[#f8fafc] min-h-screen font-sans">

    <!-- ===== HEADER ===== -->
    <PageHeader :title="parcelCrop.crop?.name || '—'">
      <template #subtitle>
        <i class="bx bx-leaf"></i>
        Détails et gestion de la plantation
      </template>
      <template #breadcrumb>
        <NuxtLink to="/farmer/dashboard" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
          <span>Accueil</span>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <NuxtLink to="/farmer/parcels" class="hover:text-[#10b481] transition-colors">Parcelles</NuxtLink>
        <template v-if="parcelCrop.parcel">
          <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
          <NuxtLink :to="`/farmer/parcels/show/${parcelCrop.parcel}`" class="hover:text-[#10b481] transition-colors">
            {{ parcelCrop.parcel_name || 'Parcelle' }}
          </NuxtLink>
        </template>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">{{ parcelCrop.crop?.name || 'Plantation' }}</span>
      </template>
    </PageHeader>
    <div class="flex items-center justify-end gap-3 mb-6">
      <button @click="goBack" class="p-2.5 bg-white border border-gray-200 rounded-xl text-gray-400 hover:text-gray-700 transition-all">
        <i class="bx bx-arrow-back text-lg"></i>
      </button>
      <NuxtLink :to="`/farmer/parcels/crops/edit/${route.params.id}`" class="flex items-center gap-2 px-4 py-2.5 bg-[#013b28] text-white rounded-xl text-[13px] font-medium hover:bg-[#022c22] transition-colors shadow-sm">
        <i class="bx bx-edit-alt text-sm"></i> Modifier
      </NuxtLink>
    </div>

    <!-- ===== TOP: MAP + INFO CARD ===== -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">

      <!-- Map (2/3) -->
      <div class="lg:col-span-2 relative h-[400px] rounded-2xl overflow-hidden shadow-sm border border-gray-100">
        <div id="parcel-crop-map" class="w-full h-full z-0 bg-gray-200"></div>

        <!-- Loading map state -->
        <div v-if="isLoadingMap" class="absolute inset-0 flex items-center justify-center bg-gray-100 z-10">
          <div class="flex flex-col items-center gap-3 text-gray-400">
            <i class="bx bx-loader-alt animate-spin text-3xl"></i>
            <span class="text-[12px] font-medium">Chargement de la carte...</span>
          </div>
        </div>

        <!-- Map Legend -->
        <div class="absolute bottom-4 left-4 z-10 bg-white/95 backdrop-blur-md px-4 py-3 rounded-xl shadow-sm border border-white/40 flex items-center gap-5">
          <div class="flex items-center gap-2">
            <div class="w-3 h-3 rounded-sm bg-gray-400/70 border border-gray-500/30"></div>
            <span class="text-[11px] text-gray-500 font-medium">Parcelle totale</span>
          </div>
          <div class="flex items-center gap-2">
            <div class="w-3 h-3 rounded-sm bg-emerald-500"></div>
            <span class="text-[11px] text-gray-500 font-medium">Surface culture ({{ cropPercentage }}%)</span>
          </div>
        </div>
      </div>

      <!-- Info Card (1/3) -->
      <div class="lg:col-span-1 bg-white rounded-2xl p-7 shadow-sm border border-gray-100/50 flex flex-col justify-between h-[400px]">
        <div>
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-[15px] font-medium text-gray-900">Informations</h3>
            <span :class="['px-2.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider border', statusBadgeClass]">
              {{ parcelCrop.status?.name || '—' }}
            </span>
          </div>

          <div class="space-y-4">
            <div class="flex items-start gap-3">
              <div class="w-8 h-8 bg-gray-50 rounded-xl flex items-center justify-center text-gray-500 flex-shrink-0">
                <i class="bx bx-map-alt text-sm"></i>
              </div>
              <div>
                <p class="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-0.5">Parcelle</p>
                <p class="text-[13px] font-semibold text-gray-900">{{ parcelCrop.parcel_name || '—' }}</p>
              </div>
            </div>

            <div class="flex items-start gap-3">
              <div class="w-8 h-8 bg-emerald-50 rounded-xl flex items-center justify-center text-emerald-600 flex-shrink-0">
                <i class="bx bxs-leaf text-sm"></i>
              </div>
              <div>
                <p class="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-0.5">Culture</p>
                <p class="text-[13px] font-semibold text-gray-900">{{ parcelCrop.crop?.name || '—' }}</p>
                <p v-if="parcelCrop.crop?.variety?.name" class="text-[11px] text-gray-400">{{ parcelCrop.crop.variety.name }}</p>
              </div>
            </div>

            <div class="flex items-start gap-3">
              <div class="w-8 h-8 bg-blue-50 rounded-xl flex items-center justify-center text-blue-500 flex-shrink-0">
                <i class="bx bx-calendar text-sm"></i>
              </div>
              <div>
                <p class="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-0.5">Date de plantation</p>
                <p class="text-[13px] font-semibold text-gray-900">{{ formatDate(parcelCrop.planting_date) }}</p>
              </div>
            </div>

            <div class="flex items-start gap-3">
              <div class="w-8 h-8 bg-amber-50 rounded-xl flex items-center justify-center text-amber-500 flex-shrink-0">
                <i class="bx bx-calendar-check text-sm"></i>
              </div>
              <div>
                <p class="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-0.5">Date de récolte</p>
                <p class="text-[13px] font-semibold" :class="parcelCrop.harvest_date ? 'text-gray-900' : 'text-gray-300 italic'">
                  {{ parcelCrop.harvest_date ? formatDate(parcelCrop.harvest_date) : 'Non planifiée' }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Surface stat at bottom -->
        <div class="pt-4 border-t border-gray-100">
          <div class="flex items-center justify-between mb-3">
            <div>
              <p class="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1">Surface allouée</p>
              <p class="text-[22px] font-bold text-gray-900">{{ parcelCrop.area }} <span class="text-[13px] font-medium text-gray-400">m²</span></p>
            </div>
            <div class="w-10 h-10 bg-emerald-50 rounded-xl flex items-center justify-center text-emerald-600">
              <i class="bx bx-area text-lg"></i>
            </div>
          </div>
          <div class="flex justify-between text-[10px] text-gray-400 mb-1.5">
            <span>{{ cropPercentage }}% de la parcelle</span>
            <span>{{ parcelTotalAreaM2 }} m² total</span>
          </div>
          <div class="h-1.5 bg-gray-100 rounded-full overflow-hidden">
            <div class="h-full bg-emerald-500 rounded-full transition-all duration-700" :style="{ width: cropPercentage + '%' }"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- ===== RECOMMENDATIONS CARD ===== -->
    <div class="bg-white rounded-2xl p-7 shadow-sm border border-gray-100/50 mb-6">
      <div class="flex items-center justify-between mb-5">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 bg-emerald-50 rounded-xl flex items-center justify-center text-emerald-600">
            <i class="bx bx-bulb text-lg"></i>
          </div>
          <div>
            <h3 class="text-[15px] font-medium text-gray-900">Recommandations agronomiques</h3>
            <p class="text-[11px] text-gray-400">Basées sur le statut et la culture en cours</p>
          </div>
        </div>
        <span class="px-2.5 py-1 bg-emerald-50 text-emerald-700 rounded-lg text-[11px] font-semibold border border-emerald-100">Sesily AI</span>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div v-for="rec in recommendations" :key="rec.title" class="flex gap-3 p-4 bg-gray-50/60 rounded-xl border border-gray-100">
          <div :class="['w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 text-sm', rec.iconBg]">
            <i :class="['bx', rec.icon]"></i>
          </div>
          <div>
            <p class="text-[12px] font-semibold text-gray-800 mb-0.5">{{ rec.title }}</p>
            <p class="text-[11px] text-gray-500 leading-relaxed">{{ rec.text }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- ===== BOTTOM GRID: TASKS + YIELDS ===== -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 pb-10">

      <!-- Tasks Card -->
      <div class="bg-white rounded-2xl p-7 shadow-sm border border-gray-100/50 flex flex-col">

        <!-- Header -->
        <div class="flex items-start justify-between mb-4">
          <div>
            <h3 class="text-[15px] font-medium text-gray-900">Tâches agricoles</h3>
            <p class="text-[11px] text-gray-400 mt-0.5">{{ tasks.length }} tâche{{ tasks.length !== 1 ? 's' : '' }}</p>
          </div>
          <div class="flex items-center gap-2 flex-shrink-0">
            <NuxtLink
              :to="`/farmer/parcels/crops/show/tasks/create?parcel_crop=${route.params.id}`"
              class="flex items-center gap-1.5 px-3.5 py-2 bg-[#013b28] text-white rounded-xl text-[12px] font-medium hover:bg-[#022c22] transition-colors shadow-sm"
            >
              <i class="bx bx-plus text-sm"></i> Ajouter
            </NuxtLink>
            <NuxtLink
              :to="`/farmer/parcels/crops/show/tasks?parcel_crop=${route.params.id}`"
              class="flex items-center gap-1.5 px-3.5 py-2 bg-gray-50 border border-gray-100 text-gray-500 rounded-xl text-[12px] font-medium hover:bg-gray-100 transition-colors"
            >
              Tout voir <i class="bx bx-right-arrow-alt text-sm"></i>
            </NuxtLink>
          </div>
        </div>

        <!-- Barre de progression globale -->
        <div v-if="tasks.length" class="mb-5">
          <div class="flex items-center justify-between text-[10px] font-semibold text-gray-400 mb-1.5">
            <span>Progression générale</span>
            <span class="text-emerald-600">
              {{ tasks.length ? Math.round((tasks.filter(t => t.status_detail?.name === 'Done').length / tasks.length) * 100) : 0 }}%
            </span>
          </div>
          <div class="h-1.5 bg-gray-100 rounded-full overflow-hidden">
            <div
              class="h-full bg-emerald-500 rounded-full transition-all duration-700"
              :style="{ width: tasks.length ? Math.round((tasks.filter(t => t.status_detail?.name === 'Done').length / tasks.length) * 100) + '%' : '0%' }"
            ></div>
          </div>
        </div>

        <!-- Liste -->
        <div class="space-y-2 max-h-[320px] overflow-y-auto pr-0.5">
          <div v-if="isLoadingTasks" class="py-10 flex flex-col items-center gap-2 text-gray-400">
            <i class="bx bx-loader-alt animate-spin text-2xl"></i>
            <span class="text-[12px]">Chargement…</span>
          </div>

          <div v-else-if="!tasks.length" class="py-10 text-center">
            <div class="w-12 h-12 bg-emerald-50 rounded-full flex items-center justify-center mx-auto mb-3">
              <i class="bx bx-task text-emerald-500 text-xl"></i>
            </div>
            <p class="text-[13px] font-semibold text-gray-700 mb-1">Aucune tâche planifiée</p>
            <p class="text-[11px] text-gray-400 mb-4">Ajoutez une première tâche agricole.</p>
            <NuxtLink
              :to="`/farmer/parcels/crops/show/tasks/create?parcel_crop=${route.params.id}`"
              class="inline-flex items-center gap-1.5 px-4 py-2 bg-[#013b28] text-white rounded-xl text-[12px] font-medium hover:bg-[#022c22] transition-colors"
            >
              <i class="bx bx-plus text-sm"></i> Créer une tâche
            </NuxtLink>
          </div>

          <!-- Task row -->
          <div
            v-for="task in tasks"
            :key="task.id"
            :class="[
              'relative flex items-start gap-3 px-4 py-3.5 rounded-xl border transition-all group cursor-default',
              task.is_overdue && task.status_detail?.name !== 'Done'
                ? 'border-rose-100 bg-rose-50/30 hover:bg-rose-50/50'
                : 'border-gray-100 bg-gray-50/20 hover:bg-gray-50/60 hover:border-gray-200'
            ]"
          >
            <!-- Barre latérale de priorité -->
            <div :class="['absolute left-0 top-2 bottom-2 w-[3px] rounded-r-full', getPriorityBar(task.priority_detail?.name)]"></div>

            <!-- Icône statut -->
            <div :class="['w-7 h-7 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5', getTaskStatusIconBg(task.status_detail?.name)]">
              <i :class="['bx text-sm', getTaskStatusIcon(task.status_detail?.name)]"></i>
            </div>

            <!-- Contenu -->
            <div class="flex-1 min-w-0">
              <!-- Ligne 1 : nom + badge statut -->
              <div class="flex items-center gap-2 mb-1">
                <p :class="[
                  'text-[13px] font-semibold truncate flex-1',
                  task.status_detail?.name === 'Done' ? 'line-through text-gray-400' : 'text-gray-900'
                ]">{{ task.name || task.title || '—' }}</p>
                <span :class="['flex-shrink-0 text-[9px] font-black uppercase tracking-widest px-2 py-0.5 rounded-full', getTaskStatusChip(task.status_detail?.name)]">
                  {{ getTaskStatusLabel(task.status_detail?.name) }}
                </span>
              </div>

              <!-- Ligne 2 : description -->
              <p v-if="task.description" class="text-[11px] text-gray-400 line-clamp-1 mb-1.5 leading-relaxed">
                {{ task.description }}
              </p>

              <!-- Ligne 3 : méta (date + retard + priorité) -->
              <div class="flex items-center gap-3 flex-wrap">
                <span :class="['flex items-center gap-1 text-[11px]', task.is_overdue && task.status_detail?.name !== 'Done' ? 'text-rose-500 font-semibold' : 'text-gray-400']">
                  <i :class="['bx text-xs', task.is_overdue && task.status_detail?.name !== 'Done' ? 'bxs-calendar text-rose-400' : 'bx-calendar text-gray-300']"></i>
                  {{ task.due_date ? formatDate(task.due_date) : '—' }}
                </span>
                <span v-if="task.is_overdue && task.days_overdue && task.status_detail?.name !== 'Done'"
                  class="text-[9px] font-black text-rose-600 bg-rose-100 px-1.5 py-0.5 rounded-md uppercase tracking-wide">
                  +{{ task.days_overdue }}j retard
                </span>
                <span v-if="task.priority_detail?.name" :class="['text-[10px] font-semibold flex items-center gap-1', getPriorityTextColor(task.priority_detail.name)]">
                  <span :class="['w-1.5 h-1.5 rounded-full', getPriorityBar(task.priority_detail.name)]"></span>
                  {{ getPriorityLabel(task.priority_detail.name) }}
                </span>
              </div>
            </div>

            <!-- Actions au survol -->
            <div class="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity flex-shrink-0 self-center">
              <NuxtLink
                :to="`/farmer/parcels/crops/show/tasks/edit/${task.id}?parcel_crop=${route.params.id}`"
                class="p-1.5 bg-white border border-gray-100 rounded-lg shadow-sm text-gray-400 hover:text-emerald-600 hover:border-emerald-200 transition-all"
                title="Modifier"
              >
                <i class="bx bx-pencil text-sm"></i>
              </NuxtLink>
              <button
                @click="confirmDeleteTask(task.id)"
                class="p-1.5 bg-white border border-gray-100 rounded-lg shadow-sm text-gray-400 hover:text-rose-500 hover:border-rose-200 transition-all"
                title="Supprimer"
              >
                <i class="bx bx-trash text-sm"></i>
              </button>
            </div>
          </div>

          <!-- Footer stats -->
          <div class="mt-4 pt-4 border-t border-gray-100 grid grid-cols-3 gap-3">
            <div class="flex flex-col items-center gap-1 p-3 bg-amber-50 rounded-xl">
              <span class="text-[20px] font-bold text-amber-600">{{ tasks.filter(t => t.status_detail?.name === 'Pending').length }}</span>
              <span class="flex items-center gap-1 text-[10px] font-semibold text-amber-500 uppercase tracking-wider">
                <span class="w-1.5 h-1.5 rounded-full bg-amber-400"></span> En attente
              </span>
            </div>
            <div class="flex flex-col items-center gap-1 p-3 bg-sky-50 rounded-xl">
              <span class="text-[20px] font-bold text-sky-600">{{ tasks.filter(t => t.status_detail?.name === 'In Progress').length }}</span>
              <span class="flex items-center gap-1 text-[10px] font-semibold text-sky-500 uppercase tracking-wider">
                <span class="w-1.5 h-1.5 rounded-full bg-sky-400"></span> En cours
              </span>
            </div>
            <div class="flex flex-col items-center gap-1 p-3 bg-emerald-50 rounded-xl">
              <span class="text-[20px] font-bold text-emerald-600">{{ tasks.filter(t => t.status_detail?.name === 'Done').length }}</span>
              <span class="flex items-center gap-1 text-[10px] font-semibold text-emerald-600 uppercase tracking-wider">
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span> Terminées
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Yields Card -->
      <div class="bg-white rounded-2xl p-7 shadow-sm border border-gray-100/50">
        <div class="flex items-center justify-between mb-5">
          <div>
            <h3 class="text-[15px] font-medium text-gray-900">Rendements</h3>
            <p class="text-[11px] text-gray-400">{{ yieldRecords.length }} enregistrement{{ yieldRecords.length !== 1 ? 's' : '' }}</p>
          </div>
          <div class="flex items-center gap-2">
            <NuxtLink
              :to="`/farmer/parcels/crops/show/yields/create?parcel_crop=${route.params.id}`"
              class="flex items-center gap-1.5 px-3.5 py-2 bg-[#013b28] text-white rounded-xl text-[12px] font-medium hover:bg-[#022c22] transition-colors shadow-sm"
            >
              <i class="bx bx-plus text-sm"></i> Ajouter
            </NuxtLink>
            <NuxtLink
              :to="`/farmer/parcels/crops/show/yields?parcel_crop=${route.params.id}`"
              class="flex items-center gap-1.5 px-3.5 py-2 bg-gray-50 border border-gray-100 text-gray-500 rounded-xl text-[12px] font-medium hover:bg-gray-100 transition-colors"
            >
              Tout voir <i class="bx bx-right-arrow-alt text-sm"></i>
            </NuxtLink>
          </div>
        </div>

        <div class="space-y-2 max-h-[340px] overflow-y-auto">
          <div v-if="isLoadingYields" class="py-8 text-center">
            <i class="bx bx-loader-alt animate-spin text-gray-400 text-xl"></i>
          </div>
          <div v-else-if="!yieldRecords.length" class="py-10 text-center">
            <div class="w-10 h-10 bg-gray-50 rounded-full flex items-center justify-center mx-auto mb-3">
              <i class="bx bx-package text-gray-400 text-lg"></i>
            </div>
            <p class="text-[13px] text-gray-400">Aucun rendement enregistré</p>
          </div>
          <div v-for="record in yieldRecords" :key="record.id" class="flex items-center gap-3 p-3.5 rounded-xl border border-gray-50 hover:bg-gray-50/60 transition-colors group">
            <div class="w-9 h-9 bg-emerald-50 rounded-xl flex items-center justify-center text-emerald-600 flex-shrink-0">
              <i class="bx bx-package text-sm"></i>
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-[13px] font-semibold text-gray-900">{{ record.yield_amount ?? record.yield ?? '—' }} kg</p>
              <p class="text-[11px] text-gray-400">{{ record.date ? formatDate(record.date) : '—' }}</p>
            </div>
            <div v-if="record.notes" class="text-[11px] text-gray-400 truncate max-w-[80px]">{{ record.notes }}</div>
            <div class="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
              <NuxtLink
                :to="`/farmer/parcels/crops/show/yields/edit/${record.id}?parcel_crop=${route.params.id}`"
                class="p-1.5"
                title="Modifier"
              >
                <i class="bx bx-pencil text-sm text-gray-400 hover:text-emerald-600 transition-colors"></i>
              </NuxtLink>
              <button @click="confirmDeleteYield(record.id)" class="p-1.5">
                <i class="bx bx-trash text-sm text-gray-400 hover:text-rose-500 transition-colors"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- ===== DELETE TASK MODAL ===== -->
  <Teleport to="body">
    <Transition name="modal-pop">
      <div v-if="showDeleteTaskModal" class="fixed inset-0 flex items-center justify-center z-[100] px-4">
        <div class="absolute inset-0 bg-[#022c22]/80 backdrop-blur-sm" @click="showDeleteTaskModal = false"></div>
        <div class="bg-white rounded-2xl p-8 w-full max-w-sm text-center shadow-2xl relative z-10">
          <div class="w-16 h-16 bg-rose-50 rounded-2xl flex items-center justify-center mx-auto mb-5">
            <i class="bx bx-trash text-3xl text-rose-500"></i>
          </div>
          <h3 class="text-[16px] font-semibold text-gray-900 mb-2">Supprimer la tâche ?</h3>
          <p class="text-[13px] text-gray-400 mb-7">Cette action est irréversible.</p>
          <div class="flex gap-3">
            <button @click="deleteTaskConfirmed" :disabled="isDeletingTask" class="flex-1 py-3 bg-rose-500 text-white rounded-xl text-[12px] font-bold uppercase tracking-wider hover:bg-rose-600 disabled:opacity-50 transition-colors">
              {{ isDeletingTask ? '...' : 'Supprimer' }}
            </button>
            <button @click="showDeleteTaskModal = false" class="flex-1 py-3 bg-gray-50 text-gray-500 rounded-xl text-[12px] font-bold uppercase tracking-wider hover:bg-gray-100">
              Annuler
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>

  <!-- ===== DELETE YIELD MODAL ===== -->
  <Teleport to="body">
    <Transition name="modal-pop">
      <div v-if="showDeleteYieldModal" class="fixed inset-0 flex items-center justify-center z-[100] px-4">
        <div class="absolute inset-0 bg-[#022c22]/80 backdrop-blur-sm" @click="showDeleteYieldModal = false"></div>
        <div class="bg-white rounded-2xl p-8 w-full max-w-sm text-center shadow-2xl relative z-10">
          <div class="w-16 h-16 bg-rose-50 rounded-2xl flex items-center justify-center mx-auto mb-5">
            <i class="bx bx-trash text-3xl text-rose-500"></i>
          </div>
          <h3 class="text-[16px] font-semibold text-gray-900 mb-2">Supprimer ce rendement ?</h3>
          <p class="text-[13px] text-gray-400 mb-7">Cette action est irréversible.</p>
          <div class="flex gap-3">
            <button @click="deleteYieldConfirmed" :disabled="isDeletingYield" class="flex-1 py-3 bg-rose-500 text-white rounded-xl text-[12px] font-bold uppercase tracking-wider hover:bg-rose-600 disabled:opacity-50 transition-colors">
              {{ isDeletingYield ? '...' : 'Supprimer' }}
            </button>
            <button @click="showDeleteYieldModal = false" class="flex-1 py-3 bg-gray-50 text-gray-500 rounded-xl text-[12px] font-bold uppercase tracking-wider hover:bg-gray-100">
              Annuler
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
definePageMeta({ layout: "dashboard" })

import { ref, computed, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useAuthStore } from "~/stores/auth"
import { useApi } from "~/composables/useApi"

const { locale } = useI18n()
const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const { apiFetch } = useApi()

// ===== STATE =====
const parcelCrop = ref<any>({})
const parcelData = ref<any>({})

const tasks = ref<any[]>([])
const yieldRecords = ref<any[]>([])

const isLoadingMap = ref(true)
const isLoadingTasks = ref(false)
const isLoadingYields = ref(false)

// Task delete
const showDeleteTaskModal = ref(false)
const taskToDeleteId = ref<number | null>(null)
const isDeletingTask = ref(false)

// Yield delete
const showDeleteYieldModal = ref(false)
const yieldToDeleteId = ref<number | null>(null)
const isDeletingYield = ref(false)

// Map
let L: any
let map: any

// ===== COMPUTED =====
const parcelTotalAreaM2 = computed(() => {
  const points = parcelData.value?.points
  if (!points || points.length < 3) return 0
  const areaHa = calculateParcelAreaHa(points)
  return Math.round(Number(areaHa) * 10000)
})

const cropPercentage = computed(() => {
  const total = parcelTotalAreaM2.value
  const crop = Number(parcelCrop.value?.area || 0)
  if (!total || !crop) return 0
  return Math.min(100, Math.round((crop / total) * 100))
})

const statusBadgeClass = computed(() => {
  const name = parcelCrop.value?.status?.name
  switch (name) {
    case "Planned":   return "bg-sky-50 text-sky-600 border-sky-100"
    case "Planted":   return "bg-emerald-50 text-emerald-600 border-emerald-100"
    case "Growing":   return "bg-amber-50 text-amber-600 border-amber-100"
    case "Harvested": return "bg-gray-50 text-gray-600 border-gray-100"
    case "Failed":    return "bg-rose-50 text-rose-600 border-rose-100"
    default:          return "bg-gray-50 text-gray-400 border-gray-100"
  }
})

const recommendations = computed(() => {
  const status = parcelCrop.value?.status?.name
  const harvestDate = parcelCrop.value?.harvest_date
  const plantingDate = parcelCrop.value?.planting_date
  const daysSince = plantingDate
    ? Math.floor((Date.now() - new Date(plantingDate).getTime()) / 86400000)
    : null

  if (!status || status === "Planned") return [
    { icon: "bxs-map-pin",  iconBg: "bg-blue-50 text-blue-500",    title: "Préparation du sol", text: "Assurez-vous que le sol est bien labouré et drainé avant la mise en terre." },
    { icon: "bx-water",     iconBg: "bg-cyan-50 text-cyan-500",     title: "Humidification", text: "Humidifiez le sol quelques jours avant la plantation pour favoriser la germination." },
    { icon: "bxs-leaf",     iconBg: "bg-emerald-50 text-emerald-600", title: "Qualité des semences", text: "Vérifiez la traçabilité et la qualité des semences avant la mise en terre." },
  ]

  if (status === "Planted" || status === "Growing") return [
    { icon: "bx-water",     iconBg: "bg-blue-50 text-blue-500",    title: "Surveillance hydrique", text: `Contrôlez régulièrement l'humidité du sol.${daysSince ? ` ${daysSince} jours depuis la plantation.` : ''}` },
    { icon: "bx-shield",    iconBg: "bg-amber-50 text-amber-500",  title: "Contrôle phytosanitaire", text: "Inspectez les feuilles et tiges pour détecter maladies et ravageurs." },
    { icon: "bx-time-five", iconBg: "bg-emerald-50 text-emerald-600", title: "Planification récolte", text: harvestDate ? `Récolte prévue le ${formatDate(harvestDate)}.` : "Définissez une date de récolte estimée pour optimiser votre planification." },
  ]

  if (status === "Harvested") return [
    { icon: "bx-rotate-left", iconBg: "bg-amber-50 text-amber-500",  title: "Rotation culturale", text: "Planifiez une culture différente pour maintenir la fertilité du sol." },
    { icon: "bx-data",        iconBg: "bg-blue-50 text-blue-500",    title: "Analyse des rendements", text: "Comparez avec les saisons précédentes pour identifier les axes d'amélioration." },
    { icon: "bxs-leaf",       iconBg: "bg-emerald-50 text-emerald-600", title: "Amendement du sol", text: "Apportez du compost ou un engrais organique pour préparer la prochaine saison." },
  ]

  return [
    { icon: "bx-error",   iconBg: "bg-rose-50 text-rose-500",    title: "Analyse post-échec", text: "Identifiez les causes (maladie, sécheresse, ravageurs) pour éviter la répétition." },
    { icon: "bx-vial",    iconBg: "bg-amber-50 text-amber-500",  title: "Test de sol", text: "Réalisez une analyse de sol pour détecter carences ou excès de nutriments." },
    { icon: "bx-refresh", iconBg: "bg-blue-50 text-blue-500",    title: "Consultation", text: "Consultez un agronome avant de replanter sur cette parcelle." },
  ]
})

// ===== HELPERS =====
function formatDate(date: string | null) {
  if (!date) return "—"
  try {
    return new Date(date).toLocaleDateString(locale.value === "fr" ? "fr-FR" : "en-GB", { day: "2-digit", month: "short", year: "numeric" })
  } catch { return date }
}

function calculateParcelAreaHa(points: any[]): number {
  if (!points || points.length < 3) return 0
  let area = 0
  const n = points.length
  for (let i = 0; i < n; i++) {
    const { lat: x1, lng: y1 } = points[i]
    const { lat: x2, lng: y2 } = points[(i + 1) % n]
    area += x1 * y2 - x2 * y1
  }
  area = Math.abs(area / 2)
  const avgLat = points.reduce((s: number, p: any) => s + p.lat, 0) / points.length
  const areaM2 = area * 111000 * 111000 * Math.cos((avgLat * Math.PI) / 180)
  return areaM2 / 10000
}

function getTaskStatusIcon(name: string) {
  if (name === "Done")        return "bx-check text-emerald-600"
  if (name === "In Progress") return "bx-time-five text-sky-500"
  if (name === "Cancelled")   return "bx-x text-gray-400"
  return "bx-time text-amber-500" // Pending
}

function getTaskStatusIconBg(name: string) {
  if (name === "Done")        return "bg-emerald-50"
  if (name === "In Progress") return "bg-sky-50"
  if (name === "Cancelled")   return "bg-gray-100"
  return "bg-amber-50" // Pending
}

function getTaskStatusChip(name: string) {
  if (name === "Done")        return "bg-emerald-100 text-emerald-700"
  if (name === "In Progress") return "bg-sky-100 text-sky-700"
  if (name === "Cancelled")   return "bg-gray-100 text-gray-500"
  return "bg-amber-100 text-amber-700" // Pending
}

function getTaskStatusLabel(name: string) {
  if (name === "Done")        return "Terminée"
  if (name === "In Progress") return "En cours"
  if (name === "Cancelled")   return "Annulée"
  return "En attente" // Pending
}

function getPriorityBar(name: string) {
  if (name === "High")   return "bg-rose-500"
  if (name === "Medium") return "bg-amber-400"
  if (name === "Low")    return "bg-emerald-500"
  return "bg-gray-200"
}

function getPriorityTextColor(name: string) {
  if (name === "High")   return "text-rose-500"
  if (name === "Medium") return "text-amber-500"
  return "text-emerald-600"
}

function getPriorityLabel(name: string) {
  if (name === "High")   return "Haute"
  if (name === "Medium") return "Moyenne"
  if (name === "Low")    return "Faible"
  return name ?? "—"
}

// Conservé pour compatibilité (non utilisé dans le nouveau design)
function getTaskStatusDot(name: string) {
  if (name === "Done")        return "bg-emerald-500"
  if (name === "In Progress") return "bg-sky-500"
  if (name === "Cancelled")   return "bg-gray-400"
  return "bg-amber-400" // Pending
}

// ===== MAP =====
async function initMap(points: any[]) {
  isLoadingMap.value = true
  if (!import.meta.client || !points || points.length < 3) {
    isLoadingMap.value = false
    return
  }

  L = await import("leaflet")
  await import("leaflet/dist/leaflet.css")

  const satellite = L.tileLayer(
    "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    { attribution: "Esri" }
  )

  map = L.map("parcel-crop-map", {
    center: [-18.8792, 47.5079],
    zoom: 6,
    layers: [satellite],
    zoomControl: false,
  })

  const latlngs = points.map((p: any) => [p.lat, p.lng])

  // Full parcel polygon — muted gray
  const parcelPoly = L.polygon(latlngs, {
    color: "#6b7280",
    fillColor: "#9ca3af",
    fillOpacity: 0.35,
    weight: 2,
    dashArray: "5 5",
  }).addTo(map)

  // Scaled inner polygon — represents the crop surface area
  const centroid = {
    lat: points.reduce((s: number, p: any) => s + p.lat, 0) / points.length,
    lng: points.reduce((s: number, p: any) => s + p.lng, 0) / points.length,
  }

  const totalAreaM2 = Number(calculateParcelAreaHa(points)) * 10000
  const cropAreaM2 = Number(parcelCrop.value?.area || 0)
  const scaleFactor = totalAreaM2 > 0 ? Math.min(1, Math.sqrt(cropAreaM2 / totalAreaM2)) : 0.5

  const scaledPoints = points.map((p: any) => ({
    lat: centroid.lat + (p.lat - centroid.lat) * scaleFactor,
    lng: centroid.lng + (p.lng - centroid.lng) * scaleFactor,
  }))

  L.polygon(scaledPoints.map((p: any) => [p.lat, p.lng]), {
    color: "#10b481",
    fillColor: "#10b481",
    fillOpacity: 0.55,
    weight: 2,
  }).addTo(map)

  map.fitBounds(parcelPoly.getBounds(), { padding: [40, 40] })
  isLoadingMap.value = false
}

// ===== TASKS CRUD =====
function confirmDeleteTask(id: number) {
  taskToDeleteId.value = id
  showDeleteTaskModal.value = true
}

async function deleteTaskConfirmed() {
  if (!taskToDeleteId.value) return
  isDeletingTask.value = true
  try {
    await apiFetch(`/api/tasks/${taskToDeleteId.value}/`, { method: "DELETE" })
    tasks.value = tasks.value.filter(t => t.id !== taskToDeleteId.value)
    showDeleteTaskModal.value = false
  } catch (e) {
    console.error("Erreur suppression tâche:", e)
  } finally {
    isDeletingTask.value = false
  }
}

// ===== YIELDS CRUD =====
function confirmDeleteYield(id: number) {
  yieldToDeleteId.value = id
  showDeleteYieldModal.value = true
}

async function deleteYieldConfirmed() {
  if (!yieldToDeleteId.value) return
  isDeletingYield.value = true
  try {
    await apiFetch(`/api/yield-records/${yieldToDeleteId.value}/`, { method: "DELETE" })
    yieldRecords.value = yieldRecords.value.filter(r => r.id !== yieldToDeleteId.value)
    showDeleteYieldModal.value = false
  } catch (e) {
    console.error("Erreur suppression rendement:", e)
  } finally {
    isDeletingYield.value = false
  }
}

const goBack = () => router.back()

// ===== INIT =====
onMounted(async () => {
  if (!authStore.isAuthenticated) return router.push("/login")

  try {
    // 1. Fetch parcel-crop data
    const cropData: any = await apiFetch(`/api/parcel-crops/${route.params.id}/`)

    // 2. Fetch parcel to get polygon points and name
    let parcel: any = null
    try {
      parcel = await apiFetch(`/api/parcels/${cropData.parcel}/`)
    } catch {
      // Fallback: list and find
      try {
        const list: any = await apiFetch("/api/parcels/")
        const items = Array.isArray(list) ? list : (list.results || [])
        parcel = items.find((p: any) => p.uuid === cropData.parcel) || null
      } catch { /* no points available */ }
    }

    parcelData.value = parcel || {}
    parcelCrop.value = {
      ...cropData,
      parcel_name: parcel?.name || parcel?.parcel_name || cropData.parcel,
    }

    // 3. Init map with parcel polygon
    if (parcel?.points?.length >= 3) {
      await initMap(parcel.points)
    } else {
      isLoadingMap.value = false
    }

    // 4. Fetch tasks for this parcel-crop
    isLoadingTasks.value = true
    try {
      const taskData: any = await apiFetch(`/api/tasks/?parcel_crop=${route.params.id}`)
      tasks.value = Array.isArray(taskData) ? taskData : (taskData.results || [])
    } catch (e) {
      console.error("Erreur chargement tâches:", e)
    } finally {
      isLoadingTasks.value = false
    }

    // 5. Fetch yield records for this parcel-crop
    isLoadingYields.value = true
    try {
      const yieldData: any = await apiFetch(`/api/yield-records/?parcel_crop=${route.params.id}`)
      yieldRecords.value = Array.isArray(yieldData) ? yieldData : (yieldData.results || [])
    } catch (e) {
      console.error("Erreur chargement rendements:", e)
    } finally {
      isLoadingYields.value = false
    }

  } catch (err) {
    console.error("Erreur chargement plantation:", err)
  }
})
</script>

<style scoped>
#parcel-crop-map {
  height: 100%;
  width: 100%;
}

:deep(.leaflet-bar) {
  border: none;
  box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1);
}

:deep(.leaflet-bar a) {
  background-color: white;
  color: #112830;
  border-radius: 12px !important;
  margin-bottom: 5px;
  border: none;
}

.modal-pop-enter-active,
.modal-pop-leave-active {
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.modal-pop-enter-from,
.modal-pop-leave-to {
  opacity: 0;
  transform: scale(0.95);
}
</style>