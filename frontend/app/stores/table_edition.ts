/**
 * Store used to manage the state of table edition
 * accross multiple components
 */
export const useTableEditionStore = defineStore('tableEdition', () => {
  const dbStore = useDatabasesStore()
  const { currentDatabase } = storeToRefs(dbStore)

  const selectedTableName = ref<string>()
  const selectedTable = computed(() => currentDatabase.value?.tables.find(table => table.name === selectedTableName.value))

  const tableDocuments = computed(() => selectedTable.value?.documents || [])
  const hasData = computed(() => tableDocuments.value.length > 0)
  
  /** Only fetch the first item for now. In the future we need to deal with multiple data from different documents*/
  // const tableData = computed(() => hasData.value && tableDocuments.value.map(doc => doc.data).flat() || [])
  const selectedTableDataName = ref<string>()
  const selectedTableDataNames = computed(() => selectedTable.value?.documents.map(doc => doc.name) || [])
  const tableData = computed(() => tableDocuments.value.find(doc => doc.name === selectedTableDataName.value)?.data || [])

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
     * The data to use for the current table
     */
    tableData,
    /**
     * Whether the current table has data
     */
    hasData
  }
}, {
  persist: {
    pick: ['selectedTableName', 'selectedTableDataName'],
    storage: sessionStorage
  }
})
