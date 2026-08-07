import { expect, test } from '@playwright/test'
import { faker } from '@faker-js/faker'

test('get existing databases, go to a database and check the tables', { tag: '@userWorkflowPrimary' }, async ({ page }) => {})

test('get existing databases, go to a database and edit it', { tag: '@userWorkflowPrimary' }, async ({ page }) => {
  // Go to the databases page
  void page.goto('/databases')

  // Get the list of databases
  const linkEl = page.getByRole('link', { name: /test-database/ })
  
  await expect(linkEl).toBeVisible()
  await linkEl.click()

  // Check that the database page is loaded
  await expect(page).toHaveURL(/\/databases\/\d+/)

  // Go to the table editor page
  const tableEditorLink = page.getByRole('link', { name: /Table editor/ })
  await tableEditorLink.click()
  
  await page.waitForSelector('aside', { state: 'visible' })

  const aside = page.locator('aside', { hasText: 'Table Editor' })
  const createButton = page.locator('button', { hasText: /Create/ })
  await expect(aside.or(createButton).first()).toBeVisible()

  // Open the modal to create a new table
  const createTableButton = aside.getByRole('button', { name: /Create/ })
  await createTableButton.click()

  // Enter a new name for the table and save it
  const tableNameInput = page.getByPlaceholder(/Document [nN]ame/)

  await expect(tableNameInput).toBeVisible()
  await expect(tableNameInput).toBeEnabled()

  await tableNameInput.fill(`test-table-${faker.string.alphanumeric({ length: { min: 3, max: 5 } })}`)
  const saveButton = page.getByRole('button', { name: /Create/ })

  await expect(saveButton).toBeEnabled()
  await saveButton.click()

  // Select the newly created table
  const selectButton = page.locator('button').filter({ hasText: 'Select a table' })
  await expect(selectButton).toBeEnabled()
  await selectButton.click()

  // Upload new CSV file: As file

  // Upload new CSV file: From url

  // Check that the table is updated
})

