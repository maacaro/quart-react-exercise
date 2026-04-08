/**
 * TaskList Component
 * Displays a list of tasks with actions
 */

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

import { useMemo, useState } from "react";
import { Task, TaskStatus } from "../types/task";

interface TaskListProps {
  tasks: Task[];
  onUpdate: (id: number, data: Partial<Task>) => Promise<void>;
  onDelete: (id: number) => Promise<void>;
  onSave?: (task: Task) => Promise<void>; // ✅ NUEVO opcional
}

const STATUS_OPTIONS: { value: TaskStatus; label: string }[] = [
  { value: "pending", label: "Pending" },
  { value: "in_progress", label: "In Progress" },
  { value: "completed", label: "Completed" },
];

function TaskList({ tasks, onUpdate, onDelete, onSave }: TaskListProps) {
  const [updatingIds, setUpdatingIds] = useState<Set<number>>(new Set());
  const [deletingIds, setDeletingIds] = useState<Set<number>>(new Set());
  const [savingIds, setSavingIds] = useState<Set<number>>(new Set());
  const [errorById, setErrorById] = useState<Record<number, string | null>>({});

  const isBusy = useMemo(() => {
    return (id: number) =>
      updatingIds.has(id) || deletingIds.has(id) || savingIds.has(id);
  }, [updatingIds, deletingIds, savingIds]);

  const handleStatusChange = async (task: Task, newStatus: TaskStatus) => {
    setErrorById((prev) => ({ ...prev, [task.id]: null }));
    setUpdatingIds((prev) => new Set(prev).add(task.id));

    try {
      // Usamos el callback cuando cambia el status
      await onUpdate(task.id, { status: newStatus });
    } catch (err) {
      setErrorById((prev) => ({
        ...prev,
        [task.id]: err instanceof Error ? err.message : "Failed to update task",
      }));
    } finally {
      setUpdatingIds((prev) => {
        const next = new Set(prev);
        next.delete(task.id);
        return next;
      });
    }
  };

  const handleDelete = async (id: number) => {
    setErrorById((prev) => ({ ...prev, [id]: null }));
    setDeletingIds((prev) => new Set(prev).add(id));

    try {
      await onDelete(id);
    } catch (err) {
      setErrorById((prev) => ({
        ...prev,
        [id]: err instanceof Error ? err.message : "Failed to delete task",
      }));
    } finally {
      setDeletingIds((prev) => {
        const next = new Set(prev);
        next.delete(id);
        return next;
      });
    }
  };

  const handleSave = async (task: Task) => {
    if (!onSave) return;

    setErrorById((prev) => ({ ...prev, [task.id]: null }));
    setSavingIds((prev) => new Set(prev).add(task.id));

    try {
      await onSave(task);
    } catch (err) {
      setErrorById((prev) => ({
        ...prev,
        [task.id]: err instanceof Error ? err.message : "Failed to save task",
      }));
    } finally {
      setSavingIds((prev) => {
        const next = new Set(prev);
        next.delete(task.id);
        return next;
      });
    }
  };

  if (tasks.length === 0) {
    return (
      <div className="task-list-empty" data-testid="task-list-empty">
        No tasks yet. Create one to get started!
      </div>
    );
  }

  return (
    // ❗ IMPORTANTE: NO usar data-testid="task-list" aquí
    // porque TasksPage ya lo tiene y rompe strict mode
    <div className="task-list" data-testid="task-list-inner">
      {tasks.map((task) => (
        <div key={task.id} className="task-card" data-testid="task-card">
          <div className="task-card-header">
            <h3 className="task-title">{task.title}</h3>
          </div>

          {task.description ? (
            <p className="task-description">{task.description}</p>
          ) : null}

          <div className="task-meta">
            <label>
              Status:{" "}
              <select
                data-testid="task-status-select"
                value={task.status}
                disabled={isBusy(task.id)}
                onChange={(e) =>
                  handleStatusChange(task, e.target.value as TaskStatus)
                }
              >
                {STATUS_OPTIONS.map((opt) => (
                  <option key={opt.value} value={opt.value}>
                    {opt.label}
                  </option>
                ))}
              </select>
            </label>

            {updatingIds.has(task.id) && (
              <span className="task-loading" aria-label="updating">
                Updating...
              </span>
            )}
          </div>

          {errorById[task.id] ? (
            <div className="error" data-testid="task-item-error">
              {errorById[task.id]}
            </div>
          ) : null}

          <div className="task-actions">
            {onSave && (
              <button
                type="button"
                data-testid="task-save-btn"
                disabled={isBusy(task.id)}
                onClick={() => handleSave(task)}
              >
                {savingIds.has(task.id) ? "Saving..." : "Save"}
              </button>
            )}

            <button
              type="button"
              data-testid="task-delete-btn"
              disabled={isBusy(task.id)}
              onClick={() => handleDelete(task.id)}
            >
              Delete
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}

export default TaskList;
export { TaskList };
