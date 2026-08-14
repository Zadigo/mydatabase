import type { H3Event } from 'h3'

type Options = {
  body: Record<string, unknown>
  params: Record<string, unknown>
  query: Record<string, unknown>
}

/**
 * Mock function to create a mock H3Event object for testing purposes.
 * @link https://dev.to/doantrongnam/a-developers-guide-to-unit-testing-nuxt-3-server-routes-4f55
 * @param event 
 */
export function mockH3Event(event: Partial<H3Event> & Partial<Options>) {
  const e = {
    node: {
      req: {
        headers: { 'content-type': 'application/json' },
        method: 'POST',
      }
    },
    context: {
      params: event.params || {},
      query: event.query || {},
    },
    // Our mock readBody function will look for this property
    _requestBody: event.body,
  }
  return { ...e, ...event } as H3Event
}

// export type TestCase<P> = {
//   title: string
//   props?: P
// }

// export function defineTestCase<T>(title: string, testCaseProps?: T): TestCase<T> {
//   return {
//     title,
//     props: testCaseProps
//   }
// }

// export function defineTestCases<T>(cases: ReturnType<typeof defineTestCase<T>>[]): TestCase<T>[] {
//   return cases.flatMap((testCase) => testCase)
// }


// defineTestCases(
//   defineTestCase('should render correctly with default props', {
//     something: 'value'
//   })
// )
