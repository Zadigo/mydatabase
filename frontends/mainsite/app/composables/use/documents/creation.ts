import type { Database } from '#shared/types'
import type { NewDocument, DocumentTypes, DocumentParams } from '#shared/types/documents'
import type { StepperItem } from '@nuxt/ui'
import type { VueUseWsReturnType } from '~/types'

const documentTemplate: NewDocument['documents'][number] = {
  name: '',
  content_type: 'json',
  source_type: 'url',
  url: '',
  file: undefined,
  entry_key: null,
  primary_key_file: false,
  column_options: []
}

const newDocumentDataTemplate: NewDocument = {
  global_name: '',
  documents: [{ ...documentTemplate }],
  merge: false,
}

/**
 * Composable used for creating a new document
 * @param wsObject The websocket object used to send messages to the server when the document is created. If not provided, the composable will not send any websocket messages.
 */
export const useCreateDocument = createGlobalState((_wsObject?: VueUseWsReturnType) => {
  const [showAddDocumentModal, toggleShowAddDocumentModal] = useToggle(false)

  const newDocument = ref<NewDocument>({ ...newDocumentDataTemplate })

  const getNewDocumentByIndex = reactive((index: number) => newDocument.value.documents[index])

  /**
   * Creates the new document
   */

  function resetNewDocument() {
    newDocument.value = { ...newDocumentDataTemplate }
  }

  function selectPrimaryKeyFile(documentParams: DocumentParams | undefined) {
    newDocument.value.documents.forEach((item) => { item.primary_key_file = false })
    if (documentParams) {
      documentParams.primary_key_file = true
    }
  }

  function removeDocument(index: number, callback?: () => void) {
    if (newDocument.value.documents.length === 1) {
      newDocument.value.documents[0] = { ...documentTemplate }
    } else {
      newDocument.value.documents.splice(index, 1)
    }
    if (callback) {
      callback()
    }
  }

  function addDocument(documentType: DocumentTypes = 'json') {
    newDocument.value.documents.push({ ...documentTemplate, content_type: documentType })
  }

  const { currentDatabase } = _useDatabases()
  const { selectedTable } = useTableEditionComposable()

  function create() {
    const { data } = useAsyncData('createDocument', async () => {
      const formData = new FormData()
      
      // Append each document to the form 
      // data under their respective keys
      newDocument.value.documents.forEach((item, idx) => {
        if (item.source_type === 'file' && item.file) {
          formData.append(`file_${idx}`, item.file)
        } else {
          formData.append(`url_${idx}`, item.url || '')
        }

        formData.append(`index_${idx}`, idx.toString())
        formData.append(`name_${idx}`, item.name)
        formData.append(`content_type_${idx}`, item.content_type)
        formData.append(`source_type_${idx}`, item.source_type)
        formData.append(`column_options_${idx}`, JSON.stringify(item.column_options || {}))
        formData.append(`primary_key_file_${idx}`, String(item.primary_key_file))
        
        if (item.entry_key) {
          formData.append(`entry_key_${idx}`, item.entry_key)
        }

      })

      return Promise.all([
        $fetch<{ name: string }>(`/api/tables/${selectedTable.value?.id}/upload`, {
          method: 'POST',
          body: formData,
        }),
        $fetch<Database>(`/api/databases/${currentDatabase.value?.id}`, {
          method: 'GET',
        })
      ])
    }) 

    const [createData, databaseUpdateData] = data.value || [{ name: '' }, {}]
    console.log('createData', createData)
    console.log('databaseUpdateData', databaseUpdateData) 
  }

  const currentStep = ref<StepperItem['title']>('Documents')

  function updateStep(item: StepperItem) {
    currentStep.value = item.title || 'Documents'
  }

  return {
    /**
     * The current step of the stepper when creating a new document
     */
    currentStep,
    /**
     * The new document being created
     */
    newDocument,
    /**
     * Shows the modal to add a new document
     */
    showAddDocumentModal,
    /**
     * Updates the current step of the stepper when creating a new document
     */
    updateStep,
    /**
     * Creates the new document
     */
    create,
    /**
     * Removes a document from the list of documents being created
     * @param index The index of the document to remove
     */
    removeDocument,
    /**
     * Adds a new document to the list of documents being created
     * @param documentType The type of document to add. Defaults to "json"
     */
    addDocument,
    /**
     * Selects a document as the primary key file for the new document being created
     * @param tableDocument The document to select as the primary key file
     */
    selectPrimaryKeyFile,
    /**
     * Resets the new document being created to its initial state
     * @param index The index of the document to reset
     */
    resetNewDocument,
    /**
     * Toggles the modal to add a new document
     */
    toggleShowAddDocumentModal,
    /**
     * Gets the new document being created by its index
     * @param index The index of the document to retrieve
     */
    getNewDocumentByIndex
  }
})
