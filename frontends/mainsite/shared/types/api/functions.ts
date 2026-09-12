export type DatabaseFunctions = typeof BASE_DATABASE_FUNCTIONS[number]

export type FunctionReturnTypes = typeof FUNCTION_RETURN_TYPES[number]

export type FunctionFailures = typeof FUNCTION_FAILURES[number]

interface FunctionReturnBody {
  type: FunctionReturnTypes
  value: string
}

interface FailureBody {
  do: FunctionFailures
  default_value: string
}

export interface FunctionSignals {
  failure: FailureBody
}

export interface FunctionBody {
  name: string
  table: string
  columns: string[]
  returns: FunctionReturnBody
  chain_to: string[]
  signals: FunctionSignals
}

export type DatabaseFunction = {
  function: FunctionBody
}
