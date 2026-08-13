import { test } from '@playwright/test'
import { faker } from '@faker-js/faker'

test.describe('Waitlist API', () => {
  test.describe.configure({ timeout: 60000 })

  test('should return 200 OK for valid waitlist data', async ({ request }) => {
    const response = await request.post('/api/waitlist', {
      data: {
        email: faker.internet.email(),
        firstname: faker.person.firstName(),
        lastname: faker.person.lastName(),
        company: faker.company.name(),
        url: faker.internet.url()
      }
    })
    test.expect(response.status()).toBe(200)
  })

  test('should return 400 Bad Request for invalid waitlist data', async ({ request }) => {
    const response = await request.post('/api/waitlist', {
      data: {
        email: 'invalid-email',
        firstname: '',
        lastname: '',
        company: '',
        url: ''
      }
    })
    test.expect(response.status()).toBe(400)
  })
})
