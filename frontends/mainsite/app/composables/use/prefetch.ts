import type { Nullable } from '~/types'

type FileTypes = 'csv' | 'json'

type PrefetchOptions = {
  entryKey?: Nullable<string>
  fileType?: FileTypes
}

type WsMessage = Pick<PrefetchOptions, 'entryKey'> & {
  action: 'load_via_url' | (string & {})
}

type WsPrefetchOptions<R> = Pick<PrefetchOptions, 'entryKey' | 'fileType'> & {
  ws: ReturnType<typeof useWebSocket<R>>
  wsSendMessage: WsMessage
}

/**
 * 
 * @param entryKey 
 * @param fileType 
 */
function usePreviewer<T extends Record<string, unknown> = Record<string, unknown>>(entryKey?: Nullable<string>, fileType: FileTypes = 'json') {
  const initialData = ref<T | undefined>()

  const preview = computed(() => {
    // Check initialData.value instead of the ref object itself
    if (initialData.value !== undefined) {
      if (fileType === 'json' && entryKey) {
        // Safe type assertion because we are extracting a sub-key from the object
        return (initialData.value as Record<string, unknown>)[entryKey] as T
      } else {
        return initialData.value
      }
    }
    return undefined
  })

  return {
    initialData,
    preview
  }
}

/**
 * 
 * @param source
 * @param options
 */
export function urlPrefetchViaHttp<T extends Record<string, unknown> = Record<string, unknown>>(source: Ref<string | undefined>, options: PrefetchOptions) {
  const { entryKey, fileType = 'json' } = options
  const { initialData, preview } = usePreviewer<T>(entryKey, fileType)

  const headers: Record<string, string> = {
    'Accept': fileType === 'csv' ? 'text/csv' : 'application/json',
    'Content-Type': fileType === 'csv' ? 'text/csv' : 'application/json'
  }

  const { load } = useMemoize(async () => {
    const url = new URL(source.value || '')

    try {
      // Assert the $fetch type as T because runtime string URLs bypass Nitro's static route inference
      const data = await $fetch<unknown>(url.pathname, {
        method: 'GET',
        baseURL: url.origin,
        headers
      })
      console.log(data)
      return data as T
    } catch (error) {
      console.error('Error fetching data:', error)
      return undefined
    }
  })

  watchDebounced(source, async () => {
    if (isDefined(source)) {
      initialData.value = await load()
    }
  }, {
    immediate: false,
    debounce: 0
  })
  
  return preview
}

/**
 * 
 * @param source
 * @param options 
- */
export function urlPrefetchViaWebSocket<T = Record<string, unknown>>(source:  Ref<string | undefined>, options: WsPrefetchOptions<T>) {
  const { ws, wsSendMessage } = options
  const { preview, initialData } = usePreviewer<T>(options.entryKey, options.fileType)

  watchDebounced(source, async () => {
    ws.send(JSON.stringify(wsSendMessage))
    initialData.value = ws.data
  })

  return preview
}
