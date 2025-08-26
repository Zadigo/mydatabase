import type { DropdownMenuItem } from '@nuxt/ui'

export {
  useTable,
  useTableColumns
} from './tables'

export {
  useDatabaseCreation
} from './databases'


/**
 * Transforms an array of strings into an array of menu items
 * that can be used in Nuxt UI dropdown elements
 * @param data The strings to convert
 */
export function useToMenuItems<T = DropdownMenuItem[]>(data: string[]) {
  const items = ref<T>(data.map(item => ({ label: item })))

  return {
    items
  }
}

/**
 * WebSocket message utilities
 */
export function useWebsocketMessage() {
  function stringify<T = Record<string, unknown>>(message: T): string {
    return JSON.stringify(message)
  }

  function parse<M>(message: string): M | undefined {
    try {
      return JSON.parse(message) as M
    } catch {
      return undefined
    }
  }

  return {
    /**
     * Stringify a WebSocket message
     */
    stringify,
    /**
     * Parse a WebSocket message
     */
    parse
  }
}
