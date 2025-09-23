export type DefaultColumnOption = 'visible' | 'editable' | 'sortable' | 'searchable'

export type ColumnOptions = { name: string } & { [K in DefaultColumnOption]: boolean }

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
  new_name: string
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
   */
  visible: boolean
}
