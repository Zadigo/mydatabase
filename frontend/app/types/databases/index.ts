import type { _BaseDatabaseObject, _BaseDatetimes } from '..'
import type { Table } from '../tables'

export type * from './endpoints'
export type * from './connections'

/**
 * A simplified version of the table type which does not include the
 * data stored by the documents for performance reasons
 */
export type SimpleTable = Pick<Table, 'id' | 'name' | 'description' | 'active_document_datasource' | 'component' | 'active' | 'documents'> & _BaseDatetimes

/**
 * A database is a collection of tables
 */
export interface Database extends _BaseDatabaseObject {
  /**
   * The name of the database
   */
  name: string
  /**
   * The list of tables in the database
   */
  tables: SimpleTable[]
  /**
   * Whether the database is active or not
   */
  active: boolean
  /**
   * Whether the database is paused or not. A paused database 
   * will not be used for queries, but will still be visible in 
   * the UI and can be resumed at any time.
   */
  paused: boolean
  database_functions: null
  database_triggers: null
  document_relationships: null
  /**
   * A slug is a URL-friendly version of the database name, typically used 
   * for routing and identification purposes in the frontend application.
   */
  slug: string
  /**
   * The timestamp of when the database was last updated, in ISO 8601 format. This field is used to 
   * track changes to the database and can be useful for caching and synchronization purposes.
   */
  updated_at: string
  /**
   * The timestamp of when the database was created, in ISO 8601 format. This field is used to
   *  track the creation time of the database and can be useful for auditing and historical purposes.
   */
  created_at: string
}
