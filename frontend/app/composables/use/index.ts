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
