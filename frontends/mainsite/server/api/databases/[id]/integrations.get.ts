export default defineEventHandler((event) => {
  const id = getRouterParam(event, 'id')
  return $fetch(`/v1/databases/${id}/integrations`, {
    method: 'GET',
    baseURL: useRuntimeConfig().public.prodDomain
  })
})
