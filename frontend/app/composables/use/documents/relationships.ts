/**
 * Composable used for editing the relationships between documents
 */
export function useEditDocumentRelationship() {
  function create() {
    // Do something
  }

  const tableEditionStore = useTableEditionStore()
  const { tableDocuments, selectedTableDocument } = storeToRefs(tableEditionStore)

  // const availableDocuments = computed(() => useArrayFilter(tableDocuments, (doc) => doc.document_uuid !== selectedTableDocument.value?.document_uuid).value)

  /**
   * Columns
   */

  const primaryKey = ref<string>()
  const foreignTableId = ref<string>()
  const foreignTableForeignKey = ref<string>()

  const primaryKeyColumns = computed(() => isDefined(selectedTableDocument) ? selectedTableDocument.value.column_names : [])
  const foreignTable = useArrayFind(tableDocuments, (doc) => doc.document_uuid === foreignTableId.value)
  const foreignTableColumns = computed(() => isDefined(foreignTable) ? foreignTable.value.column_names : [])

  return {
    primaryKeyColumns,
    foreignTableColumns,
    availableDocuments: tableDocuments,
    /**
     * The primary key of the current document
     */
    primaryKey,
    /**
     * The foreign table id of the related document
     */
    foreignTableId,
    /**
     * The foreign key of the related document
     */
    foreignTableForeignKey,
    /**
     * Creates the relationship between two documents
     */
    create
  }
}

