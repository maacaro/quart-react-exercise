/**
 * Task entity type definition
 */

export type TaskStatus = "pending" | "in_progress" | "completed";

export interface Task {
  id: number;
  title: string;
  description: string;
  status: TaskStatus;
  created_at: string;
  updated_at: string;
}

/**
 * Data for creating a new task
 *
 * (Assignment style: CreateTaskRequest)
 */
export interface CreateTaskRequest {
  title: string;
  description?: string;
  status?: TaskStatus;
}

/**
 * Data for updating an existing task
 *
 * (Assignment style: UpdateTaskRequest)
 */
export interface UpdateTaskRequest {
  title?: string;
  description?: string;
  status?: TaskStatus;
}

/**
 * Backwards-compat aliases so nada revienta si el starter code
 * o algún import viejo usa CreateTaskData / UpdateTaskData
 */
export type CreateTaskData = CreateTaskRequest;
export type UpdateTaskData = UpdateTaskRequest;
