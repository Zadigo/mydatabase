import type { DatabaseEndpoint } from '~/types/databases/endpoints'

export const endpointsFixture: DatabaseEndpoint[] = [
  {
    id: 1,
    methods: "GET",
    endpoint: "my-database",
    endpoint_uuid: "98da4160-cf18-492e-9a82-0eb204eb6abe",
    database_schema: {
      id: "49",
      name: "My new database",
      tables: [
        {
          id: "22",
          name: "My quick table"
        }
      ]
    }
  }
]

