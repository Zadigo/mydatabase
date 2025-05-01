import { defaultColumnInputs, type DefaultOperators, defaultOperators, defaultUnions } from '../data'

/**
 * A composable for using filters
 */
export function useColumnFilters() {
  /**
   *
   */
  function createFilter<T extends string | number>(column: string, operator: DefaultOperators, value: T): { column: string, operator: DefaultOperators, value: T } {
    if (!defaultOperators.includes(operator)) {
      return {
        column,
        operator: 'contains',
        value
      }
    } else {
      return {
        column,
        operator,
        value
      }
    }
  }

  return {
    defaultOperators,
    defaultColumnInputs,
    defaultUnions,
    createFilter
  }
}
