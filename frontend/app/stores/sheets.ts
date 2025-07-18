export const useSheetsStore = defineStore('sheets', () => {
  const { activeSlide } = storeToRefs(useSlideStore())
  const searchSheet = ref<string>('')

  const activeSlideSheets = computed(() => activeSlide.value ? activeSlide.value.sheets : [])
  const hasSheets = computed(() => activeSlideSheets.value.length > 0)

  const searched = computed(() => {
    if (!searchSheet.value || searchSheet.value.trim() === '') {
      return activeSlideSheets.value
    } else {
      return activeSlideSheets.value.filter(sheet => sheet.name.toLowerCase().includes(searchSheet.value.toLowerCase()))
    }
  })

  return {
    /**
     * Returns the sheets or data sources that are
     * currently linked to the current slide
     */
    activeSlideSheets,
    /**
     * Whether the current slide has any sheets or data 
     * sources linked to it
     */
    hasSheets,
    /**
     * Search term for filtering sheets
     */
    searched,
  }
})
