export const integrationTool = [
  'Zapier',
  'Make',
  'Google Sheets',
  'Airtable',
  'Supabase',
  'Excel',
  'N8N',
  'Notion'
] as const

export type IntegrationTool = typeof integrationTool[number]

export interface ConnectionOptions {
  name: IntegrationTool
  short_description: string
  logo: string
  coming_soon: boolean
  beta: boolean
}
