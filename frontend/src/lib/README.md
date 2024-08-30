This directory contains the subdirectories `api`, `context`, and `hooks`. After you ran
```bash
npm run generate:client
```
it should also contain the subdirectory `client`.
`generate:client` serves as a Software Development Kit (SDK) for interacting with the backend.

## api
`client.ts` creates an instance of the KunstgraphClient class with a base URL for the API.

## client
All the files in here are automatically generated and should not be edited. The openapi-typescript-codegen library generates Typescript clients based on the OpenAPI specification in the backend.

## context
In `keywordContext.ts`, a React context is defined to manage the list of keywords. These keywords are utilized in the advanced search feature to specify the attributes or relations targeted by a specific query.

## hooks
`getSourceFromSourceAttribute.ts` defines how the sources should be displayed. For example, the internal source identifier "goer" gets displayed as "Kunstsammlung H. Goering".
