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

// TODO: When listing databases, I do not want to load the "data" field in documents
export type SimpleTable = Pick<Table, 'id' | 'name' | 'description' | 'active_document_datasource' | 'component' | 'active' | 'documents'> & _BaseDatetimes

export type TableComponent = 'data-table' | 'graph-table'
