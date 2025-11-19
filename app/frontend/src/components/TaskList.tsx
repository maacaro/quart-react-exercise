/**
 * TaskList Component
 * Displays a list of tasks with actions
 */
import { Task } from '../types/task';

interface TaskListProps {
  tasks: Task[];
  onUpdate: (id: number, data: Partial<Task>) => Promise<void>;
  onDelete: (id: number) => Promise<void>;
}

function TaskList({ tasks, onUpdate, onDelete }: TaskListProps) {
  /**
   * TODO: Implement this component
   *
   * Requirements:
   * - Display all tasks in a list
   * - Show task title, description, and status for each task
   * - Provide a button or dropdown to change task status
   * - Provide a delete button for each task
   * - Handle empty state (no tasks)
   *
   * Hints:
   * - Map over the tasks array to render each task
   * - Use the onUpdate callback when status changes
   * - Use the onDelete callback when delete button is clicked
   * - Consider using a select dropdown for status changes
   * - Add loading/disabled states during async operations
   */

  if (tasks.length === 0) {
    return <div className="task-list-empty">No tasks yet. Create one to get started!</div>;
  }

  return (
    <div className="task-list">
      {/* TODO: Render tasks here */}
      <p>Task list rendering not implemented yet</p>
    </div>
  );
}

export default TaskList;
