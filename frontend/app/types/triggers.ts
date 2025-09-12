export const databaseTriggerEvent = ['insert', 'update', 'delete'] as const

export type DatabaseTriggerEvent = (typeof databaseTriggerEvent)[number]

interface TriggerMetadata {
	database: string
}

interface TriggerBody {
	name: string
	metadata: TriggerMetadata
	when: 'before' | 'after'
  event: DatabaseTriggerEvent
	functions: string[]
}

export interface DatabaseTrigger {
	trigger: TriggerBody
}
