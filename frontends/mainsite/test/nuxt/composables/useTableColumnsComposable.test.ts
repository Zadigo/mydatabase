import { describe, it, expect, vi, beforeEach } from 'vitest'
// import {  useTableColumnsComposable} from '~/composables/use/tables/edition'
import { staticTableDocumentFixture } from '~~/test/__fixtures__'

vi.mock('~/composables/use/tables/edition', async (original) => {
  const actual = await original<typeof import('~/composables/use/tables/edition')>()
  return {
    ...actual,
    useTableEditionComposable: vi.fn(() => ({
      selectedTableDocument: ref([])
    }))
  }
})

describe.todo('useTableColumnsComposable', () => {
  // beforeEach(() => {
  //   vi.resetModules()
  // })

  it('should return default properties', async () => {
    const { useTableColumnsComposable } = await import('~/composables/use/tables/edition')

    const defaults = useTableColumnsComposable()

    expect(defaults).toHaveProperty('columnNames')
    expect(defaults).toHaveProperty('columnOptions')
    expect(defaults).toHaveProperty('columnTypeOptions')
    expect(defaults).toHaveProperty('toggleOption')
    expect(defaults).toHaveProperty('changeTypeOption')
    expect(defaults).toHaveProperty('toggleConstraint')
    expect(defaults).toHaveProperty('save')

    expect(defaults.toggleOption).toBeInstanceOf(Function)
    expect(defaults.changeTypeOption).toBeInstanceOf(Function)
    expect(defaults.toggleConstraint).toBeInstanceOf(Function)
    expect(defaults.save).toBeInstanceOf(Function)

    console.log(defaults.columnNames.value)
  })
})
