import { databasesFixture } from '~/data/__fixtures__'

export const useDatabasesStore = defineStore('databases', () => {
  const databases = reactive(databasesFixture)

  const search = ref<string>('')
  const searched = computed(() => {
    return databases.filter(database => database.name.toLowerCase().includes(search.value.toLowerCase()))
  })

  const routeId = ref<number | null>(null)
  const currentDatabase = computed(() => databases.find(database => database.id === routeId.value))

  return {
    routeId,
    search,
    searched,
    currentDatabase
  }
})
