import { expect, test } from "@playwright/test";

test("has title", async ({ page }) => {
  await page.goto("http://localhost:3000/");

  // expect no error
});

test("get started link", async ({ page }) => {
  await page.goto("http://localhost:3000/");
  expect(await page.isVisible("text=Search")).toBeTruthy();
});
