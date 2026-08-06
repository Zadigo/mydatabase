import { describe, it, expect } from 'vitest'
import { useH3TestUtils } from '../../setup'
import { mockH3Event } from '../../__mocks__'

const { mockedDefinedHandler } = useH3TestUtils()

describe.todo('GET /funny-test', () => {
  it('is registered as an event handler', () => {
    expect(mockedDefinedHandler).toHaveBeenCalled()
  })

  it('should return a funny message', async () => {
    const handler = await import('~~/server/api/funny-test.get')

    const event = mockH3Event({ body: {} })
    const result = await handler.default(event)
    console.log(result)
    expect(result).toEqual('great')
  })
})
