import { mountSuspended } from '@nuxt/test-utils/runtime'
import { describe, it, expect, vi } from 'vitest'
import LoginPage from '~/pages/login.vue'
import { faker } from '@faker-js/faker'

vi.stubGlobal('$fetch', vi.fn((url: string, options: any) => {
  if (url === '/api/auth/login' && options.method === 'POST') {
    return Promise.resolve({ success: true })
  }
  return Promise.reject(new Error('Unknown API endpoint'))
}))

describe('LoginPage', { tags: ['nuxt_page'] }, () => {
  it('should render page correctly', async () => {
    const component = await mountSuspended(LoginPage)
    
    const formEl = component.find('form#form-login')
    expect(formEl).toBeDefined()

    const buttonEl = component.find('button#action-login')
    expect(buttonEl).toBeDefined()
  })

  const expectedInputFields = [
    { name: 'email', type: 'text' },
    { name: 'password', type: 'password' }
  ]

  expectedInputFields.forEach((field) => {
    it(`should have input field for ${field.name}`, async () => {
      const component = await mountSuspended(LoginPage)
      const inputEl = component.find(`input[name="${field.name}"]`)

      expect(inputEl).toBeDefined()
      expect(inputEl.attributes('type')).toBe(field.type)
      expect(inputEl.attributes('disabled')).toBeUndefined()
    })
  })

  it('should call login function when login button is clicked', async () => {
    const component = await mountSuspended(LoginPage)
    const buttonEl = component.find('button#action-login')

    const email = component.find('input[name="email"]')
    const password = component.find('input[name="password"]')

    await email.setValue(faker.internet.email())
    await password.setValue(faker.internet.password())

    await buttonEl.trigger('click')
    
    // Check for navigation to have been triggered
    expect(component.vm.$router.currentRoute.value.fullPath).toBe('/')
  })
})
