/**
 * Task API client functions.
 *
 * Following API client patterns from app/frontend/src/api/ in main project.
 */
import {
  Task,
  CreateTaskRequest,
  UpdateTaskRequest,
} from "../types/task";

const API_BASE = "/api";

const handleJsonResponse = async <T>(response: Response): Promise<T> => {
  if (!response.ok) {
    let message = `Request failed with status ${response.status}`;

    try {
      const body = await response.json();
      if (body && typeof body === "object" && "error" in body) {
        message = (body as any).error ?? message;
      }
    } catch {
      // ignoramos errores al parsear JSON
    }

    throw new Error(message);
  }

  return response.json() as Promise<T>;
};

/**
 * Fetch all tasks.
 */
export const getTasks = async (): Promise<Task[]> => {
  const response = await fetch(`${API_BASE}/tasks`);
  return handleJsonResponse<Task[]>(response);
};

/**
 * Fetch single task by ID.
 */
export const getTask = async (id: number): Promise<Task> => {
  const response = await fetch(`${API_BASE}/tasks/${id}`);
  return handleJsonResponse<Task>(response);
};

/**
 * Create a new task.
 */
export const createTask = async (
  data: CreateTaskRequest,
): Promise<Task> => {
  const response = await fetch(`${API_BASE}/tasks`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  return handleJsonResponse<Task>(response);
};

/**
 * Update an existing task.
 */
export const updateTask = async (
  id: number,
  data: UpdateTaskRequest,
): Promise<Task> => {
  const response = await fetch(`${API_BASE}/tasks/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  return handleJsonResponse<Task>(response);
};

/**
 * Delete a task.
 */
export const deleteTask = async (id: number): Promise<void> => {
  const response = await fetch(`${API_BASE}/tasks/${id}`, {
    method: "DELETE",
  });

  if (!response.ok) {
    let message = `Request failed with status ${response.status}`;

    try {
      const body = await response.json();
      if (body && typeof body === "object" && "error" in body) {
        message = (body as any).error ?? message;
      }
    } catch {
      // ignoramos errores al parsear JSON
    }

    throw new Error(message);
  }

  // 204 sin contenido → devolvemos void
};
