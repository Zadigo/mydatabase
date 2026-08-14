import { mockNuxtImport, mountSuspended } from '@nuxt/test-utils/runtime'
import type { WebSocketStatus } from '@vueuse/core'
import { describe, it, expect, vi } from 'vitest'
import EditorPage from '~/pages/databases/[id]/editor.vue'
import { staticTableDocumentFixture } from '~~/test/__fixtures__'

vi.mock('~/components/editor/modals/EditTable.vue', async () => {
  return {
    default: defineComponent({
      name: 'ModalsEditTable',
      template: '<div data-testid="modals-edit-table"><slot /></div>'
    })
  }
})

vi.mock('~/components/editor/modals/AddDocument.vue', async () => {
  return {
    default: defineComponent({
      name: 'ModalsAddDocument',
      template: '<div data-testid="modals-add-document"><slot /></div>'
    })
  }
})

vi.mock('~/components/editor/modals/EditDocument.vue', async () => {
  return {
    default: defineComponent({
      name: 'ModalsEditDocument',
      template: '<div data-testid="modals-edit-document"><slot /></div>'
    })
  }
})

vi.mock('~/components/editor/modals/CreateTable.vue', async () => {
  return {
    default: defineComponent({
      name: 'ModalsCreateTable',
      template: '<div data-testid="modals-create-table"><slot /></div>'
    })
  }
})

mockNuxtImport('useRoute', original => vi.fn<typeof import('vue-router').useRouter>(original))

vi.mock('@vueuse/core', async () => {
  const actual = await vi.importActual<typeof import('@vueuse/core')>('@vueuse/core')
  return {
    ...actual,
    useWebSocket: vi.fn<typeof import('@vueuse/core')[ 'useWebSocket' ]>().mockImplementation((_url: MaybeRefOrGetter<string | URL | undefined>, _options: any) => {
      return {
        open: () => {},
        close: () => {},
        status: ref<WebSocketStatus>('CLOSED'),
        send: () => true,
        data: ref({ value: '' }),
        ws: ref(undefined)
      }
    })
  }
})

const actions = vi.hoisted(() => {
  const editButtonAction = vi.fn<() => void>(() => void 0)
  return {
    editButtonAction
  }
})

vi.mock('~/composables/use/tables/edition', async (original) => {
  const actual = await original<typeof import('~/composables/use/tables/edition')>()
  return {
    ...actual,
    useTableEditionComposable: vi.fn<typeof actual.useTableEditionComposable>().mockImplementation(() => {
      return {
        selectedTable: ref(staticTableDocumentFixture),
        tableData: ref([staticTableDocumentFixture]),
        hasDocuments: ref(true),
        hasData: ref(true),
        selectedTableDocument: ref(staticTableDocumentFixture),
        editableTableRef: ref(null),
        toggleEditTableDrawer: actions.editButtonAction
      }
    })
  }
})

describe.only('EditorPage', () => {
  it('should render page correctly', async () => {
    const component = await mountSuspended(EditorPage)
    expect(component).toBeDefined()
    console.log(component.html())
  })

  it('should call toggleEditTableDrawer when edit button is clicked', async () => {
    const component = await mountSuspended(EditorPage, {
      
    })
    const editButton = component.get('#edit-table')
    await editButton.trigger('click')
    expect(actions.editButtonAction).toHaveBeenCalled()
  })
})
