import type { DocumentData } from '~/types'

/**
 * Store used to manage the state of table edition
 * accross multiple components aka which table is
 * being edited, what data in the table is being
 * manipulated etc.
 */
export const useTableEditionStore = defineStore('tableEdition', () => {
  const dbStore = useDatabasesStore()
  const { currentDatabase } = storeToRefs(dbStore)

  const selectedTableName = ref<string>()
  const selectedTable = computed(() => currentDatabase.value?.tables.find(table => table.name === selectedTableName.value))

  const tableDocuments = computed(() => selectedTable.value?.documents || [])
  const hasDocuments = computed(() => tableDocuments.value.length > 0)
  
  const selectedTableDataName = ref<string>()
  const selectedTableDataNames = computed(() => selectedTable.value?.documents.map(doc => doc.name) || [])

  const tableData = reactive<DocumentData[]>([])
  const hasData = computed(() => tableData.length > 0)

  return {
    /**
     * The current table
     */
    selectedTable,
    /**
     * The name of the selected table
     */
    selectedTableName,
    /**
     * The name of the selected document
     * for the current table
     */
    selectedTableDataName,
    /**
     * List of available documents by name
     */
    selectedTableDataNames,
    /**
     * The documents contained within the selected table
     */
    tableDocuments,
    /**
     * The actual data to use for the current table
     */
    tableData,
    /**
     * Whether the current table has any data
     */
    hasData,
    /**
     * Whether the current table has at least
     * one document linked to it
     */
    hasDocuments
  }
}, {
  persist: {
    pick: ['selectedTableName', 'selectedTableDataName'],
    storage: sessionStorage
  }
})
