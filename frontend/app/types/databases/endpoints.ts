import type { _BaseDatabaseObject } from '..'
import type { Table } from '../tables'

/**
 * @private
 */
// interface _DatabaseTable {
// 	id: string
// 	name: string
// }

/**
 * @private
 */
interface _DatabaseSchema extends _BaseDatabaseObject {
	name: string
	tables: Table[]
}

export interface DatabaseEndpoint extends _BaseDatabaseObject {
	methods: ('GET' | 'POST' | 'PUT' | 'DELETE')[]
	endpoint: string
	endpoint_uuid: string
  database_schema: _DatabaseSchema
}
