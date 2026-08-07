export type DatabaseTriggerEvent = (typeof DATABASE_TRIGGER_EVENT)[number]

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
