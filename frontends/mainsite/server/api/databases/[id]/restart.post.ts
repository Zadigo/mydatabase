export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig(event)
  const id = getRouterParam(event, 'id')
  return await $fetch(`/v1/databases/${id}/restart`, {
    method: 'POST',
    baseURL: config.public.prodDomain
  })
})
