import { defineStore } from "pinia";

const useSheets = defineStore('sheets', {
  data: () => ({
    sheets: [],
    currentSheet: {}
  })
})

export {
  useSheets
}
