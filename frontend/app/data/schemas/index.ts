import zod from 'zod'

export const newSlideSchema = zod.object({
  name: zod.string().nonempty(),
  private: zod.boolean().default(false)
})

export type NewSlide = zod.infer<typeof newSlideSchema>
