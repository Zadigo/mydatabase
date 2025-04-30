export type ComponentTypes = 'Table block' | 'Graph block' | 'Grid block' | 'Chart block'

export interface BlockItem {
  id: number
  name: string
  block_id: string
  component: ComponentTypes
  record_creation_columns: string[]
  record_update_columns: string[]
  visible_columns: string[]
  block_data_source: string | null
  active_data_source: string | null
  conditions: string[]
  allow_record_creation: boolean
  allow_record_update: boolean
  allow_record_search: boolean
  user_filters: string[]
  search_columns: string[]
  active: boolean
  modified_on: string
  created_on: string
}

export interface BlockItemData {
  [string]: string | number
}

export interface BlockRequestData {
  name: string | null
  record_creation_columns: string[]
  record_update_columns: string[]
  allow_record_creation: boolean
  allow_record_search: boolean
  allow_record_update: boolean
  block_data_source: string | null
  search_columns: string[]
  user_filters: string[]
  visible_columns: string[]
  conditions: {
    filters: string[]
    groups: string
  }
  active: boolean
}
