import { z } from 'zod'

export const WaitlistDataSchema  = z.object({
  email: z.string(),
  telephone: z.string().optional(),
  company: z.string(),
  firstname: z.string(),
  lastname: z.string()
})

export type WaitlistData = z.infer<typeof WaitlistDataSchema>
