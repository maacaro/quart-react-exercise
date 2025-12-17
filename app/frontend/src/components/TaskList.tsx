/**
 * TaskList Component
 * Displays a list of tasks with actions
 */
import { useMemo, useState } from "react";
import { Task, TaskStatus } from "../types/task";

interface TaskListProps {
  tasks: Task[];
  onUpdate: (id: number, data: Partial<Task>) => Promise<void>;
  onDelete: (id: number) => Promise<void>;
}

const STATUS_OPTIONS: { value: TaskStatus; label: string }[] = [
  { value: "pending", label: "Pending" },
  { value: "in_progress", label: "In Progress" },
  { value: "completed", label: "Completed" },
];

function TaskList({ tasks, onUpdate, onDelete }: TaskListProps) {
  const [updatingIds, setUpdatingIds] = useState<Set<number>>(new Set());
  const [deletingIds, setDeletingIds] = useState<Set<number>>(new Set());
  const [errorById, setErrorById] = useState<Record<number, string | null>>({});

  const isBusy = useMemo(() => {
    return (id: number) => updatingIds.has(id) || deletingIds.has(id);
  }, [updatingIds, deletingIds]);

  const handleStatusChange = async (task: Task, newStatus: TaskStatus) => {
    setErrorById((prev) => ({ ...prev, [task.id]: null }));
    setUpdatingIds((prev) => new Set(prev).add(task.id));

    try {
      // Solo actualizamos status (lo que pide el TODO del componente)
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

  if (tasks.length === 0) {
    return (
      <div className="task-list-empty" data-testid="task-list-empty">
        No tasks yet. Create one to get started!
      </div>
    );
  }

  return (
    <div className="task-list" data-testid="task-list">
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
            <button
              type="button"
              data-testid="task-delete-btn"
              disabled={isBusy(task.id)}
              onClick={() => handleDelete(task.id)}
            >
              {deletingIds.has(task.id) ? "Deleting..." : "Delete"}
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}

export default TaskList;
export { TaskList };
