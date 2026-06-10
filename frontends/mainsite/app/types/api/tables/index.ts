import type { Nullable } from '~/types'
import type { _BaseDatabaseObject } from '..'
import type { ColumnOptions, ColumnTypeOptions, ColumnTypes } from './columns'

export type * from './columns'

export type DocumentData = Record<string, unknown>

/**
 * A document represents a details about
 * an Excel/Google sheet with the data that
 * is contained within that sheet
 */
export interface TableDocument extends _BaseDatabaseObject {
  /**
   * The name of the document
   */
  name: string
  /**
   * The unique identifier for the document
   */
  document_uuid: string
  /**
   * The names of the columns present
   * in the document
   */
  column_names: string[]
  /**
   * The column options used for this document
   * @default []
   */
  column_options: ColumnOptions[]
  /**
   * The column type options used for this document
   * @default []
   */
  column_types: ColumnTypes[]
  /**
   * The column type options used for this document
   * @default []
   */
  column_type_options: ColumnTypeOptions[]
}

export type TableComponent = 'data-table' | 'graph-table'

export interface Table extends _BaseDatabaseObject {
  /**
   * The name of the table
   */
  name: string
  /**
   * A description for the table
   * @default null
   */
  description: string
  /**
   * The UUID of the document which contains the data
   * that the table is supposed to return
   * @default null
   */
  active_document_datasource: Nullable<string>
  /**
   * The component used to display the data for the given table
   * @default "data-table"
   */
  component: TableComponent
  /**
   * Whether the table is currently active
   * @default true
   */
  active: boolean
  /**
   * The list of Excel/Google sheets associated with this table
   */
  documents: TableDocument[]
}
