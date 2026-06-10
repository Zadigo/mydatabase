import type { SimpleTable } from './api/databases'

export type * from './api'

export type Nullable<T> = T | null

export type Undefineable<T> = T | undefined

export type Empty<T> = Nullable<T> | Undefineable<T>

export type Arrayable<T> = T[]

export type RefOrUndefined<T> = Ref<Undefineable<T>>

export type MaybeTable = RefOrUndefined<SimpleTable>

export type Refeable<T> = T | Ref<T>

export type VueUseWsReturnType = ReturnType<typeof import('@vueuse/core').useWebSocket>
