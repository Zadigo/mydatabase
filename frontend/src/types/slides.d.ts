import type { BlockItem } from './block'

export interface Slide {
  id: number
  user: {
    id: number
  }
  slide_id: string
  name: string
  blocks: BlockItem[]
  slide_data_source: string | null
  access: 'Public' | 'Private'
  modified_on: string
  created_on: string
}

export interface SlideData {
  [string]: string
}
