import { databasesFixture } from '~/data/__fixtures__'

export const useDatabasesStore = defineStore('databases', () => {
  const databases = reactive(databasesFixture)

  const search = ref<string>('')
  const searched = computed(() => {
    return databases.filter(database => database.name.toLowerCase().includes(search.value.toLowerCase()))
  })

  return {
    search,
    searched
  }
})
