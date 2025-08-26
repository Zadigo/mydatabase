import type { Table } from '~/types'
import { useWebsocketMessage } from '..'

/**
 * Composable to manage the WebSocket connection for live
 * table data editing
 * @param table The table to edit
 */
export function useTableWebocketManager(editableTableRef: Ref<Table | undefined>) {
  const config = useRuntimeConfig()
  const { stringify } = useWebsocketMessage()

  const wsobject = useWebSocket(`${config.public.wsProdDomain}/ws/documents`, {
    immediate: true,
    onConnected(ws) {
      ws.send(stringify({ action: 'idle_connect' }))
    }
  })

  // onMounted(() => {
  //   wsobject.open()
  // })

  // onUnmounted(() => {
  //   wsobject.close()
  // })

  return {
    wsobject
  }
}
