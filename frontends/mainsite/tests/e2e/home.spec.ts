import { test } from '@playwright/test'

test('should load the home page', async ({ page }) => {
  await page.goto('/')
  await page.waitForSelector('a')
})
