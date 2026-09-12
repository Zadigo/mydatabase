export default defineEventHandler(async (event) => {
  const id = getRouterParam(event, 'id')
  const body = await readBody(event)
  return await $fetch<SimpleTable>(`/v1/tables/${id}`, {
    method: 'PATCH',
    baseURL: useRuntimeConfig().public.prodDomain,
    body: body
  })
})
