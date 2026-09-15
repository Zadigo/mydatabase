import type { ColumnOptions } from './api/tables/columns'

export type DocumentTypes = 'csv' | 'json' | 'google_sheet'

export interface DocumentParams {
  name: string
  url: string
  file: File | undefined
  entry_key: Nullable<string>
  source_type: 'file' | 'url'
  content_type: DocumentTypes
  primary_key_file: boolean
  column_options: ColumnOptions[]
}

export interface NewDocument {
  global_name: string
  documents: DocumentParams[]
  merge: boolean
}
