export interface Table {
  id: number
  name: string
}

type SimpleTable = Pick<Table, 'id' | 'name'>

export interface Database {
  id: number
  name: string
  tables: SimpleTable[]
}
