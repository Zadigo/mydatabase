export {
  useDatabaseCreation
} from './use'

/**
 * Get the WebSocket production domain URL
 * @param path The specific path to append to the base WebSocket URL
 */
export function useWsProdDomain(path: string) {
  const config = useRuntimeConfig()
  return `${config.public.wsProdDomain}/${path}`
}

/**
 * Composable used to truncate a string
 * @param value The string value to truncate
 * @param limit The amount to truncate the string by
 */
export function useTruncateString() {
  function truncate(value: string, limit: number = 50) {
    return `${value.substring(0, limit)}...`
  }
  return {
    truncate
  }
}
