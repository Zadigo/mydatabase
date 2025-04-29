export interface Block {
    name: string
    block_id: string
    component: string
    record_creation_columns: string[]
    record_update_columns: string[]
    visible_columns: string[]
    block_data_source: null
    search_columns: string[]
    user_filters: string[]
    conditions: string[]
    allow_record_creation: boolean
    allow_record_update: boolean
    allow_record_search: boolean
    active: boolean
    modified_on: string
    created_on: string
}

export interface Slide {
    name: string
    slide_id: string
    blocks: Block[]
    slide_data_source: null
    acces: null
    columns_visibility: null
    share_url: string
    modified_on: string
    created_on: string
}
