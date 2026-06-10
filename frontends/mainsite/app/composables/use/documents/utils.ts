import type { ColumnType, SimpleTable, TableDocument } from '~/types'
import type { NewDocument } from '.'

/**
 * Find the actual document from a table based on its 
 * `active_document_datasource` field
 * @param table The table to get the actual document from
 */
export function useTableActualDocument<T extends MaybeRef<SimpleTable>>(table: T) {
  const actualTable = toValue(table)
  const availableDocuments = computed(() => actualTable.documents || [])
  return useArrayFind<TableDocument>(availableDocuments, (doc) => actualTable.active_document_datasource === doc.document_uuid)
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
