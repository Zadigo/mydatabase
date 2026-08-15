import { createErrorTemplate } from '~/utils/errors'
import type { FileCheckoutResponse } from '~/types'

export default defineEventHandler(async (event) => {
  try {
    const params = getRouterParams(event) as { id: string }
    const formData = await readBody<FormData>(event)

    return await $fetch<FileCheckoutResponse>(`/v1/tables/${params.id}/checkout`, {
      method: 'POST',
      baseURL: useRuntimeConfig().public.prodDomain,
      body: formData
    })
  } catch (error) {
    const template = createErrorTemplate(error)
    throw createError(template)
  }
})
