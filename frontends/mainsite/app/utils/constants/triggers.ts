export const databaseTriggerEvent = [ 'insert', 'update', 'delete' ] as const

export const databaseTriggerWhen = [ 'before', 'after' ] as const

export const databaseTriggerOrientation = [ 'row', 'column' ] as const
