import { describe, it, expect, beforeEach, vi } from 'vitest'
import { useDatabaseCreation } from '~/composables'
import { setActivePinia, createPinia } from 'pinia'
import { mockNuxtImport } from '@nuxt/test-utils/runtime'
import type { $Fetch, NitroFetchRequest, NitroFetchOptions } from 'nitropack'
import { databaseFixture } from '~/data/__fixtures__'

import type { NewDatabase } from '~/composables'

const newDatabase: NewDatabase = {
  name: 'Test Database',
  description: 'Some easy description'
}

vi.stubGlobal('useRuntimeConfig', () => ({
  public: {
    prodDomain: 'https://api.mydatabase.com'
  }
}))

const { fetchMock } = vi.hoisted(() => {
  const fetchMock = vi.fn<$Fetch>(async (url: NitroFetchRequest, options: NitroFetchOptions) => {
    if (url === '/api/databases' && options.method === 'POST') {
      return [databaseFixture]
    }

    if (url === '/api/databases/create' && options.method === 'POST') {
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
    const result = useDatabaseCreation()
    result.newDatabase.value = {
      name: 'Test Database',
      description: 'Some easy description'
    }
    
    await result.create()

    // expect(fetchMock).toHaveBeenCalledWith('/api/databases/create', {
    //   method: 'POST',
    //   body: {
    //     name: 'Test Database',
    //     description: 'Some easy description'
    //   }
    // })
    // expect(result.newDatabase.value).toEqual({ name: '', description: '' })

    const { databases } = _useDatabases() 
    expect(databases.value.length).toBe(1)
  })
})
