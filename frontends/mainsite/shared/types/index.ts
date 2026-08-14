import { z } from 'zod'

export const NewDatabaseSchema = z.object({
  name: z.string().min(3),
  description: z.string().nullish()
})

export type NewDatabase = z.infer<typeof NewDatabaseSchema>

export const NewTableSchema = z.object({
  name: z.string().min(5),
  database: z.string().or(z.number()).nullish()
})

export type NewTable = z.infer<typeof NewTableSchema>
