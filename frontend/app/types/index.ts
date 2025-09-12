import type { SimpleTable } from './tables'

export type * from './tables'

export type MaybeTable = MaybeRef<SimpleTable | undefined>

export type ReturnAny = string | number | boolean | null

export type Nullable<T> = T | null

/**
 * @private
 */
export interface _BaseDatetimes {
  updated_at: string
  created_at: string
}

/**
 * A database is a collection of tables
 */
export interface Database extends _BaseDatetimes {
  id: number
  /**
   * The name of the database
   */
  name: string
  /**
   * The list of tables in the database
   */
  tables: SimpleTable[]
}
