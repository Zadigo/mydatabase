import type { SimpleTable, TableDocument } from '~/types'
import { useWebsocketMessage } from '..'

/**
 * Composable to manage the WebSocket connection for live
 * table data editing
 * 
 * @description Using websocket for these operations is
 * faster and more efficient especially when dealing with big
 * datasets. Also, websockets allow for collaborative editing
 * that we will implement in future releases
 * 
 * @param table The table to edit
 */
export function useTableWebocketManager(selectedTable: Ref<SimpleTable | undefined>, selectedDocument: Ref<TableDocument | undefined>) {
  const config = useRuntimeConfig()
  const { stringify, parse } = useWebsocketMessage()

  const tableEditionStore = useTableEditionStore()
  const { tableData } = storeToRefs(tableEditionStore)

  const wsObject = useWebSocket(`${config.public.wsProdDomain}/ws/documents`, {
    immediate: false,
    onConnected(ws) {
      ws.send(stringify({ action: 'idle_connect' }))
    },
    onMessage(ws, event) {
      const data = parse(event.data)
      console.log('String data', data)

      if (data) {
        switch (data.action) {
          case 'loaded_via_id':
            if (data.document_data) {
              console.log('Parsed data', JSON.parse(data.document_data))
              tableData.value = JSON.parse(data.document_data)
            }
            
            // TODO: Remove this now comes directly within
            // the API when loading the databases
            // if (data.columns) {
            //   columnNames.value = data.columns.names
            //   columnOptions.value = data.columns.options
            //   columnTypeOptions.value = data.columns.type_options
            // }
            break

          default:
            console.error(`Action not identified: ${JSON.stringify(data)}`)
            break
        }
      }
    }
  })

  function loadDataViaId() {
    if (isDefined(selectedTable) && isDefined(selectedDocument)) {
      wsObject.send(stringify({
        action: 'load_via_id',
        table_id: selectedTable.value.id,
        document: {
          id: selectedDocument.value.id,
          name: selectedDocument.value.name
        }
      }))
    }
  }

  onMounted(() => {
    wsObject.open()
    loadDataViaId()
  })

  onUnmounted(() => {
    wsObject.close()
  })

  /**
   * Every time the selected document changes, 
   * send a WebSocket message to load inner
   * data contained within it
   */
  watchDebounced(selectedDocument, () => {
    loadDataViaId()
  }, {
    debounce: 300
  })

  return {
    wsObject
  }
}
