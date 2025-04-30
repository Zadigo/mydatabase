export interface BlockItem {
  id: number
}

export interface BlockItemData {
  [string]: string | number
}

export interface BlockRequestData {
  name: null
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
