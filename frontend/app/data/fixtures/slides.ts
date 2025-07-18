import type { Block, Slide } from '~/types'

export const blockFixture: Block = {
  id: 1,
  name: 'Simple block',
  block_id: 'bl_TFuSU',
  component: 'table-block',
  record_creation_columns: null,
  record_update_columns: null,
  visible_columns: null,
  block_data_source: null,
  data_source: null,
  conditions: null,
  allow_record_creation: true,
  allow_record_update: true,
  allow_record_search: true,
  user_filters: null,
  search_columns: null,
  active: true,
  modified_on: '2025-07-18T12:19:48.593508Z',
  created_on: '2025-07-18T12:19:42.450695Z'
} as const

export const blocksFixture = [blockFixture]

export const slideFixture: Slide = {
  id: 1,
  user: {
    id: 1
  },
  slide_id: 'sl_QWVSd',
  name: 'Billboard winners',
  sheets: [
    {
      id: 1,
      user: {
        id: 1
      },
      name: 'Billboard winners',
      sheet_id: 'sh_OhmQy',
      url: null,
      csv_based: true,
      csv_file: '/media/sheets/sh_OhmQy/JIpXVkWM9RqcTXyD4Vl3.csv',
      columns: null,
      column_types: null,
      created_on: '2025-07-18T10:30:29.279737Z'
    }
  ],
  // blocks: [],
  blocks: blocksFixture,
  slide_data_source: null,
  access: 'Public',
  modified_on: '2025-07-18T10:32:50.473257Z',
  created_on: '2025-07-18T10:32:41.795427Z'
} as const

export const slidesFixture: Slide[] = [slideFixture]
