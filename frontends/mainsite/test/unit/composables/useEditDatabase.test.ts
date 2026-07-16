import { describe, it, expect, vi } from 'vitest'
import { useEditDatabase } from '../../../app/composables'
import { defineComponent, ref } from 'vue'
import { mountSuspended } from '@nuxt/test-utils/runtime'
import { databaseStaticFixture } from '../../__fixtures__/database'
import { useRuntimeConfig } from 'nuxt/app'

vi.stubGlobal('useRuntimeConfig', () => {
  return {
    public: {
      prodDomain: 'https://example.com'
    }
  }
})

const fetchMock = vi.fn(async (url: string, options: any) => {
  if (url === `/v1/databases/${databaseStaticFixture.id}` && options.method === 'POST') {
    return {
      ...databaseStaticFixture,
      name: options.body.name
    }
  }
  throw new Error('Unknown endpoint or method')
})

vi.stubGlobal('$fetch', fetchMock)

describe('useEditDatabase', () => {
  it('should initialize with default params', () => {
    const result = useEditDatabase(ref(databaseStaticFixture))
    expect(result).toBeDefined()
    expect(result.newDatabaseName.value).toBe(databaseStaticFixture.name)
  })

  it('should update the database name when newDatabaseName changes', async () => {
    const component = await mountSuspended(defineComponent({
      template: `
      <div>
        <input v-model="newDatabaseName" />
      </div>
      `,
      setup() {
        const { newDatabaseName } = useEditDatabase(ref(databaseStaticFixture))
        return {
          newDatabaseName
        }
      }
    }))

    component.vm.$nextTick() // Wait for the component to render
    expect(component).toBeDefined()

    const inputEl = component.find('input')
    expect(inputEl.exists()).toBe(true)

    const newName = 'Updated Database Name'
    await inputEl.setValue(newName)

    // Wait for the debounce to trigger the update
    await new Promise(resolve => setTimeout(resolve, 1500))

    expect(fetchMock).toHaveBeenCalledWith(`/v1/databases/${databaseStaticFixture.id}`, {
      baseURL: useRuntimeConfig().public.prodDomain,
      method: 'POST',
      body: {
        name: newName
      }
    })
  })
})
