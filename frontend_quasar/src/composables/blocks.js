import { computed, ref } from 'vue'
import { useSlides } from 'src/stores/slides'
import { api } from '../boot/axios'
import { session } from '../boot/vue-storages'

export function useBlocksComposable (app) {
  const slidesStore = useSlides()
  const cachedDataSource = ref({})
  const dataResults = ref([])

  const useBlockDataSource = computed(() => {
    // Checks whether we have a data at the block level
    // or at the slide level. If we have data at the 
    // block level, then we will be using it, otherwise
    // we will be using the global slide data
    return app.ctx.block.block_data_source !== null
  })

  const hasSlideDataSource = computed(() => {
    // Checks whether we have a data source to work
    // with from the slide level
    return slidesStore.currentSlide.slide_data_source !== null
  })

  const dataSourceId = computed(() => {
    // Returns the correct data source ID to use to
    // retrieve the data from the database
    return slidesStore.currentSlide.slide_data_source || app.ctx.block.slide_data_source
  })

  function setDataSource (data) {
    // Sets the data using the initial response
    // from the backend
    cachedDataSource.value = data
    dataResults.value = data.results
  }

  async function requestDataSource (callback) {
    // Returns the actual data for the given
    // data source ID (slide or block level)
    try {
      // if (dataSourceId.value !== null) {
      //   const response = await api.get(`/datasources/${dataSourceId.value}`)
      //   setDataSource(response.data)
      //   session.dictSet('sources', dataSourceId.value, response.data)
      // }
      const slideId = slidesStore.currentSlide.slide_id
      const blockId = app.ctx.block.block_id

      // if (session.dictExists('sources', blockId)) {
      //   const data = session.dictGet('sources', blockId)
      //   dataResults.value = data
      // } else {
      // }
      const response = await api.get(`/slides/${slideId}/blocks/${blockId}`)
      const response2 = await api.get(`/datasources/${response.data.active_data_source.data_source_id}`)
      cachedDataSource.value = response2.data
      dataResults.value = response2.data.results
      session.dictSet('sources', blockId, response2.data)
      if (callback) {
        callback()
      }
    } catch (error) {
      console.log(error)
    }
  }

  return {
    dataResults,
    dataSourceId,
    cachedDataSource,
    setDataSource,
    requestDataSource,
    hasSlideDataSource,
    useBlockDataSource
  }
}
