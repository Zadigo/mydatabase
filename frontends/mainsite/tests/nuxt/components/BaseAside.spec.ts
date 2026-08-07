import { mountSuspended } from '@nuxt/test-utils/runtime'
import { describe, it, expect } from 'vitest'
import BaseAside from '~/components/BaseAside.vue'
import EditAsideLinks from '~/components/editor/AsideLinks.vue'
import DatabaseAsideLinks from '~/components/database/AsideLinks.vue'
import SettingsAsideLinks from '~/components/settings/project/AsideLinks.vue'

describe('BaseAside component', () => {
  const cases: ('editor' | 'database' | 'settings' | 'none')[] = ['editor', 'database', 'settings', 'none']

  cases.forEach((displayMode) => {
    it(`should render correctly with ${ displayMode } prop`, async () => {
      const component = await mountSuspended(BaseAside, {
        props: {
          asideName: displayMode
        }
      })
      expect(component.find('h2')).toBeDefined()

      if (displayMode === 'editor') {
        expect(component.findComponent(EditAsideLinks)).toBeDefined()
      }

      if (displayMode === 'database') {
        expect(component.findComponent(DatabaseAsideLinks)).toBeDefined()
      }
      
      if (displayMode === 'settings') {
        expect(component.findComponent(SettingsAsideLinks)).toBeDefined()
      }
    })
  })
})
