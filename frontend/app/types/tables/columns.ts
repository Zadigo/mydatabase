export type DefaultColumnOption = 'visible' | 'editable' | 'sortable' | 'searchable'

export type ColumnOptions = { name: string, columnType: ColumnType } & { [K in DefaultColumnOption]: boolean }

export const columnType = [
  'String',
  'Number',
  'Boolean',
  'Date',
  'DateTime',
  'Array',
  'Dict'
] as const

export type ColumnType = typeof columnType[number]

export interface ColumnTypeOptions {
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
  columnType: ColumnType,
  /**
   * Column values should be unique
   * @default false
   */
  unique: boolean
  /**
   * Column an be null
   * @default true
   */
  nullable: boolean
  /**
   * Whether the column is visible in the table or not
   * @default true
   * @deprecated This field is deprecated and should not be used. Use the `UserPreferredColumnTypeOptions` interface instead, which includes the `visible` property for user preferences.
   */
  visible: boolean
}

export interface UserPreferredColumnTypeOptions extends ColumnTypeOptions {
  /**
  * Whether the column is visible in the table or not
  * @default true
  */
  visible: boolean
}

export interface FileCheckoutResponse {
  sample: Record<string, unknown>[]
  numberOfRows: number
  numberOfColumns: number
  columns: string[]
  columnTypes: UserPreferredColumnTypeOptions[]
}
