export interface NewDocument {
  name: string
  url: string
  google_sheet_id: string
  file: null
}

/**
 * Composable used for creating a new document
 */
export function useCreateDocument() {
  const [showAddDocumentModal, toggleShowAddDocumentModal] = useToggle()

  const newDocument = ref<NewDocument>({
    name: '',
    url: '',
    google_sheet_id: '',
    file: null
  })

  return {
    newDocument,
    showAddDocumentModal,
    toggleShowAddDocumentModal
  }
}
