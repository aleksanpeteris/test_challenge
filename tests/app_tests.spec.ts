import { test, expect } from '@playwright/test';

test('has title', async ({ page }) => {
  await page.goto('http://localhost:8000/');

  // Expect a title "to contain" a substring.
  await expect(page).toHaveTitle('Vite + React + TS');
});

test('test file upload, process and simple QNA', async ({ page}) => {
    // TODO create fixtures to clean up uploaded files, move check block to separate methods
    await page.goto('http://127.0.0.1:8000/');

    const file_input = page.locator('input[type="file"]');

    await file_input.click();

    // Choose file to upload
    await file_input.setInputFiles('./tests/fixtures/test_10Mb.pdf');

    const uploadButton = file_input.locator('..').locator('button');

    await expect(uploadButton).toBeEnabled();

    // Upload the file
    await uploadButton.click();

    await expect(page.getByText('test_10Mb.pdf')).toBeVisible();

    // Process the file
    await page.locator('button[aria-label="Process file"]').click();

    // Ask simple question about file name
    // TODO

    // Push button
    //await page.locator('button:text("Ask Question")').click();

    // Expect answer
    // TODO

    // Delete file
    await page.locator('button[aria-label="Delete file"]').click();

});
