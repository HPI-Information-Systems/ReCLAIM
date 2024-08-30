# E2E Tests

This directory contains end-to-end tests for the project. These tests are written in Typescript and use the [Playwright](https://playwright.dev/) library to interact with the browser.

## Running the tests

To run the tests, please run

```bash
npm run test:e2e
```

This will start the test runner and run all the tests in the `e2e_tests` directory.

To run the tests in an interactive ui mode, please run

```bash
npm run test:e2e:ui
```

## Installing playwright

Should the playwright browsers not be installed, please run the following command to install them:

```bash
npx playwright install
```

## Writing tests

To write a new test, please create a new file in the `tests/` directory. The file should have the extension `.spec.ts`. Each function in the file should be a test case.

For example:

```typescript
import { test, expect } from "@playwright/test";

test("should open the homepage", async ({ page }) => {
  await page.goto("http://localhost:3000");
  const title = await page.title();
  expect(title).toBe("Homepage");
});
```
