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

// export const ColumnTypeSchema = z.object({
//   name: z.string(),
//   newName: z.string(),
//   columnType: z.enum('')
// })

// export const NewDocumentSchema = z.object({
//   name: z.string().nullish(),
//   using_columns: ,
//   documents: z.array(
//     z.object({
//       name: z.string().min(2),
//       url: z.string().nullish(),
//       file: z.file().nullish(),
//       entry_key: z.string().nullish()
//     })
//   )
// })

// export type NewDocument = z.infer<typeof NewDocumentSchema>
