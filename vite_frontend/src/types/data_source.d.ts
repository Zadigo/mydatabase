import type { User } from "./user"

/**
 * Information on the data source 
 */
export interface DataSource {
  id: number
  user: User
  name: string
  data_source_id: string
  google_sheet_url: string | null
  csv_based: boolean
  csv_file: string | null
  columns: string[]
  column_names: string[]
  created_on: string
}

/**
 * The actual data from the source e.g. rows 
 */
export type RowData = {
  [key: string]: string | number | boolean | null
}

/**
 * The result that is received when the data from the
 * source is read and returned by the endpoint 
 */
export interface DataSourceDataApiResponse {
  columns: string[]
  count: number
  results: RowData[]
}


