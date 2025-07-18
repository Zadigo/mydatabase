export interface Block {
  id: number
  name: string | null
  block_id: string
  component: string
  record_creation_columns: string[] | null
  record_update_columns: string[] | null
  visible_columns: string[] | null
  block_data_source: string | null
  data_source: string | null
  conditions: {
    filters: Record<string, unknown>[]
  } | null
  allow_record_creation: boolean
  allow_record_update: boolean
  allow_record_search: boolean
  user_filters: Record<string, unknown> | null
  search_columns: string[] | null
  active: boolean
  modified_on: string
  created_on: string
} 

export interface Sheet {
  id: number
  user: {
    id: number
  }
  sheet_id: string
  name: string
  url: string | null
  csv_based: boolean
  csv_file: string | null
  columns: string[] | null
  column_types: Record<string, string> | null
  created_on: string
}

export interface Slide {
  id: number
  user: {
    id: number
  }
  slide_id: string
  name: string
  sheets: Sheet[]
  blocks: Block[]
  slide_data_source: string | null
  access: 'Public' | 'Private'
  modified_on: string
  created_on: string
}
