import type { TableDocument } from '~/types'

export * from './file_checkout'

/**
 * Composable used for editing a document
 */
export const useEditDocument = createGlobalState(() => {
  const [showEditDocumentModal, toggleShowEditDocumentModal] = useToggle()

  const { tableDocuments } = useTableEditionComposable()

  async function remove(tableDocument: TableDocument) {
    // TODO: Move to server
    const { status } = await useFetch(`/v1/documents/${tableDocument.document_uuid}`, {
      baseURL: useRuntimeConfig().public.prodDomain,
      method: 'DELETE'
    })

    if (status.value === 'success') {
      tableDocuments.value = tableDocuments.value.filter(doc => doc.id !== tableDocument.id)
    }
  }

  return {
    /**
     * Shows the modal to edit a document
     */
    showEditDocumentModal,
    /**
     * Removes a document from the database
     * @param tableDocument The document to remove
     */
    remove,
    /**
     * Toggles the modal to edit a document
     */
    toggleShowEditDocumentModal
  }
})
