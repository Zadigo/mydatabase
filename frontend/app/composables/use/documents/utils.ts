import type { ColumnType, PlainOrRef, SimpleTable, TableDocument } from '~/types'
import type { NewDocument } from '.'

/**
 * Get the actual document from a table based on the `active_document_datasource`
 * field of the table
 * @param table The table to get the actual document from
 */
export function useTableActualDocument<T extends PlainOrRef<SimpleTable, SimpleTable>>(table: T) {
  const actualTable = ref<T>(table)
  const availableDocuments = computed(() => isDefined(actualTable) ? actualTable.value?.documents : [])
  return useArrayFind<TableDocument>(availableDocuments, (doc) => actualTable.value?.active_document_datasource === doc.document_uuid)
}

/**
 * Composable to get options related to column types
 */
export function useColumnTypeOptions() {
  function getTypeIcon(columnType: ColumnType) {
    let icon: string = 'i-lucide-a-large-small'

    switch (columnType) {
      case 'String':
        icon = 'i-lucide-a-large-small'
        break

      case 'Number':
        icon = 'i-lucide-superscript'
        break

      case 'Array':
        icon = 'i-lucide-brackets'
        break

      case 'Boolean':
        icon = 'i-lucide-check'
        break

      case 'Date':
        icon = 'i-lucide-calendar'
        break

      case 'DateTime':
        icon = 'i-lucide-calendar-clock'
        break

      case 'Dict':
        icon = 'i-lucide-braces'
        break

      default:
        icon = 'i-lucide-a-large-small'
        break
    }

    return icon
  }

  function getTypeOptions(headers: string[]): NewDocument['using_columns'] {
    return toReactive(headers.map((h) => ({
      name: h,
      new_name: h,
      columnType: 'String',
      unique: false,
      nullable: true,
      visible: true
    })))  
  }

  return {
    /**
     * Helper function to get the icon for a certain column type
     * @default "i-lucide-a-large-small"
     */
    getTypeIcon,
    /**
     * Helper function to get the type options
     * for a list of columns
     */
    getTypeOptions
  }
}
