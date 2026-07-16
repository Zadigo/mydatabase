import { createErrorTemplate } from '~/utils'

export default defineEventHandler(async (event) => {
  const tableDocument = await readBody<{ document_uuid: string }>(event)

  try {
    return await $fetch(`/v1/documents/${tableDocument.document_uuid}`, {
      baseURL: useRuntimeConfig().public.prodDomain,
      method: 'DELETE'
    })
  } catch (error) {
    const template = createErrorTemplate(error)
    throw createError(template)
  }
})
