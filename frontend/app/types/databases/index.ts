import type { _BaseDatabaseObject, _BaseDatetimes } from '..'
import type { Table } from '../tables'

export type * from './endpoints'

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
}
