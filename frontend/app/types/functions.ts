import type { Nullable } from '.'
import type { baseDatabaseFunctions} from '~/utils'

export type DatabaseFunctions = typeof baseDatabaseFunctions[number]

export type FunctionReturnTypes = typeof functionReturnTypes[number]

export type FunctionFailures = typeof functionFailures[number]

interface FunctionReturnBody {
	type: FunctionReturnTypes
  value: string
}

interface FailureBody {
	do: FunctionFailures;
  default_value: string
}

export interface FunctionSignals {
  failure: FailureBody
}

export interface FunctionBody {
	name: string
	table: Nullable<number>
	columns: string[]
	returns: FunctionReturnBody
	chain_to: string[]
	signals: FunctionSignals
}

export type DatabaseFunction = {
	function: FunctionBody
}
