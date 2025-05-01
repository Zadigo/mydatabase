import type { RouteParamsGeneric } from 'vue-router'
import type { Component } from 'vue'
import type { DeafaultComponentTypes } from '../data'

export * from './slides'
export * from './sheet'
export * from './block'
export * from './data_source'
export * from './user'

export interface ExtendedRouteParamsGeneric extends RouteParamsGeneric {
  id: string
}

export type BlockType = {
  name: string
  component: Component | (() => Promise<{ default: Component }>)
  // sidebar: Component | (() => Promise<{ default: Component }>)
  shortname: DeafaultComponentTypes
  icon: string
}
