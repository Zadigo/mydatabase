import 'vue-router'

export {}

type BaseRouteLabel = 'Home page'
  | 'Project overview'
  | 'Integrations'
  | 'Database: Schema'
  | 'Database: Functions'
  | 'Database: Connections' 
  | 'Database: Tables'
  | 'Database: Triggers'
  | 'Account: settings'

type SettingsRouteLabel = 'Settings: Home'
  | 'Settings: Endpoints'
  | 'Settings: Api Keys'

type EditorRouteLabel = 'Editor: Table'

declare module 'vue-router' {
  interface RouteMeta {
    label?: BaseRouteLabel | SettingsRouteLabel | EditorRouteLabel
  }
}
