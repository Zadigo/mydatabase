export type * from './databases'
export type * from './functions'
export type * from './relationships'
export type * from './triggers'
export type * from './tables'


/**
 * @private
 */
export interface _BaseDatetimes {
  updated_at: string
  created_at: string
}

/**
 * @private
 */
export interface _BaseDatabaseObject extends _BaseDatetimes {
  id: number
}
