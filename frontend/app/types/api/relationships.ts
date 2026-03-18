/**
 * @private
 */
interface Fields {
	left: string
	right: string
}

/**
 * @private
 */
interface Metadata {
	type: '1-1' | '1-many' | 'many-1' | 'many-many'
}

/**
 * @private
 */
interface Table {
	from: string
	to: string
  fields: Fields
	meta: Metadata
}

export interface TableRelationship {
	table: Table
}
