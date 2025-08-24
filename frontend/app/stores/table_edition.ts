export const useTableEditionStore = defineStore('tableEdition', () => {
  const selectedTable = ref<string>('')

  return {
    selectedTable
  }
})
