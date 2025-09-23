import type { SimpleTable } from './databases'

export type * from './tables'
export type * from './databases'
export type * from './accounts'

export type Nullable<T> = T | null

export type Undefineable<T> = T | undefined

export type Arrayable<T> = T[]

export type RefOrUndefined<T> = Ref<Undefineable<T>>

export type MaybeTable = RefOrUndefined<SimpleTable>

export type PlainOrRef<T, M> = T | RefOrUndefined<M>

export type ReturnAny = Nullable<string | number | boolean>

export type Refeable<T> = T | Ref<T>

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
