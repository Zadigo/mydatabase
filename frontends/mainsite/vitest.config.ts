import { defineConfig } from 'vitest/config'
import { defineVitestProject } from '@nuxt/test-utils/config'

export default defineConfig({
  test: {
    // setupFiles: [ './tests/setup.ts' ],
    exclude: [
      'node_modules',
      '.nuxt',
      'dist',
      'tests/__fixtures__',
      'tests/e2e'
    ],
    coverage: {
      enabled: true,
      provider: 'v8',
      reporter: [ 'text', 'json', 'html' ]
    },
    env: {
      NODE_ENV: 'test',
      MODE: 'test'
    },
    projects: [
      await defineVitestProject({
        test: {
          name: 'nuxt',
          include: ['tests/nuxt/**/*.{test,spec}.ts'],
          environment: 'nuxt',
          testTimeout: 20000,
          tags: [
            {
              name: 'nuxt',
              description: 'Tests for Nuxt'
            },
            {
              name: 'unit',
              description: 'Tests for composables'
            },
            {
              name: 'nuxt_page',
              description: 'Tests for pages'
            }
          ]
        }
      }),
      await defineVitestProject({
        test: {
          name: 'integration',
          include: ['tests/integration/**/*.{test,spec}.ts'],
          environment: 'node',
          testTimeout: 20000,
          tags: [
            {
              name: 'integration',
              description: 'Integration tests'
            }
          ]
        }
      })
    ]
  },
  resolve: {}
})
