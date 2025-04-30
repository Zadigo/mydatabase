import { defineStore } from "pinia"
import { ref } from "vue"

export const useSheets = defineStore('sheets', () => {
  const sheets = ref([])
  const currentSheet = ref({})

  return {
    sheets,
    currentSheet
  }
})
