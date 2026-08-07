import type { Nullable } from '~/types'

type FileTypes = 'csv' | 'json'

type PrefetchOptions = {
  url: string
  entryKey?: Nullable<string>
  fileType?: FileTypes
}

type WsMessage = Pick<PrefetchOptions, 'entryKey'> & {
  action: 'load_via_url' | (string & {})
  url: string
}

type WsPrefetchOptions<R> = Pick<PrefetchOptions, 'entryKey' | 'fileType'> & {
  ws: ReturnType<typeof useWebSocket<R>>
  wsSendMessage: WsMessage
}

function usePreviewer<T>(entryKey?: Nullable<string>, fileType: FileTypes = 'json') {
  const initialData = ref<T>()

  const preview = computed(() => {
    if (isDefined(initialData)) {
      if (fileType == 'json' && isDefined(entryKey)) {
        return initialData.value[entryKey]
      } else {
        return initialData.value
      }
    } else {
      return undefined
    }
  })

  return {
    preview,
    initialData
  }
}

/**
 * 
 * @param source
 * @param options
 */
export function urlPrefetchViaHttp<T = Record<string, string>, S = string>(source: Ref<S>, options: PrefetchOptions) {
  const { url, entryKey, fileType = 'json' } = options
  const _initialData = ref<T>()

  const headers: Record<string, string> = {
    'Accept': fileType === 'csv' ? 'text/csv' : 'application/json',
    'Content-Type': fileType === 'csv' ? 'text/csv' : 'application/json'
  }

  const config = useRuntimeConfig()

  const { load } = useMemoize(async () => {
    return await $fetch<T>(url, {
      method: 'GET',
      baseURL: config.public.prodDomain,
      headers
    })
  })

  watchDebounced(source, async () => {
    try {
      _initialData.value = await load()
    } catch (error) {
      console.error(error)
    }
  })

  const preview = computed(() => {
    if (isDefined(_initialData)) {
      if (fileType == 'json' && isDefined(entryKey)) {
        return _initialData.value[entryKey]
      } else {
        return _initialData.value
      }
    } else {
      return undefined
    }
  })

  return preview
}

/**
 * 
 * @param source
 * @param options 
- */
export function urlPrefetchViaWebSocket<S extends string = string, T = unknown>(source: Ref<S>, options: WsPrefetchOptions<T>) {
  const { ws, wsSendMessage } = options
  const { preview, initialData } = usePreviewer(options.entryKey, options.fileType)

  watchDebounced(source, async () => {
    ws.send(JSON.stringify(wsSendMessage))
    initialData.value = ws.data
  })

  return preview
}


urlPrefetchViaWebSocket('', {

})
