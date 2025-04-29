import _ from 'lodash'
import { computed, ref } from 'vue'
import { useSlides } from '../stores/slides'

export function useDataUpdating (app, columns) {
  const slidesStore = useSlides()
  const isSaved = ref(false)

  const requiresSaving = computed(() => {
    // Compares the request data against the
    // initial data to determine whether the
    // user brought changes to the initial data
    // that would require him to press a save button
    const truthArray = []
    _.forEach(columns, (column) => {
      const initialValue = slidesStore.currentSlide[column]
      const currentValue = app.ctx.requestData[column]
      truthArray.push(initialValue === currentValue)
    })
    return _.some(truthArray, x => x === false)
  })

  const canBeSaved = computed(() => {
    // Computed method that checks if an item
    // still requires saving. In other words,
    // checks if the user pressed the saved
    // button and that item still requires saving
    return !this.isSaved && this.requiresSaving
  })

  return {
    isSaved,
    canBeSaved,
    requiresSaving
  }
}
