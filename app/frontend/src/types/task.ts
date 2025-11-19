/**
 * Task entity type definition
 */
export interface Task {
  id: number;
  title: string;
  description: string;
  status: 'pending' | 'in_progress' | 'completed';
  created_at: string;
  updated_at: string;
}

/**
 * Data for creating a new task
 */
export interface CreateTaskData {
  title: string;
  description: string;
  status?: 'pending' | 'in_progress' | 'completed';
}

/**
 * Data for updating an existing task
 */
export interface UpdateTaskData {
  title?: string;
  description?: string;
  status?: 'pending' | 'in_progress' | 'completed';
}
