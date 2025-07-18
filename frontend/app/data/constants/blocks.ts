export const blockTypes = [
  {
    name: 'Table',
    component: 'table-block',
    icon: 'table'
  },
  {
    name: 'Calendar',
    component: 'calendar-block',
    icon: 'calendar'
  },
  {
    name: 'Chart',
    component: 'chart-block',
    icon: 'chart-simple'
  },
  {
    name: 'Grid',
    component: 'grid-by-two-block',
    icon: 'table-cells-large'
  }
] as const

export type BlockTypeNames = (typeof blockTypes)[number]['name']

export type BlockTypeComponents = (typeof blockTypes)[number]['component']
