export const defaultComponentTypes = [
  'table-block', 
  'graph-block', 
  'grid-block', 
  'chart-block'
] as const

export type ComponentTypes = (typeof defaultComponentTypes)[number]


export const defaultColumnTypes = [
  'Text',
  'Data',
  'Link',
  'Number'
] as const

export type ColumnTypes = (typeof defaultColumnTypes)[number]
