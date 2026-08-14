import { describe, it, expect, vi } from 'vitest'
import { _useDatabases } from '~/composables/use/databases'
import { mockNuxtImport } from '@nuxt/test-utils/runtime'
import { databaseFixture, tableFixture } from '~~/test/__fixtures__'
import type { Database } from '~/types/api/databases'
import { definedTestCases } from '~~/test/__mocks__'

vi.mock('@vueuse/core', async (original) => {
  const actual = await original<typeof import('@vueuse/core')>()
  return {
    ...actual
  }
})

const { mockedFetch, mockedRouter } = vi.hoisted(() => {
  const mockedFetch = vi.fn(async (url: string, options: any) => {
    if (url === '/api/databases' && options.method === 'GET') {
      return [databaseFixture]
    }

    return undefined
  })

  const mockedRouter = vi.fn<typeof import('vue-router').useRoute>(() => ({
    params: {
      id: '1'
    }
  }))

  return { mockedFetch, mockedRouter }
})

mockNuxtImport('$fetch', () => mockedFetch)
mockNuxtImport('useRoute', async () => mockedRouter)

describe('useDatabasesComposable', () => {
  it('should return default properties', () => {
    const defaults = _useDatabases()

    expect(defaults).toHaveProperty('allTableDocuments')
    expect(defaults).toHaveProperty('databases')
    expect(defaults).toHaveProperty('routeId')
    expect(defaults).toHaveProperty('search')
    expect(defaults).toHaveProperty('searched')
    expect(defaults).toHaveProperty('currentDatabase')
    expect(defaults).toHaveProperty('availableTables')
    expect(defaults).toHaveProperty('availableTableNames')
    expect(defaults).toHaveProperty('hasTables')

    expect(defaults.databases.value).toEqual([])
  })

  const testCases = definedTestCases((manager) => {
    return manager.parameterize(
      [
        {
          title: 'with search "Test Database"',
          testValue: 'Test Database',
          expectedLength: 1,
        },
        {
          title: 'with search ""',
          testValue: '',
          expectedLength: 1,
        }
      ]
    )
  })

  testCases.runner.forEach((testCase) => {
    it(`should be able to search for databases: ${testCase.title}`, async () => {
      mockedFetch.mockResolvedValueOnce([databaseFixture])
  
      const defaults = _useDatabases()
      
      defaults.search.value = testCase.testValue as string
      await nextTick()
      
      expect(defaults.searched.value).toHaveLength(testCase.expectedLength as number)
      expect(defaults.searched.value[0]?.name).toBe('Test Database')
    })
  })

  it('should have current database to "1" and currenDatabase set', () => {
    const defaults = _useDatabases()
    
    console.log(defaults.databases.value)

    expect(isDefined(defaults.currentDatabase)).toBeDefined()
    expect(defaults.currentDatabase.value?.id).toBe(1)
    expect(toValue(defaults.hasTables)).toBe(false)
    expect(toValue(defaults.allTableDocuments)).toEqual([])
  })

  it('should have current database to undefined when route is invalid', () => {
    mockedRouter.mockReturnValueOnce({
      params: {
        databaseId: '999'
      }
    })

    const defaults = _useDatabases()

    expect(toValue(defaults.availableTables)).toEqual([])
    expect(toValue(defaults.availableTableNames)).toEqual([])
    expect(toValue(defaults.hasTables)).toBeFalsy()
    expect(toValue(defaults.allTableDocuments)).toEqual([])
  })

  it.todo('should return current tables and table names when current database is set', () => {
    const fixture: Database = {
      ...databaseFixture,
       tables: [
          tableFixture
       ]
    }

    mockedFetch.mockImplementation(async (url, options) => {
      if (url === '/api/databases' && options.method === 'GET') {
        return [fixture]
      }
    })

    const defaults = _useDatabases()
    console.log(toValue(defaults.databases))

    expect(toValue(defaults.currentDatabase)).toBeDefined()
    expect(toValue(defaults.availableTableNames)).toEqual([tableFixture.name])
  })
})
