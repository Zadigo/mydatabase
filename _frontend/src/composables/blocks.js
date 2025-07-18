import { ref } from 'vue'

export function useBlocksComposable (instance) {
  const selected = ref(false)
  const columnSortingChoices = ref(['No sort', 'Ascending', 'Descending'])
  const columnTypeChoices = ref(['Text', 'Date', 'Link', 'Number'])

  function handleBlockSelection (details) {
    // Highlights the block when the user
    // has clicked on the card
    selected.value = !selected.value
    instance.emit('block-selected', details)
  }

  return {
    selected,
    columnTypeChoices,
    columnSortingChoices,
    handleBlockSelection
  }
}
