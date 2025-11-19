/**
 * TaskForm Component
 * Form for creating new tasks
 */
import { useState, FormEvent } from 'react';
import { CreateTaskData } from '../types/task';

interface TaskFormProps {
  onSubmit: (data: CreateTaskData) => Promise<void>;
}

function TaskForm({ onSubmit }: TaskFormProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [status, setStatus] = useState<'pending' | 'in_progress' | 'completed'>('pending');
  const [isSubmitting, setIsSubmitting] = useState(false);

  /**
   * Handle form submission
   *
   * TODO: Implement this function
   * Hints:
   * - Prevent default form submission
   * - Validate that title and description are not empty
   * - Set isSubmitting to true before calling onSubmit
   * - Call onSubmit with the form data
   * - Clear the form fields after successful submission
   * - Set isSubmitting to false when done
   * - Handle errors appropriately
   */
  const handleSubmit = async (e: FormEvent) => {
    // TODO: Implement
  };

  return (
    <form className="task-form" onSubmit={handleSubmit}>
      <h3>Create New Task</h3>

      <div className="form-group">
        <label htmlFor="title">Title:</label>
        <input
          id="title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Enter task title"
          disabled={isSubmitting}
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="description">Description:</label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Enter task description"
          disabled={isSubmitting}
          required
          rows={3}
        />
      </div>

      <div className="form-group">
        <label htmlFor="status">Status:</label>
        <select
          id="status"
          value={status}
          onChange={(e) => setStatus(e.target.value as 'pending' | 'in_progress' | 'completed')}
          disabled={isSubmitting}
        >
          <option value="pending">Pending</option>
          <option value="in_progress">In Progress</option>
          <option value="completed">Completed</option>
        </select>
      </div>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Creating...' : 'Create Task'}
      </button>
    </form>
  );
}

export default TaskForm;
