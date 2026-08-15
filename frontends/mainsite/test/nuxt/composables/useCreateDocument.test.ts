import { describe, it, expect, vi, beforeEach } from 'vitest'
import { useCreateDocument } from '~/composables/use/documents/creation'
import type { NewDocument, DocumentParams } from '~/composables/use/documents'
import type { StepperItem } from '@nuxt/ui'

vi.stubGlobal('$fetch', vi.fn())

const emptyDocumentParams: DocumentParams = {
  name: '',
  content_type: 'json',
  source_type: 'url',
  url: null,
  file: undefined,
  entry_key: null,
  primary_key_file: false
}

const emptyNewDocument: NewDocument = {
  name: '',
  documents: [
    emptyDocumentParams
  ],
  merge: false,
  using_columns: []
}

describe('useCreateDocument', () => {
  it('should return default values', async () => {
    const defaults = useCreateDocument()

    expect(defaults).toHaveProperty('currentStep')
    expect(defaults).toHaveProperty('newDocument')
    expect(defaults).toHaveProperty('showAddDocumentModal')
    expect(defaults).toHaveProperty('updateStep')
    expect(defaults).toHaveProperty('create')
    expect(defaults).toHaveProperty('removeDocument')
    expect(defaults).toHaveProperty('addDocument')
    expect(defaults).toHaveProperty('selectPrimaryKeyFile')
    expect(defaults).toHaveProperty('resetNewDocument')
    expect(defaults).toHaveProperty('toggleShowAddDocumentModal')
    expect(defaults).toHaveProperty('getNewDocumentByIndex')

    expect(toValue(defaults.currentStep)).toBe('Documents')
    expect(toValue(defaults.showAddDocumentModal)).toBe(false)

    expect(toValue(defaults.newDocument)).toEqual(emptyNewDocument)
  })

  it('should get new document by index', async () => {
    const defaults = useCreateDocument()

    const documentAtIndex0 = defaults.getNewDocumentByIndex(0)

    expect(toValue(documentAtIndex0)).toBeDefined()
    expect(isReactive(documentAtIndex0)).toBe(true)
  })

  it('should reset new document', async () => {
    const defaults = useCreateDocument()
    defaults.newDocument.value.name = 'Test Document'
    
    const docParams = defaults.newDocument.value.documents[0]
    if (docParams) {
      docParams.name = 'Test Document 1'
      docParams.url = 'https://example.com'
    }

    defaults.resetNewDocument()

    expect(toValue(defaults.newDocument)).toEqual(emptyNewDocument)
  })
  
  describe('useCreateDocument - Group testing', () => {
    let documentParams: DocumentParams[] = []

    beforeEach(() => {
      documentParams = [
        {
          ...emptyDocumentParams,
          name: 'Document 1',
          primary_key_file: false
        },
        {
          ...emptyDocumentParams,
          name: 'Document 2',
          primary_key_file: false
        }
      ]
    })
    
    it('should select primary key file', async () => {
      const defaults = useCreateDocument()

      defaults.newDocument.value.documents = documentParams

      defaults.selectPrimaryKeyFile(defaults.newDocument.value.documents[1])
  
      expect(defaults.newDocument.value.documents[0]?.primary_key_file).toBe(false)
      expect(defaults.newDocument.value.documents[1]?.primary_key_file).toBe(true)
    })

    it ('should remove document when length over 1', async () => {
      const defaults = useCreateDocument()

      defaults.newDocument.value.documents = documentParams

      defaults.removeDocument(0)

      expect(defaults.newDocument.value.documents.length).toBe(1)
      expect(defaults.newDocument.value.documents[0]?.name).toBe('Document 2')
    })

    it ('should reset document when length is 1', async () => {
      const defaults = useCreateDocument()

      const singleDocumentParams = [emptyDocumentParams]
      defaults.newDocument.value.documents = singleDocumentParams

      defaults.removeDocument(0)

      expect(defaults.newDocument.value.documents.length).toBe(1)
      expect(defaults.newDocument.value.documents[0]?.name).toBe('')
    })

    it ('should add document', async () => {
      const defaults = useCreateDocument()

      defaults.newDocument.value.documents = documentParams

      defaults.addDocument('json')

      expect(defaults.newDocument.value.documents.length).toBe(3)
      expect(defaults.newDocument.value.documents[2]?.name).toBe('')
      expect(defaults.newDocument.value.documents[2]?.content_type).toBe('json')
    })
  })

  it('should update step with string', async () => {
    const stepperItem: StepperItem = { title: 'Columns' }

    const defaults = useCreateDocument()
    defaults.updateStep(stepperItem)

    expect(toValue(defaults.currentStep)).toBe('Columns')

    stepperItem.title = undefined
    defaults.updateStep(stepperItem)

    expect(toValue(defaults.currentStep)).toBe('Documents')
  })
})
