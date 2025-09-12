export type BaseWsSendMessage =
  | { action: 'idle_connect' }
  | { action: 'load_via_id' }
  | { action: 'load_via_url', url: string, entry_key?: string }


interface DocumentData {
  document_data: string
  columns: {
    names: string[]
    options: ColumnOptions[]
    type_options: ColumnTypeOptions[]
  }
}

export type BaseReceiveWsAction =
  | { action: 'connected' } & DocumentData
  | { action: 'loaded_via_id' } & DocumentData
  | { action: 'loaded_via_url' } & DocumentData
  | { action: 'checkedout_url' | 'checkedout_file' } & DocumentData
  | { action: 'processing_url' }
  | { action: 'error' | 'success', message: string }

/**
 * WebSocket message utilities
 */
export function useWebsocketMessage() {
  function stringify<T extends BaseWsSendMessage>(message: T): string {
    return JSON.stringify(message)
  }

  function parse<M extends BaseReceiveWsAction>(message: string): M | undefined {
    try {
      return JSON.parse(message) as M
    } catch {
      return undefined
    }
  }

  const parseToRef = reactify(parse)

  return {
    /**
     * Helper function that allows us to 
     * stringify a WebSocket message
     */
    stringify,
    /**
     * Helper function that allows us to
     * parse WebSocket messages
     */
    parse,
    /**
     * Helper function that allows us to
     * parse WebSocket messages by returning a ref
     */
    parseToRef
  }
}
