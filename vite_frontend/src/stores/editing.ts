import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { api } from '../plugins'

import type { BlockItem, DataSource, DataSourceDataApiResponse, Slide } from '../types'
import type { BlockRequestData } from '../utils'
import { defaultOperators, type DefaultOperators } from '../data'

export const useEditing = defineStore('editing', () => {
  const currentBlockToEdit = ref<BlockItem>()

  /**
   * Data souce for the slide if present and available
   * for other components that need it
   */
  const slideDataSourceToEdit = ref<DataSource>()

  /**
   * This ref is used for the user clicks on blocks which can
   * contain different datasources. The datasouce of the current
   * block is establised here
   */
  const blockActiveDatasourceToEdit = ref<DataSource>()

  /**
   * Gets populated when the user clicks on a block. Thie data
   * is to be modified and manipulated to be sent to Django
   */
  const blockRequestData = ref<BlockRequestData>({
    name: '',
    record_creation_columns: [],
    record_update_columns: [],
    allow_record_creation: true,
    allow_record_search: true,
    allow_record_update: true,
    block_data_source: null,
    search_columns: [],
    user_filters: [],
    visible_columns: [],
    conditions: {
      filters: [],
      groups: []
    },
    active: true
  })

  /**
   * Indicates if the slide has data 
   */
  const slideHasData = computed(() => {
    return typeof slideDataSourceToEdit.value === 'undefined'
  })

  /**
   * Checks if a block was selected in a slide
   */
  const blockSelected = computed(() => {
    // Checks if a block was selected in a slide
    if (currentBlockToEdit.value) {
      return true
    } else {
      return false
    }
  })

  /**
   * Reset the modifications made
   * to the blockRequestData
   */
  function resetBlockRequestData() {
    blockRequestData.value = {
      name: '',
      record_creation_columns: [],
      record_update_columns: [],
      allow_record_creation: true,
      allow_record_search: true,
      allow_record_update: true,
      block_data_source: null,
      search_columns: [],
      user_filters: [],
      visible_columns: [],
      conditions: {
        filters: [],
        groups: []
      },
      active: true
    }
  }

  /**
   * Sets the active datasource to edit for the
   * current sheet ID of the current active block
   */
  async function setActiveDatasource(block?: BlockItem | null, slide?: Slide | null) {
    if (block) {
      blockActiveDatasourceToEdit.value = block.block_data_source
    } else if (slide) {
      slideDataSourceToEdit.value = slide.slide_data_source
    }
  }

  /**
   * Set the current values for the
   * in the requestData for the current
   * selected block
   */
  function setCurrentBlockRequestData() {
    if (currentBlockToEdit.value) {
      Object.keys(blockRequestData.value).forEach((key) => {
        blockRequestData.value[key] = currentBlockToEdit.value[key]
      })
    }
  }

  /**
   * Returns the underlying data for a specific given
   * datasource ID
   *
   * @param id The ID of the datasource
   * @param callback Callback function with the actual data
   */
  async function getDatasourceData(datasourceId: string, callback: (data: DataSourceDataApiResponse) => void) {
    try {
      if (datasourceId) {
        const response = await api.get<DataSourceDataApiResponse>(`/api/v1/datasources/${datasourceId}`)
        callback(response.data)
      }
    } catch (e) {
      console.log(e)
    }
  }

  /**
   * Helper function used to create filters
   */
  function createFilter<T extends string | number>(column: string, operator: DefaultOperators, value: T): { column: string, operator: DefaultOperators, value: T } {
    if (!defaultOperators.includes(operator)) {
      return {
        column,
        operator: 'contains',
        value
      }
    } else {
      return {
        column,
        operator,
        value
      }
    }
  }

  return {
    blockActiveDatasourceToEdit,
    slideDataSourceToEdit,
    blockRequestData,
    blockSelected,
    currentBlockToEdit,
    slideHasData,

    createFilter,
    getDatasourceData,
    setCurrentBlockRequestData,
    resetBlockRequestData,
    setActiveDatasource
  }
})
