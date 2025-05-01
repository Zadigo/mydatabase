import { z } from 'zod'

export const newSlideSchema = z.object({
  name: z.string().nonempty(),
  private: z.boolean().default(false)
})

export type NewSlide = z.infer<typeof newSlideSchema>
