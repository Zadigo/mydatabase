import { describe, it, expect } from 'vitest'
import { useDatabaseFunction, useDatabaseFunctions } from '~/composables'
import { datatabaseFunctionFixture } from '../../__fixtures__'

describe('useDatabaseFunctions', () => {
  it('should initialize with default params', () => {
    const result = useDatabaseFunctions()
    expect(result.create).toBeTypeOf('function')
  })
})

describe('useDatabaseFunction', () => {
  it('should initialize with default params', () => {
    const funcs = ref([datatabaseFunctionFixture])
    const func = ref(datatabaseFunctionFixture)

    const result = useDatabaseFunction(funcs, func)
    expect(result).toBeUndefined()
  })
})
