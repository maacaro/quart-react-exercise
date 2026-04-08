/**
 * Task creation/edit form component.
 *
 * Following component patterns from app/frontend/src/components/ in main project.
 */
import React, { useState } from "react";
import { CreateTaskRequest, TaskStatus } from "../types/task";

interface TaskFormProps {
  onSubmit: (data: CreateTaskRequest) => Promise<void>;
  onCancel: () => void;
  initialData?: CreateTaskRequest;
}

const TaskForm: React.FC<TaskFormProps> = ({
  onSubmit,
  onCancel,
  initialData,
}) => {
  const [title, setTitle] = useState(initialData?.title ?? "");
  const [description, setDescription] = useState(initialData?.description ?? "");
  const [status, setStatus] = useState<TaskStatus>(
    initialData?.status ?? "pending",
  );
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    // ✅ Validación que esperan tus tests E2E
    if (!title.trim()) {
      setError("Title is required");
      return;
    }

    try {
      setLoading(true);
      await onSubmit({
        title: title.trim(),
        description: description.trim(),
        status,
      });
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to save task",
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="task-form"
      data-testid="task-form"
    >
      {error && (
        <div data-testid="error-message" className="error">
          {error}
        </div>
      )}

      <div className="form-group">
        <label htmlFor="title">Title *</label>
        <input
          id="title"
          data-testid="task-title-input"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Enter task title"
          disabled={loading}
        />
      </div>

      <div className="form-group">
        <label htmlFor="description">Description</label>
        <textarea
          id="description"
          data-testid="task-description-input"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Enter task description"
          disabled={loading}
          rows={3}
        />
      </div>

      <div className="form-group">
        <label htmlFor="status">Status</label>
        <select
          id="status"
          data-testid="task-status-select"
          value={status}
          onChange={(e) =>
            setStatus(e.target.value as TaskStatus)
          }
          disabled={loading}
        >
          <option value="pending">Pending</option>
          <option value="in_progress">In Progress</option>
          <option value="completed">Completed</option>
        </select>
      </div>

      <div className="form-actions">
        <button
          type="submit"
          data-testid="create-task-btn"
          disabled={loading}
        >
          {loading ? "Saving..." : "Create Task"}
        </button>
        <button type="button" onClick={onCancel} disabled={loading}>
          Cancel
        </button>
      </div>
    </form>
  );
};

// 👇 Exportamos de las dos formas por si acaso
export default TaskForm;
export { TaskForm };
