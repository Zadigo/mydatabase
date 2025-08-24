export interface Document {
  id: number
  data: Record<string, unknown>
}

export interface Table {
  id: number
  name: string
  documents: Document[]
}

type SimpleTable = Pick<Table, 'id' | 'name' | 'documents'>

export interface Database {
  id: number
  name: string
  tables: SimpleTable[]
}
