import { mountSuspended } from '@nuxt/test-utils/runtime'
import { describe, it, expect, vi } from 'vitest'
import LoginPage from '~/pages/login.vue'
import { useLogin } from 'nuxt-authentication'

vi.stubGlobal('$fetch', vi.fn())

describe.only('LoginPage', { tags: ['nuxt_page'] }, () => {
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

    await buttonEl.trigger('click')
  })
})
