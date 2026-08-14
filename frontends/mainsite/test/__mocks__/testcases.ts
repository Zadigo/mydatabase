type ComponentOptions<T> = {
  props: T
}

type InferValueType<T> =
  T extends string ? string :
  T extends number ? number :
  T extends boolean ? boolean :
  T extends object ? object :
  unknown

type Conditions<T extends unknown = string | number | boolean | object> = {
  /**
   * The value to be test for
   */
  testValue: T | null | undefined
  /**
   * Expected value for the test
   */
  expectedValue: InferValueType<T> | null | undefined
  /**
   * Expected length of an object
   */
  expectedLength?: number
  /**
   * A conditional function that expects to return
   * an expected value for the test. This result of the
   * function will override `testValue`
   * @param t The current test case
   */
  conditionalTestValue?: <R extends InferValueType<T>>(t: TestCase) => R
  /**
   * Whether to skip the case
   * @default false
   */
  skip: boolean
  /**
   * Whether the case should use authentication
   * @default false
   */
  isAuthenticated: boolean
}

type TestCase = {
  title: string
} & Partial<ComponentOptions<Record<string, unknown>>> & Partial<Conditions>

// type TestCases = TestCase[]

type UuidTestCase = TestCase & { uuid: string }

type UuidTestCases = UuidTestCase[]

export function defineTestCase(testCase: TestCase): UuidTestCase {
  return { ...testCase, uuid: crypto.randomUUID() }
}

class TestCaseManager {
  private cases: UuidTestCases = []

  constructor() {
    this.cases = []
  }

  get runner(): UuidTestCases {
    return this.cases
      .flatMap((testCase) => testCase)
      .filter((testCase) => !testCase.skip)
  }

  parameterize(testCase: TestCase[]): TestCaseManager {
    this.cases.push(...testCase.map((tc) => ({ ...tc, uuid: crypto.randomUUID() })))
    this.cases.forEach((testCase) => {
      if (testCase.conditionalTestValue) {
        testCase.testValue = testCase.conditionalTestValue(testCase)
      }
    })
    return this
  }

  caseForFailure<K extends keyof UuidTestCase[ 'props' ]>(fields: K[], ...args: string[]) {
    const candidates = this.cases.filter((testCase) => args.includes(testCase.title))
    candidates.forEach((testCase) => {
      this.cases.push({
        ...testCase,
        skip: true,
        props: fields.reduce((acc, field) => {
          if (testCase.props && field in testCase.props) {
            acc[ field ] = undefined
          }
          return acc
        }, {} as Record<string, unknown>)
      })
    })
    return this.runner
  }
}

export function definedTestCases(callback: (manager: TestCaseManager) => TestCaseManager): TestCaseManager {
  return callback(new TestCaseManager())
}
