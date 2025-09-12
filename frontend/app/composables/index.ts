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
 */
export function useTruncateString() {
  function truncate(value: string, limit: number = 50) {
    return `${value.substring(0, limit)}...`
  }

  const truncated = reactify(truncate)

  return {
    truncated,
    /**
     * Truncates a string to the specified limit and appends ellipsis
     * @param value The string value to truncate
     * @param limit The maximum length of the string before truncation (default is 50)
     */
    truncate
  }
}
