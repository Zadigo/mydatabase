import type { ColumnTypeOptions, Nullable } from '~/types'

export * from './edition'
export * from './reader'
export * from './relationships'
export * from './utils'

export interface NewDocument {
  /**
   * The name of the document under which the document
   * will be stored in the table
   */
  name: string
  /**
   * The url of the document to import data from
   * @default ""
   */
  url: string
  /**
   * The column types for each column in the document
   * @default null
   */
  google_sheet_id: string
  /**
   * The file being uploaded by the user
   */
  file: Nullable<File>
  /**
   * A key used to get the the actual data under
   * a certain key when importing from a JSON document
   * @default null
   * @example {"data": [ {..}, {...} ] } -> entry_key = "data"
   */
  entry_key: Nullable<string>
  /**
   * Array of columns to keep when importing the document
   * If empty, all columns will be imported
   */
  using_columns: ColumnTypeOptions[]
}
