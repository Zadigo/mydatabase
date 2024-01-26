export function useRules () {
  function maxLength (value) {
    // Checks that the maximum length for a given string
    // entered by the user respects a certain length
    return value.length < 50 || 'Value should be 50 characters long'
  }

  function isNotNull (value) {
    // Checks that the value is not null
    // or is not an empty string
    return value && value !== "" || 'Value should not be empty'
  }

  return {
    maxLength,
    isNotNull
  }
}
