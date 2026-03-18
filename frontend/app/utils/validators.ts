interface Rule {
  type: 'string' | 'number' | 'boolean' | 'array' | 'object' | 'date' | 'email' | 'url' | 'ip' | 'mac' | 'sameAs'
  field: string
  value?: MaybeRefOrGetter<unknown>
  validator?: (value: unknown) => boolean | Promise<boolean>
  message?: string,
  isValid?: boolean,
  flag?: 'neutral' | 'success' | 'error' | 'warning' | 'info'
}

export function useValidators<S extends MaybeRefOrGetter<Record<string, unknown>>>() {
  function required(value: S[keyof S]) {
    return value !== undefined && value !== null && value !== ''
  }

  function requiredIf(condition: boolean) {
    return (value: S[keyof S]) => {
      if (condition) {
        return required(value)
      }
      return true
    }
  }

  function requiredUnless(condition: boolean) {
    return (value: S[keyof S]) => {
      if (!condition) {
        return required(value)
      }
      return true
    }
  }

  function minLength(length: number) {
    return (value: S[keyof S]) => {
      if (typeof value === 'string') {
        return value.length >= length
      }
      return true
    }
  }

  function maxLength(length: number) {
    return (value: S[keyof S]) => {
      if (typeof value === 'string') {
        return value.length <= length
      }
      return true
    }
  }

  function minValue(value: number) {
    return (value: S[keyof S]) => {
      if (typeof value === 'number') {
        return value >= minValue
      }
      return true
    }
  }

  function maxValue(value: number) {
    return (value: S[keyof S]) => {
      if (typeof value === 'number') {
        return value <= maxValue
      }
      return true
    }
  }

  function between(min: number, max: number) {
    return (value: S[keyof S]) => {
      if (typeof value === 'number') {
        return value >= min && value <= max
      }
      return true
    }
  }

  function onlyAlphabet() {
    return (value: S[keyof S]) => {
      if (typeof value === 'string') {
        return /^[A-Za-z]+$/.test(value)
      }
      return true
    }
  }

  function alphaNumeric() {
    return (value: S[keyof S]) => {
      if (typeof value === 'string') {
        return /^[A-Za-z0-9]+$/.test(value)
      }
      return true
    }
  }

  function numeric() {
    return (value: S[keyof S]) => {
      if (typeof value === 'string' || typeof value === 'number') {
        return !isNaN(Number(value))
      }
      return true
    }
  }
  
  function integer() {
    return (value: S[keyof S]) => {
      if (typeof value === 'string' || typeof value === 'number') {
        return Number.isInteger(Number(value))
      }
      return true
    }
  }

  function decimal() {
    return (value: S[keyof S]) => {
      if (typeof value === 'string' || typeof value === 'number') {
        return !isNaN(Number(value)) && !Number.isInteger(Number(value))
      }
      return true
    }
  }

  function email() {
    return (value: S[keyof S]) => {
      if (typeof value === 'string') {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)
      }
      return true
    }
  }

  function ipAddress() {
    return (value: S[keyof S]) => {
      if (typeof value === 'string') {
        return /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test(value)
      }
      return true
    }
  }

  function macAddress() {
    return (value: S[keyof S]) => {
      if (typeof value === 'string') {
        return /^([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})$/.test(value)
      }
      return true
    }
  }

  function sameAs() {
    return (value: S[keyof S], otherField: keyof S) => {
      return value === form[otherField]
    }
  }

  function url() {
    return (value: S[keyof S]) => {
      if (typeof value === 'string') {
        try {
          new URL(value)
          return true
        } catch {
          return false
        }
      }
      return true
    }
  }

  function or(...validators: Array<(value: S[keyof S]) => boolean | Promise<boolean>>) {
    return async (value: S[keyof S]) => {
      for (const validator of validators) {
        const result = validator(value)
        if (result instanceof Promise) {
          if (await result) {
            return true
          }
        } else if (result) {
          return true
        }
      }
      return false
    }
  }

  function asyncOr(...validators: Array<(value: S[keyof S]) => boolean | Promise<boolean>>) {
    return async (value: S[keyof S]) => or(...validators)(value)
  }

  function and(...validators: Array<(value: S[keyof S]) => boolean | Promise<boolean>>) {
    return async (value: S[keyof S]) => {
      for (const validator of validators) {
        const result = validator(value)
        if (result instanceof Promise) {
          if (!(await result)) {
            return false
          }
        } else if (!result) {
          return false
        }
      }
      return true
    }
  }

  function asyncAnd(...validators: Array<(value: S[keyof S]) => boolean | Promise<boolean>>) {
    return async (value: S[keyof S]) => and(...validators)(value)
  }

  function not() {
    return (value: S[keyof S], validator: (value: S[keyof S]) => boolean | Promise<boolean>) => {
      const result = validator(value)
      if (result instanceof Promise) {
        return result.then(res => !res)
      }
      return !result
    }
  }

  return {
    required,
    requiredIf,
    requiredUnless,
    minLength,
    maxLength,
    minValue,
    maxValue,
    between,
    onlyAlphabet,
    alphaNumeric,
    numeric,
    integer,
    decimal,
    email,
    ipAddress,
    macAddress,
    sameAs,
    url,
    or,
    asyncOr,
    and,
    asyncAnd,
    not
  }
}

export function useTesting<S extends MaybeRefOrGetter<Record<string, unknown>>>(schema: S, rules: Rule[]) {
  const _rules = ref(rules)
  
  async function _validate() {
    const _schema = toValue(schema)
    for (const rule of _rules.value) {
      if (rule.validator) {
        if (rule.validator.constructor.name === 'AsyncFunction') {
          rule.isValid = await rule.validator(_schema[ toValue(rule.field) ])
        } else {
          rule.isValid = rule.validator(_schema[ toValue(rule.field) ])
        }

        if (rule.isValid) {
          rule.flag = 'success'
        } else {
          rule.flag = 'error'
        }
      } 
    }
  }

  const { trigger: validate } = watchTriggerable(_rules, _validate, { immediate: true, deep: true })

  const errors = computed(() => {
    return _rules.value.map(rule => ({
      field: rule.field,
      message: rule.message,
      isValid: rule.isValid,
      flag: rule.flag
    }))
  })

  return {
    validate,
    errors
  }
}

// type Data = { name: string }
// const form = ref<Data>({ name: 'John' })
// const { required } = useValidators<Data>()
// const { errors } = useTesting<Data>(form, [
//   {
//     type: 'string',
//     field: 'name',
//     validator: required,
//     message: 'Name is required',
//     value: ref('John')
//   }
// ])
