import { expect, test } from '@playwright/test'

test('should show available databases created by the user', { tag: '@userWorkflowPrimary' }, async ({ page }) => {
  await page.goto('/databases')
  
  const inputEl = page.getByRole('textbox', { name: 'Search databases' })
  await inputEl.waitFor({ state: 'visible' })

  // Get the list of databases
  const databaseEls = page.locator('a[id^="link-content-"]')
  await expect(databaseEls.first()).toBeEnabled()
})

test('should be able to create a new database', { tag: '@userWorkflowPrimary' }, async ({ page }) => {
  await page.goto('/databases')

  const inputEl = page.getByRole('textbox', { name: 'Search databases' })
  await inputEl.waitFor({ state: 'visible' })

  // The model should not be visible at first
  const dialogEl = page.getByRole('dialog', { name: 'Create Database' })
  await dialogEl.waitFor({ state: 'hidden' })
  
  // Click the button to open the modal
  await page.getByRole('button', { name: 'Create Database' }).click()

  // The model should now be visible
  await dialogEl.waitFor({ state: 'visible' })

  // Fill in the form and submit
  await page.getByRole('textbox', { name: 'Name' }).fill('test-database')
  await page.getByRole('button', { name: 'Create New Database' }).click()
})

test('should be able to search the databases', { tag: '@userWorkflowSecondary' }, async ({ page }) => {
  await page.goto('/databases')
  
  const inputEl = page.getByRole('textbox', { name: 'Search databases' })
  await inputEl.waitFor({ state: 'visible' })

  // Type in the search input
  await inputEl.fill('test-database')

  // Check that the database is visible in the list
  const databaseEl = page.getByRole('link', { name: 'test-database' })
  await databaseEl.waitFor({ state: 'visible' })
})
