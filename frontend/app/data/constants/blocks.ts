export const blockTypes: BlockType[] = [
  {
    name: 'Table',
    component: 'table-block',
    icon: 'i-fa-solid:table'
  },
  {
    name: 'Calendar',
    component: 'calendar-block',
    icon: 'i-fa-solid:calendar'
  },
  {
    name: 'Chart',
    component: 'chart-block',
    icon: 'i-fa-solid:chart-area'
  },
  {
    name: 'Grid',
    component: 'grid-by-two-block',
    icon: 'i-fa6-solid:table-cells-large'
  }
] as const

export type BlockTypeNames = (typeof blockTypes)[number]['name']

export type BlockTypeComponents = (typeof blockTypes)[number]['component']

export interface BlockType {
  name: string
  component: BlockTypeNames
  icon: string
}
