import type { SimpleTable } from './tables'

export type * from './tables'

/**
 * A database is a collection of tables
 */
export interface Database {
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
