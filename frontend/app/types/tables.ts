import type { _BaseDatetimes } from '.'

export type DocumentData = Record<string, unknown>

/**
 * A document represents a details about
 * an Excel/Google sheet with the data that
 * is contained within that sheet
 */
export interface TableDocument extends _BaseDatetimes {
  id: number
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
  column_types: ColumnTypeOptions[]
}

export interface Table extends _BaseDatetimes {
  id: number
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
  active_document_datasource: string | null
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

/**
 * A simplified version of the table type which does not include the
 * data stored by the documents for performance reasons
 */
export type SimpleTable = Pick<Table, 'id' | 'name' | 'description' | 'active_document_datasource' | 'component' | 'active' | 'documents'> & _BaseDatetimes

export type TableComponent = 'data-table' | 'graph-table'
