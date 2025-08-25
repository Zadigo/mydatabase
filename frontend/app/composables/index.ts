export {
  useTable,
  useTableColumns
} from './use'

/**
 * Get the WebSocket production domain URL
 * @param path The specific path to append to the base WebSocket URL
 */
export function useWsProdDomain(path: string) {
  const config = useRuntimeConfig()
  return `${config.public.wsProdDomain}/${path}`
}
