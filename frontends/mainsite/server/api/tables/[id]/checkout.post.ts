import type { FileCheckoutResponse } from '#shared/types'

export default defineEventHandler(async (event) => {
  try {
    const multipartData = await readMultipartFormData(event)

    if (!multipartData) {
      throw new Error('No form data received.')
    }

    const formData = new FormData()

    for (const part of multipartData) {
      if (!part.name) continue

      if (part.filename) {
        const blob = new Blob([part.data], { type: part.type })
        formData.append(part.name, blob, part.filename)
      } else {
        formData.append(part.name, part.data.toString('utf-8'))
      }
    }

    const params = getRouterParams(event) as { id: string }

    if (!params.id || params.id.trim() === '') {
      throw new Error('No table ID provided.')
    }

    return await $fetch<FileCheckoutResponse>(`/v1/tables/${params.id}/checkout`, {
      method: 'POST',
      baseURL: useRuntimeConfig().public.prodDomain,
      body: formData,
    })
  } catch (error) {
    console.log(error)
    throw createError({
      status: 500,
      statusMessage: 'An unknown error occurred',
      data: undefined,
      cause: error,
      message: (error as Error).message
    })
  }


  // try {
  //   const multipartData = await readMultipartFormData(event)

  //   if (!multipartData) {
  //     console.log('No form data received.')
  //     const template = createErrorTemplate(new Error('No form data received.'))
  //     throw createError(template)
  //   }

  //   const params = getRouterParams(event) as { id: string }
  //   const formData = new FormData()

  //   for (const part of multipartData) {
  //     if (!part.name) continue

  //     if (part.filename) {
  //       const blob = new Blob([part.data], { type: part.type })
  //       formData.append(part.name, blob, part.filename)
  //     } else {
  //       formData.append(part.name, part.data.toString('utf-8'))
  //     }
  //   }

  //   if (!params.id) {
  //     const template = createErrorTemplate(new Error('No table ID provided.'))
  //     throw createError(template)
  //   }

  //   return await $fetch<FileCheckoutResponse>(`/v1/tables/${params.id}/checkout`, {
  //     method: 'POST',
  //     baseURL: useRuntimeConfig().public.prodDomain,
  //     body: formData,
  //   })
  // } catch (error) {
  //   console.error('Error during checkout:', error)
  //   const template = createErrorTemplate(error)
  //   throw createError(template)
  // }
})
