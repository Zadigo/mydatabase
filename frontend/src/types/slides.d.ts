import type { BlockItem } from './block'
import type { DataSource } from './data_source'
import type { User } from "./user"

export interface Slide {
  id: number
  user: User
  slide_id: string
  name: string
  blocks: BlockItem[]
  slide_data_source: DataSource
  access: 'Public' | 'Private'
  modified_on: string
  created_on: string
}

export interface SlideData {
  [string]: string
}
