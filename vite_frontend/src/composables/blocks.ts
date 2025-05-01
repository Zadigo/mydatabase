import { type DefaultColumnTypes, defaultColumnTypes, type DefaultSortingChoices, defaultSortingChoices } from 'src/data'
import { computed, ref } from 'vue'

export function useBlocksComposable () {
  const selected = ref<boolean>(false)

  const columnSortingChoices = computed((): DefaultSortingChoices[] => {
    return [...defaultSortingChoices]
  })

  const columnTypeChoices = computed((): DefaultColumnTypes[] => {
    return [...defaultColumnTypes]
  })

  /**
   * Highlights the block when the user 
   * has clicked on the card
   */
  function handleBlockSelection(details) {
    selected.value = !selected.value
    // if (instance) {
    //   instance.emit('block-selected', details)
    // }
  }

  return {
    selected,
    columnTypeChoices,
    columnSortingChoices,
    handleBlockSelection
  }
}
