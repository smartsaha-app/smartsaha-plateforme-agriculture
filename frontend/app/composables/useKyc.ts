import { ref } from 'vue'
import { useApi } from '~/composables/useApi'

export const useKyc = () => {
  const { apiFetch } = useApi()

  const documents    = ref<any[]>([])
  const isLoading    = ref(false)
  const isSubmitting = ref(false)
  const adminStats   = ref({ total: 0, pending: 0, approved: 0, rejected: 0 })

  // ── Utilisateur ────────────────────────────────────────────────────────────

  const fetchMyDocuments = async () => {
    isLoading.value = true
    try {
      const data: any = await apiFetch('/api/kyc/documents/')
      documents.value = data?.results || data || []
    } finally {
      isLoading.value = false
    }
  }

  const submitDocument = async (docType: string, file: File) => {
    isSubmitting.value = true
    try {
      const formData = new FormData()
      formData.append('doc_type', docType)
      formData.append('file_url', file)
      const result = await apiFetch('/api/kyc/documents/', {
        method: 'POST',
        body: formData,
      })
      return result
    } finally {
      isSubmitting.value = false
    }
  }

  const deleteDocument = async (uuid: string) => {
    await apiFetch(`/api/kyc/documents/${uuid}/`, { method: 'DELETE' })
    documents.value = documents.value.filter(d => d.uuid !== uuid)
  }

  // ── Admin ──────────────────────────────────────────────────────────────────

  const totalCount = ref(0)

  const fetchAllDocuments = async (statusFilter?: string, search?: string, page = 1) => {
    isLoading.value = true
    try {
      const params = new URLSearchParams()
      if (statusFilter) params.set('status', statusFilter)
      if (search)       params.set('search', search)
      params.set('page', String(page))
      const qs = params.toString() ? `?${params}` : ''
      const data: any = await apiFetch(`/api/kyc/admin/${qs}`)
      // Support both paginated (DRF) and plain list responses
      if (data?.results !== undefined) {
        documents.value = data.results
        totalCount.value = data.count ?? data.results.length
      } else {
        documents.value = data || []
        totalCount.value = documents.value.length
      }
    } finally {
      isLoading.value = false
    }
  }

  const fetchAdminStats = async () => {
    try {
      const data: any = await apiFetch('/api/kyc/admin/stats/')
      adminStats.value = data
    } catch (_) {}
  }

  const reviewDocument = async (
    uuid: string,
    status: 'APPROVED' | 'REJECTED',
    rejectionReason?: string
  ) => {
    const payload: Record<string, string> = { status }
    if (rejectionReason) payload.rejection_reason = rejectionReason
    const result = await apiFetch(`/api/kyc/admin/${uuid}/review/`, {
      method: 'PATCH',
      body: payload,
    })
    // Mettre à jour localement
    const idx = documents.value.findIndex(d => d.uuid === uuid)
    if (idx !== -1) documents.value[idx] = result
    return result
  }

  return {
    documents,
    totalCount,
    adminStats,
    isLoading,
    isSubmitting,
    fetchMyDocuments,
    submitDocument,
    deleteDocument,
    fetchAllDocuments,
    fetchAdminStats,
    reviewDocument,
  }
}
