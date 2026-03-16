import type { Arrayable, ColumnOptions, ColumnTypeOptions, Empty, Nullable, Undefineable } from '~/types'

interface DocumentData {
  document_data: string
  columns: {
    names: Arrayable<string>
    options: Arrayable<ColumnOptions>
    type_options: Arrayable<ColumnTypeOptions>
  }
}

export type BaseWsSendMessage =
  | { action: 'idle_connect' }
  | { action: 'load_via_id', table_id: number, document: { id: number, name: string } }
  | { action: 'load_via_url', url: string, entry_key?: Nullable<string> }
  | { action: 'load_document_data', document_uuid: Undefineable<string> }

export type BaseReceiveWsAction =
  | { action: 'connected' } & DocumentData
  | { action: 'loaded_via_id' } & DocumentData
  | { action: 'loaded_via_url' } & DocumentData
  | { action: 'checkedout_url' | 'checkedout_file' } & Omit<DocumentData, 'document_data'>
  | { action: 'processing_url' }
  | { action: 'error' | 'success', message: string }
  | { action: 'loaded_document_data', data: string }

/**
 * WebSocket message utilities
 */
export function useWebsocketMessage<S extends BaseWsSendMessage, R extends BaseReceiveWsAction>() {
  function stringify(message: S): string {
    return JSON.stringify(message)
  }

  function parse(message: MaybeRef<Empty<string>>): R | undefined {
    try {
      return JSON.parse(toValue(message) || '') as R
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
