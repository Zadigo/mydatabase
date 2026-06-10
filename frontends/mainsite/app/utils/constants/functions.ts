import type { SelectItem } from '@nuxt/ui'

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

export const functionFailures = [
  'Record',
  'Default',
  'Skip'
] as const

export const selectFunctionMenuItems = ref<SelectItem[]>([
  {
    type: 'label',
    label: 'Aggregate'
  },
  'Count',
  'Sum',
  'Avg',
  'Min',
  'Max',
  {
    type: 'separator'
  },
  {
    type: 'label',
    label: 'String'
  },
  'Upper',
  'Lower',
  'Length',
  'Trim',
  'Group concat',
  'Coalesce',
  'Extract',
  {
    type: 'separator'
  },
  {
    type: 'label',
    label: 'Date'
  },
  'Now',
  'Date',
  'Time',
  'Datetime',
  'Strftime',
  'Current timestamp',
  'Current date',
  'Current time',
  {
    type: 'separator'
  },
  {
    type: 'label',
    label: 'Miscellanous'
  },
  'Random',
  'MD5',
  'SHA256',
  'SHA512'
])
