/**
 * Task API Client
 * Functions for communicating with the backend API
 */
import { Task, CreateTaskData, UpdateTaskData } from '../types/task';

const API_BASE_URL = '/api';

/**
 * Fetch all tasks from the API
 *
 * @returns Promise<Task[]> Array of all tasks
 *
 * TODO: Implement this function
 * Hints:
 * - Use fetch() to make GET request to /api/tasks
 * - Parse JSON response
 * - Handle errors appropriately
 */
export async function fetchTasks(): Promise<Task[]> {
  // TODO: Implement
  throw new Error('Not implemented');
}

/**
 * Fetch a single task by ID
 *
 * @param id - Task ID
 * @returns Promise<Task> The requested task
 *
 * TODO: Implement this function
 * Hints:
 * - Use fetch() to make GET request to /api/tasks/${id}
 * - Parse JSON response
 * - Handle 404 errors
 */
export async function fetchTaskById(id: number): Promise<Task> {
  // TODO: Implement
  throw new Error('Not implemented');
}

/**
 * Create a new task
 *
 * @param data - Task data (title, description, status)
 * @returns Promise<Task> The created task
 *
 * TODO: Implement this function
 * Hints:
 * - Use fetch() to make POST request to /api/tasks
 * - Set Content-Type header to application/json
 * - Send JSON stringified data in body
 * - Parse JSON response
 */
export async function createTask(data: CreateTaskData): Promise<Task> {
  // TODO: Implement
  throw new Error('Not implemented');
}

/**
 * Update an existing task
 *
 * @param id - Task ID
 * @param data - Fields to update
 * @returns Promise<Task> The updated task
 *
 * TODO: Implement this function
 * Hints:
 * - Use fetch() to make PUT request to /api/tasks/${id}
 * - Set Content-Type header to application/json
 * - Send JSON stringified data in body
 * - Parse JSON response
 * - Handle 404 errors
 */
export async function updateTask(id: number, data: UpdateTaskData): Promise<Task> {
  // TODO: Implement
  throw new Error('Not implemented');
}

/**
 * Delete a task
 *
 * @param id - Task ID
 * @returns Promise<void>
 *
 * TODO: Implement this function
 * Hints:
 * - Use fetch() to make DELETE request to /api/tasks/${id}
 * - No response body expected (204 status)
 * - Handle 404 errors
 */
export async function deleteTask(id: number): Promise<void> {
  // TODO: Implement
  throw new Error('Not implemented');
}
