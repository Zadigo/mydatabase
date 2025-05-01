import { dirname, resolve } from 'path'
import { fileURLToPath } from 'url'
import { defineConfig, loadEnv } from 'vite'

import vue from '@vitejs/plugin-vue'
import eslint from 'vite-plugin-eslint'
import autoImport from 'unplugin-auto-import/vite'
// import vueI18n from '@intlify/unplugin-vue-i18n/vite'
// import unheadAddons from '@unhead/addons/vite'

export default defineConfig(({ mode }) => {
  const root = process.cwd()
  const env = loadEnv(mode, root)
  process.env = { ...process.env, ...env }

  return {
    root,
    resolve: {
      alias: [
        {
          find: '@',
          replacement: resolve(__dirname, 'src')
        },
        {
          find: 'src',
          replacement: resolve(__dirname, 'src')
        }
      ]
    },
    plugins: [
      vue(),
      eslint(),
      autoImport({
        include: [
          /\.vue$/,
          /\.ts/
        ],
        dts: './auto-imports.d.ts',
        dirs: [
          './composables/**'
        ]
      })
      // vueI18n({
      //   include: resolve(dirname(fileURLToPath(import.meta.url)), './src/locales/**'),
      //   fullInstall: false,
      //   compositionOnly: true
      // })
    ],
    test: {
      globals: true,
      environment: 'happy-dom',
      setupFiles: './tests/setup.ts'
    }
  }
})
