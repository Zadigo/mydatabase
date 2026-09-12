export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig(event)
  const id = getRouterParam(event, 'id')

  return await $fetch(`/v1/databases/${id}/delete`, {
    method: 'DELETE',
    baseURL: config.public.prodDomain
  })
})
