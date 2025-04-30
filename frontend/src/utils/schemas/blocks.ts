import { z } from 'zod'

export const BlockRequestDataSchema = z.object({
  name: z.string().nonempty(),
  record_creation_columns: z.enum(['a']),
  record_update_columns: z.enum(['a']),
  allow_record_creation: z.boolean().default(false),
  allow_record_search: z.boolean().default(false),
  allow_record_update: z.boolean().default(false),
  block_data_source: z.string().nullable(),
  search_columns: z.enum(['a']),
  user_filters: z.enum(['a']),
  visible_columns: z.enum(['a']),
  conditions: z.object({
    filters: z.enum(['a']),
    groups: z.string()
  }),
  active: z.boolean().default(false),
})

export type BlockRequestData = z.infer<typeof BlockRequestDataSchema>
