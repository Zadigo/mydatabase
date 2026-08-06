import { describe, it, expect, beforeEach, vi } from 'vitest'
import { useDatabaseCreation } from '~/composables'
import { useDatabasesStore } from '~/stores/databases'
import { setActivePinia, createPinia, storeToRefs } from 'pinia'
import { useRuntimeConfig } from 'nuxt/app'
import { mockNuxtImport } from '@nuxt/test-utils/runtime'
import type { $Fetch, NitroFetchRequest, NitroFetchOptions } from 'nitropack'

import type { NewDatabase } from '~/composables'

const newDatabase: NewDatabase = {
  name: 'Test Database',
  description: 'Some easy description'
}

// tables: [],
// active: true,
// paused: false,
// database_functions: null,
// database_triggers: null,
// document_relationships: null,
// slug: 'test-database',
// updated_at: new Date().toISOString(),
// created_at: new Date().toISOString()

vi.stubGlobal('useRuntimeConfig', () => ({
  public: {
    prodDomain: 'https://api.mydatabase.com'
  }
}))

const { fetchMock } = vi.hoisted(() => {
  const fetchMock = vi.fn<$Fetch>(async (_url: NitroFetchRequest, _options: NitroFetchOptions) => {
    if (_url === '/v1/databases/create' && _options.method === 'POST') {
      return newDatabase
    }
    throw new Error('Unknown endpoint or method')
  })

  return { fetchMock }
})

mockNuxtImport('$fetch', () => fetchMock)

describe('useDatabaseCreation', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('should initialize with default params', () => {
    const result = useDatabaseCreation()

    expect(result).toBeDefined()

    expect(result.newDatabase.value).toBeTruthy()
    expect(result.showModal.value).toBeFalsy()
    expect(result.newDatabase.value).toEqual({ name: '', description: '' })
    expect(result.create).toBeInstanceOf(Function)
  })

  it('should create a new database and reset the form', async () => {
    // fetchMock.mockReturnValue(newDatabase)
    // fetchMock.mockResolvedValue(newDatabase)
    // fetchMock.mockImplementation(() => Promise.resolve(newDatabase))

    const result = useDatabaseCreation()
    result.newDatabase.value = {
      name: 'Test Database',
      description: 'Some easy description'
    }
    
    await result.create()

    expect(fetchMock).toHaveBeenCalledWith('/v1/databases/create', {
      method: 'POST',
      body: {
        name: 'Test Database',
        description: 'Some easy description'
      },
      baseURL: useRuntimeConfig().public.prodDomain
    })
    expect(result.newDatabase.value).toEqual({ name: '', description: '' })

    const store = useDatabasesStore()
    const { databases } = storeToRefs(store)
    expect(databases.value.length).toBe(1)
  })
})
