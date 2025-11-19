/**
 * End-to-End tests for task management
 *
 * These tests verify the complete user flow through the application
 *
 * Run tests with: npm run test:e2e
 * Run in UI mode: npm run test:e2e:ui
 * Run in debug mode: npm run test:e2e:debug
 */
import { test, expect } from '@playwright/test';

test.describe('Task Management', () => {

  test.beforeEach(async ({ page }) => {
    // Navigate to the app before each test
    await page.goto('/');
  });

  test('should display the task manager page', async ({ page }) => {
    /**
     * TODO: Implement this test
     * Steps:
     * 1. Check that the page title contains "Task Manager"
     * 2. Verify the task form is visible
     * 3. Verify the task list is visible
     */

    // Example assertions:
    // await expect(page.locator('h1')).toContainText('Task Manager');
  });

  test('should create a new task', async ({ page }) => {
    /**
     * TODO: Implement this test
     * Steps:
     * 1. Fill in the task form (title, description, status)
     * 2. Click the create button
     * 3. Verify the new task appears in the task list
     * 4. Verify the form is cleared after submission
     */
  });

  test('should display empty state when no tasks exist', async ({ page }) => {
    /**
     * TODO: Implement this test
     * Steps:
     * 1. Verify the empty state message is visible
     * 2. Verify it says something like "No tasks yet"
     */
  });

  test('should update task status', async ({ page }) => {
    /**
     * TODO: Implement this test
     * Steps:
     * 1. Create a task with status "pending"
     * 2. Change the status to "in_progress"
     * 3. Verify the status is updated in the UI
     * 4. Change the status to "completed"
     * 5. Verify the status is updated in the UI
     */
  });

  test('should delete a task', async ({ page }) => {
    /**
     * TODO: Implement this test
     * Steps:
     * 1. Create a task
     * 2. Click the delete button
     * 3. Verify the task is removed from the list
     * 4. Optionally: Verify a confirmation dialog appears
     */
  });

  test('should handle form validation', async ({ page }) => {
    /**
     * TODO: Implement this test
     * Steps:
     * 1. Try to submit the form without filling required fields
     * 2. Verify validation errors appear or submit is prevented
     * 3. Fill in the required fields
     * 4. Verify the form can now be submitted
     */
  });

  test('should persist tasks after page reload', async ({ page }) => {
    /**
     * TODO: Implement this test
     * Steps:
     * 1. Create a task
     * 2. Reload the page
     * 3. Verify the task is still visible
     */
  });

  test('should handle multiple tasks', async ({ page }) => {
    /**
     * TODO: Implement this test
     * Steps:
     * 1. Create 3-5 tasks with different statuses
     * 2. Verify all tasks are displayed
     * 3. Update one task's status
     * 4. Delete one task
     * 5. Verify the correct tasks remain
     */
  });

});

/**
 * BONUS: Advanced E2E tests
 */
test.describe('Advanced Task Management', () => {

  test.skip('should handle concurrent updates gracefully', async ({ page }) => {
    /**
     * TODO: Implement this advanced test
     * Test how the app handles race conditions
     */
  });

  test.skip('should show loading states during API calls', async ({ page }) => {
    /**
     * TODO: Implement this advanced test
     * Verify loading indicators appear during async operations
     */
  });

  test.skip('should display error messages when API fails', async ({ page }) => {
    /**
     * TODO: Implement this advanced test
     * Simulate API failures and verify error handling
     */
  });

});
