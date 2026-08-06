import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useCreateDocument } from '~/composables/use/documents/edition'
import { mountSuspended } from '@nuxt/test-utils/runtime'
import { defineComponent, nextTick } from 'vue'

vi.stubGlobal('$fetch', vi.fn())

describe('useCreateDocument', () => {
  let result: ReturnType<typeof useCreateDocument>
  let component: ReturnType<typeof mountSuspended>

  beforeEach(async () => {
    setActivePinia(createPinia())

    component = await mountSuspended(
      defineComponent({
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
      }
    ))
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

  it.todo('should update newDocument when inputs change', async () => {
    result.newDocument.value.name = 'Test Document'
    result.newDocument.value.url = ''
    result.newDocument.value.google_sheet_id = ''
    result.newDocument.value.file = null
    result.newDocument.value.entry_key = null
    result.newDocument.value.using_columns = []
    
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
