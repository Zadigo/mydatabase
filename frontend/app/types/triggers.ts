export type DatabaseTriggerEvent = (typeof databaseTriggerEvent)[number]

interface Condition {
	database: number
}

interface TriggerBody {
	event: DatabaseTriggerEvent
	when: {
		before: boolean
		after: boolean
	}
	name: string
	orientation: 'row' | 'column'
	function: string
}

export interface DatabaseTrigger {
	on: Condition
	trigger: TriggerBody[]
}
