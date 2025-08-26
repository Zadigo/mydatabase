export type SendWsAction = 'idle_connect' | 'load_via_id' | 'load_via_url'

export type ReceiveWsAction = 'loaded_via_id' | 'connected' | 'loaded_via_url' | 'error'

export type AllWsAction = SendWsAction | ReceiveWsAction

export interface BaseWsSendMessage {
  action: SendWsAction
  url: string
  table_id: string | number
  document: {
    id: number
    name: string
  }
}

export interface BaseWsReceiveMessage {
  action: ReceiveWsAction,
  message: string
  
  document_id: number
  /**
   * The actual document's data
   */
  document_data: string

  /**
   * Metadata on the columns returned
   * from the underlying data
   */
  columns: {
    names: string[]
    options: ColumnOptions[]
    type_options: ColumnTypeOptions[]
  }
}

/**
 * WebSocket message utilities
 */
export function useWebsocketMessage() {
  function stringify<T extends Partial<BaseWsSendMessage>>(message: T): string {
    return JSON.stringify(message)
  }

  function parse<M extends Partial<BaseWsReceiveMessage>>(message: string): M | undefined {
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
