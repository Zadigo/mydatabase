import type { SimpleTable, TableDocument } from '~/types'
import type { BaseReceiveWsAction } from '..'
import { useWebsocketMessage } from '..'

/**
 * Composable to manage the WebSocket connection for live
 * table data editing
 * 
 * @description Using websocket for these operations is
 * faster and more efficient especially when dealing with big
 * datasets. Also, websockets allow for collaborative editing
 * that we will implement in future releases
 * @param selectedTable The table to edit
 * @param selectedDocument The document to edit
 */
export const useTableWebocketManager = createGlobalState((selectedTable: Ref<SimpleTable | undefined>, selectedDocument: Ref<TableDocument | undefined>) => {
  const config = useRuntimeConfig()
  const { stringify, parse } = useWebsocketMessage()

  const dbStore = useDatabasesStore()
  const { currentDatabase } = storeToRefs(dbStore)

  const tableEditionStore = useTableEditionStore()
  const { tableData } = storeToRefs(tableEditionStore)

  const wsObject = useWebSocket<BaseReceiveWsAction>(`${config.public.wsProdDomain}/ws/databases/${currentDatabase.value?.id}/documents`, {
    immediate: false,
    onMessage(ws, event: MessageEvent<string>) {
      const data = parse(event.data)

      if (isDefined(data)) {
        if (data.action === 'loaded_via_id' && data.document_data) {
          console.log('Parsed data', JSON.parse(data.document_data))
          tableData.value = JSON.parse(data.document_data)
        }

        if (data.action === 'error') {
          console.error('WebSocket error:', data.message)
        }

        if (data.action === 'loaded_document_data') {
          tableData.value = JSON.parse(data.data)
        }
      } else {
        console.error('Failed to parse WebSocket message:', event.data)
      }
    },
    onError(ws, event) {
      console.error('WebSocket error:', event)
    }
  })

  function loadDataViaId() {
    if (isDefined(selectedTable) && isDefined(selectedDocument)) {
      wsObject.send(
        stringify({
          action: 'load_via_id',
          table_id: selectedTable.value.id,
          document: {
            id: selectedDocument.value.id,
            name: selectedDocument.value.name
          }
        })
      )
    }
  }

  const isConnected = computed(() => wsObject.status.value === 'OPEN')  

  onMounted(() => { loadDataViaId() })
  onUnmounted(() => { if (isConnected.value) wsObject.close() })

  /**
   * Every time the selected document changes, 
   * send a WebSocket message to load the inner data
   */
  watchDebounced(selectedDocument, () => {
    loadDataViaId()
  }, {
    debounce: 300
  })

  return {
    wsObject,
    isConnected
  }
})
