import type { SimpleTable } from './databases'

export type * from './tables'
export type * from './databases'

export type Nullable<T> = T | null

export type Undefineable<T> = T | undefined

export type Empty<T> = Nullable<T> | Undefineable<T>

export type Arrayable<T> = T[]

export type RefOrUndefined<T> = Ref<Undefineable<T>>

export type MaybeTable = RefOrUndefined<SimpleTable>

export type ReturnAny = Nullable<string | number | boolean>

export type Refeable<T> = T | Ref<T>

export type VueUseWsReturnType = ReturnType<typeof import('@vueuse/core').useWebSocket>

/**
 * @private
 */
export interface _BaseDatetimes {
  updated_at: string
  created_at: string
}

/**
 * @private
 */
export interface _BaseDatabaseObject extends _BaseDatetimes {
  id: number
}
