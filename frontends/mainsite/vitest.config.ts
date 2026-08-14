import { defineConfig } from 'vitest/config'
import { defineVitestProject } from '@nuxt/test-utils/config'

export default defineConfig({
  test: {
    setupFiles: ['./tests/setup.ts'],
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
          include: ['test/nuxt/**/*.{test,spec}.ts'],
          environment: 'nuxt',
          testTimeout: 20000,
          tags: [
            {
              name: 'nuxt',
              description: 'Tests for Nuxt'
            },
            {
              name: 'composables',
              description: 'Tests for composables'
            },
            {
              name: 'pages',
              description: 'Tests for pages'
            }
          ]
        }
      }),
      await defineVitestProject({
        test: {
          name: 'integration',
          include: ['test/integration/**/*.{test,spec}.ts'],
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
