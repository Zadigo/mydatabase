import { createErrorTemplate } from '~/utils/errors'

export default defineEventHandler(async (event) => {
  try {
    const id = getRouterParam(event, 'id')
    const formData = await readBody(event)

    return await $fetch<{ name: string }>(`/v1/tables/${id}/upload`, {
      method: 'POST',
      baseURL: useRuntimeConfig().public.prodDomain,
      body: formData
    })
  } catch (error) {
    const template = createErrorTemplate(error)
    throw createError(template)
  }
})
