import type { RouteParamsGeneric } from 'vue-router'

export * from './slides'
export * from './sheet'
export * from './block'
export * from './data_source'
export * from './user'

export interface ExtendedRouteParamsGeneric extends RouteParamsGeneric {
  id: string
}
