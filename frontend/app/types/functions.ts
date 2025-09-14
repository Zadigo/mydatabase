import type { ReturnAny, Nullable } from '.'

export const baseDatabaseFunctions = [
  'Count',
  'Sum',
  'Avg',
  'Min',
  'Max',
  'Upper',
  'Lower',
  'Length',
  'Trim',
  'Group concat',
  'Coalesce',
  'Extract',
  'Now',
  'Date',
  'Time',
  'Datetime',
  'Strftime',
  'Current timestamp',
  'Current date',
  'Current time',
  'Random',
  'MD5',
  'SHA256',
  'SHA512'
] as const

export type DatabaseFunctions = typeof baseDatabaseFunctions[number]

export const functionReturnTypes = [
  'void',
  'integer',
  'float',
  'bool',
  'time',
  'text',
  'time',
  'timetz',
  'timestamp',
  'timestamptz',
  'uuid'
] as const

export type FunctionReturnTypes = typeof functionReturnTypes[number]

export const functionFailures = [
  'Record',
  'Default',
  'Skip'
] as const

export type FunctionFailures = typeof functionFailures[number]

export interface DatabaseFunction {
  name: DatabaseFunctions
  table: Nullable<number>
  columns: string[]
  returns: {
    value: ReturnAny
    /**
     * @default "void"
     */
    type: FunctionReturnTypes
  }
  chain_to: string[]
  on_fail: {
    do: FunctionFailures
    default_value: ReturnAny
  }
}
