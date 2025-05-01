export * from './operators'

export const defaultComponentTypes = [
  'table-block',
  'graph-block',
  'grid-block',
  'chart-block',
  'calendar-block',
  'grid-2-block'
] as const

export type DeafaultComponentTypes = (typeof defaultComponentTypes)[number]

export const defaultColumnTypes = [
  'Text',
  'Data',
  'Link',
  'Number'
] as const

export type DefaultColumnTypes = (typeof defaultColumnTypes)[number]
