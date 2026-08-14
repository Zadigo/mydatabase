import { describe, it, expect } from 'vitest'


describe.todo('urlPrefetchViaHttp', () => {
  it('should return a preview of the data fetched from the given URL', async () => {
    const source = ref<string>()

    const preview = urlPrefetchViaHttp<{ todo: string }>(source, {
      fileType: 'json'
    })

    expect(toValue(preview)).toBeUndefined()

    // Trigger the fetch by setting the source value
    source.value = 'https://jsonplaceholder.typicode.com/todos'

    await nextTick(() => {
      expect(toValue(preview)).toBeDefined()
      console.log(preview.value)

    })
  })
})
