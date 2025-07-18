import { defineStore } from "pinia";

const usePublishedPages = defineStore('published_pages', {
  state: () => ({
    pages: [],
    currentPage: {},
    isPreview: false
  })
})

export {
  usePublishedPages
}
