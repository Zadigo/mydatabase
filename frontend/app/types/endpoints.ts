/**
 * @private
 */
interface _DatabaseTable {
	id: string
	name: string
}

/**
 * @private
 */
interface _DatabaseSchema {
	id: string
	name: string
	tables: Table[]
}

export interface DatabaseEndpoint {
	id: number
	methods: string
	endpoint: string
	endpoint_uuid: string
  database_schema: _DatabaseSchema
}
