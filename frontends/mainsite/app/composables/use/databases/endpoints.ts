import type { DatabaseEndpoint } from '#shared/types/api/databases/endpoints'

/**
 * Composable used to fetch the endpoints for a database
 * @param database The database to fetch endpoints for
 */
export const useDatabaseEndpoints = createSharedComposable(() => {
  const { currentDatabase } = _useDatabases() 

  const endpoints = computedAsync(async () => {
    return await $fetch<DatabaseEndpoint[]>(`/api/databases/${currentDatabase.value?.id}/endpoints`, {
      method: 'GET',
    })
  })

  /**
   * New endpoint
   */

  const [ showModal, toggleShowModal ] = useToggle()
  const newEndpointName = ref<string>('')

  async function create() {
    if (isDefined(currentDatabase)) {
      const data = await $fetch<DatabaseEndpoint[]>(`/api/databases/${currentDatabase.value?.id}/endpoints/create`, {
        method: 'POST',
        baseURL: useRuntimeConfig().public.prodDomain,
        body: { endpoint: newEndpointName.value }
      })

      endpoints.value = data
      toggleShowModal()
    }
  }

  return {
    showModal,
    newEndpointName,
    endpoints,
    toggleShowModal,
    create
  }
})
