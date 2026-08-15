import type { ColumnTypeOptions, Nullable } from '~/types'

export * from './edition'
export * from './reader'
export * from './relationships'
export * from './utils'
export * from './creation'

export type DocumentTypes = 'csv' | 'json' | 'google_sheet'

export interface DocumentParams {
  name: string
  url: Nullable<string>
  file: File | undefined
  entry_key: Nullable<string>
  source_type: 'file' | 'url'
  content_type: DocumentTypes
  primary_key_file: boolean
}

export interface NewDocument {
  name: string
  using_columns: ColumnTypeOptions[]
  documents: DocumentParams[]
  merge: boolean
}
