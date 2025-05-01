import { z } from 'zod'

export const BlockRequestDataSchema = z.object({
  name: z.string().nonempty(),
  record_creation_columns: z.object({
    name: z.string(),
    state: z.boolean()
  }).array(),
  record_update_columns: z.object({
    name: z.string(),
    state: z.boolean()
  }).array(),
  allow_record_creation: z.boolean().default(false),
  allow_record_search: z.boolean().default(false),
  allow_record_update: z.boolean().default(false),
  block_data_source: z.string().nullable(),
  search_columns: z.object({
    name: z.string(),
    state: z.boolean()
  }).array(),
  user_filters: z.object({
    name: z.string(),
    state: z.boolean()
  }).array(),
  visible_columns: z.object({
    name: z.string(),
    state: z.boolean()
  }).array(),
  conditions: z.object({
    filters: z.string().array(),
    groups: z.string().array()
  }),
  active: z.boolean().default(false),
})

export type BlockRequestData = z.infer<typeof BlockRequestDataSchema>
