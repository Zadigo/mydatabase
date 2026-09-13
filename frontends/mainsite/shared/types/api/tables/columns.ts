import { columnType } from '~/constants/columns'

export type DefaultColumnOption = 'visible' | 'editable' | 'sortable' | 'searchable' | 'unique' | 'nullable'

export type ColumnType = typeof columnType[number]

export interface ColumnTypes {
  name: string
  columnType: ColumnType
}

export type ColumnOptions = {
  /**
   * The column's name
   */
  name: string
  /**
   * The new name for this column
   */
  newName: string
  /**
   * The data type for this column
   * @default "String"
   */
  columnType: ColumnType
} & { [K in DefaultColumnOption]: boolean }

export interface FileCheckoutResponse {
  sample: Record<string, unknown>[]
  numberOfRows: number
  numberOfColumns: number
  columns: string[]
  columnTypes: ColumnOptions[]
}
