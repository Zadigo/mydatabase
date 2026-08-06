import { describe, it, expect } from 'vitest'
import { useEditDatabaseFunction } from '~/composables'
import { datatabaseFunctionFixture, databaseFixture } from '../../__fixtures__'

describe('useEditDatabaseFunction', () => {
  it('should initialize with default params', () => {
    const funcs = ref([datatabaseFunctionFixture])
    const database = ref(databaseFixture)
    const func = ref(datatabaseFunctionFixture)
    
    const result = useEditDatabaseFunction(funcs, database, func)
    expect(result).toBeDefined()
  })
})
