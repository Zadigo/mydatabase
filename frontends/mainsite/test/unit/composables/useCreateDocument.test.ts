import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useCreateDocument } from '../../../app/composables/use/documents/edition'
import { mountSuspended } from '@nuxt/test-utils/runtime'
import { defineComponent, nextTick } from 'vue'

const fetchMock = vi.fn()
vi.stubGlobal('$fetch', fetchMock)

describe('useCreateDocument', () => {
  let result: ReturnType<typeof useCreateDocument>
  let component: ReturnType<typeof mountSuspended>

  beforeEach(async () => {
    setActivePinia(createPinia())

    component = await mountSuspended(defineComponent({
      template: `
      <div>
        <input type="text" v-model="result.newDocument.name" />
        <input type="text" v-model="result.newDocument.url" />
        <input type="text" v-model="result.newDocument.google_sheet_id" />
        <input type="file" @change="e => result.newDocument.file = e.target.files[0]" />
        <input type="text" v-model="result.newDocument.entry_key" />
        <input type="text" v-model="result.newDocument.using_columns" />
        {{ result.newDocument }}
      </div>
      `,
      setup() {
        result = useCreateDocument()
        return {
          result
        }
      }
    }))
  })


  it('should initialize with default params',  async () => {
    expect(component).toBeDefined()
    expect(result).toBeDefined()

    expect(result.create).toBeTypeOf('function')
    
    expect(toValue(result.currentStep)).toBe('Upload file')
    expect(toValue(result.showAddDocumentModal)).toBe(false)
    expect(toValue(result.canSend)).toBe(false)
    expect(toValue(result.newDocument)).toEqual({
      name: '',
      url: '',
      google_sheet_id: '',
      file: null,
      entry_key: null,
      using_columns: []
    })
  })

  it.only('should update newDocument when inputs change', async () => {
    // await nextTick()

    result.newDocument.name = 'Test Document'
    result.newDocument.url = ''
    result.newDocument.google_sheet_id = ''
    result.newDocument.file = null
    result.newDocument.entry_key = null
    result.newDocument.using_columns = []
    
    await nextTick()


    // const nameInput = component.find('input[type="text"]:nth-of-type(1)')
    // const urlInput = component.find('input[type="text"]:nth-of-type(2)')
    // const googleSheetIdInput = component.find('input[type="text"]:nth-of-type(3)')
    // const entryKeyInput = component.find('input[type="text"]:nth-of-type(5)')
    // const usingColumnsInput = component.find('input[type="text"]:nth-of-type(6)')

    // await nameInput.setValue('Test Document')
    // await urlInput.setValue('https://example.com')
    // await googleSheetIdInput.setValue('sheet123')
    // await entryKeyInput.setValue('entry456')
    // await usingColumnsInput.setValue('["col1", "col2"]')
    console.log(component.html())

    expect(toValue(result.newDocument)).toEqual({
      name: 'Test Document',
      url: 'https://example.com',
      using_columns: ['col1', 'col2'],
      google_sheet_id: "",
      file: null,
      entry_key: null
    })

  })
})
