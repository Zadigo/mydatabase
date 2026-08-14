import { vi } from 'vitest'
import type { H3Event, EventHandlerRequest } from 'h3'
import type { WebSocketStatus } from '@vueuse/core'

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

vi.mock('@vueuse/core', async () => {
  const actual = await vi.importActual<typeof import('@vueuse/core')>('@vueuse/core')
  return {
    ...actual,
    useWebSocket: vi.fn<typeof import('@vueuse/core')[ 'useWebSocket' ]>().mockImplementation((_url: MaybeRefOrGetter<string | URL | undefined>, _options: any) => {
      return {
        open: () => { },
        close: () => { },
        status: ref<WebSocketStatus>('CLOSED'),
        send: () => true,
        data: ref({ value: '' }),
        ws: ref(undefined)
      }
    })
  }
})
