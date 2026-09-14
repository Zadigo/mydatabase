import { createErrorTemplate } from '~/utils/errors'

export default defineEventHandler(async (event) => {
  try {
    const tableId = getRouterParam(event, 'id')

    if(!tableId) {
      throw new Error('No table ID provided')
    }

    const formData = await readMultipartFormData(event)
    
    if (!formData || formData.length === 0) {
      throw new Error('No form data provided')
    }

    return await $fetch<{ name: string }>(`/v1/tables/${tableId}/upload`, {
      method: 'POST',
      baseURL: useRuntimeConfig().public.prodDomain,
      body: formData
    })
  } catch (error) {
    const template = createErrorTemplate(error)
    throw createError(template)
  }
})
