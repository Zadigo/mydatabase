export const defaultOperators = [
  'contains',
  'does not contain...',
  'is',
  'is not',
  'is empty',
  'is not empty',

  'equals',
  'is not equal',
  'greather than',
  'greather than or equal to',
  'less than',
  'less than or equal to'
] as const

export const defaultColumnInputs = [
  'Input',
  'Single select',
  'Multi select',
  'Date'
] as const 

export const defaultUnions = [
  'and',
  'or'
] as const 

export const defaultSortingChoices = [
  'No sort',
  'Ascending',
  'Descending'
] as const

export const defaultInputTypes = [
  'Input'
] as const

export type DefaultOperators = (typeof defaultOperators)[number]

export type DefaultColumnInputs = (typeof defaultColumnInputs)[number]

export type DefaultUnions = (typeof defaultUnions)[number]

export type DefaultSortingChoices = (typeof defaultSortingChoices)[number]

export type DefaultInputTypes = (typeof defaultInputTypes)[number]
