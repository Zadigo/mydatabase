import { vi } from 'vitest'
import type { H3Event, EventHandlerRequest } from 'h3'

type Handler = (event: H3Event<EventHandlerRequest>) => Promise<unknown>

const h3 = vi.hoisted(() => {
  return {
    // <typeof import('h3')['defineEventHandler']>
    mockedDefinedHandler: vi.fn((handler: Handler) => handler)
  }
})

export function useH3TestUtils() {
  vi.stubGlobal('defineEventHandler', h3.mockedDefinedHandler)
  return h3
}

// const wsObject = vi.hoisted(() => {
//   return {
//     mockedWebSocket: vi.fn<typeof import('@vueuse/core')['useWebSocket']>()
//   }
// })
