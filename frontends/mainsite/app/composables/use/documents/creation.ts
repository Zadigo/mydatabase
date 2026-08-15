import type { Database, VueUseWsReturnType } from '~/types'
import type { NewDocument, DocumentTypes, DocumentParams } from '.'
import type { StepperItem } from '@nuxt/ui'

/**
 * Composable used for creating a new document
 * @param wsObject The websocket object used to send messages to the server when the document is created. If not provided, the composable will not send any websocket messages.
 */
export const useCreateDocument = createGlobalState((_wsObject?: VueUseWsReturnType) => {
  const [showAddDocumentModal, toggleShowAddDocumentModal] = useToggle(true)

  const newDocument = ref<NewDocument>({
    name: '',
    documents: [
      {
        name: '',
        content_type: 'json',
        source_type: 'url',
        url: null,
        file: undefined,
        entry_key: null,
        primary_key_file: false
      }
    ],
    merge: false,
    using_columns: []
  })

  const getNewDocumentByIndex = reactive((index: number) => newDocument.value.documents[index])

  /**
   * Creates the new document
   */

  function resetNewDocument() {
    newDocument.value = {
      name: '',
      documents: [
        {
          name: '',
          content_type: 'json',
          source_type: 'url',
          url: null,
          file: undefined,
          entry_key: null,
          primary_key_file: false
        }
      ],
      merge: false,
      using_columns: []
    }
  }

  function selectPrimaryKeyFile(documentParams: DocumentParams | undefined) {
    newDocument.value.documents.forEach((item) => { item.primary_key_file = false })
    if (documentParams) {
      documentParams.primary_key_file = true
    }
  }

  function removeDocument(index: number) {
    if (newDocument.value.documents.length === 1) {
      newDocument.value.documents[0] = {
        name: '',
        content_type: 'json',
        source_type: 'url',
        url: null,
        file: undefined,
        entry_key: null,
        primary_key_file: false
      }
    } else {
      newDocument.value.documents.splice(index, 1)
    }
  }

  function addDocument(documentType: DocumentTypes = 'json') {
    newDocument.value.documents.push({
      name: '',
      content_type: documentType,
      source_type: 'url',
      url: null,
      file: undefined,
      entry_key: null,
      primary_key_file: false
    })
  }

  const { currentDatabase } = _useDatabases()
  const { selectedTable } = useTableEditionComposable()

  function create() {
    const { data } = useAsyncData('createDocument', async () => {
      // Append each document to the form data under their respective keys
      const formData = new FormData()

      newDocument.value.documents.forEach((item, idx) => {
        if (item.source_type === 'file' && item.file) {
          formData.append(`file_${idx}`, item.file)
        } else {
          formData.append(`url_${idx}`, item.url || '')
        }

        formData.append(`name_${idx}`, item.name)
        formData.append(`content_type_${idx}`, item.content_type)
        formData.append(`source_type_${idx}`, item.source_type)
        
        if (item.entry_key) {
          formData.append(`entry_key_${idx}`, item.entry_key)
        }

        formData.append(`primary_key_file_${idx}`, String(item.primary_key_file))
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

  // const canSend = computed(() => isDefined(newDocument.value.file))


  return {
    /**
     * Whether the "Create Document" button can be clicked or not. Only when the user has reached the last step of the stepper, which is "Select columns"
     */
    // canSend,
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
     */
    resetNewDocument,
    /**
     * Toggles the modal to add a new document
     */
    toggleShowAddDocumentModal,
    getNewDocumentByIndex
  }
})
