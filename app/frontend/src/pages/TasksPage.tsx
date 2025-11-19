/**
 * TasksPage Component
 * Main page for managing tasks
 */
import { useState, useEffect } from 'react';
import { Task, CreateTaskData } from '../types/task';
import { fetchTasks, createTask, updateTask, deleteTask } from '../api/tasks';
import TaskList from '../components/TaskList';
import TaskForm from '../components/TaskForm';

function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  /**
   * Load tasks when component mounts
   *
   * TODO: Implement this effect
   * Hints:
   * - Call fetchTasks() from the API
   * - Update tasks state with the result
   * - Handle loading and error states
   * - Use try/catch for error handling
   */
  useEffect(() => {
    // TODO: Implement
  }, []);

  /**
   * Handle creating a new task
   *
   * TODO: Implement this function
   * Hints:
   * - Call createTask() API function
   * - Add the new task to the tasks state
   * - Handle errors appropriately
   */
  const handleCreateTask = async (data: CreateTaskData) => {
    // TODO: Implement
  };

  /**
   * Handle updating a task
   *
   * TODO: Implement this function
   * Hints:
   * - Call updateTask() API function
   * - Update the task in the tasks state
   * - Handle errors appropriately
   */
  const handleUpdateTask = async (id: number, data: Partial<Task>) => {
    // TODO: Implement
  };

  /**
   * Handle deleting a task
   *
   * TODO: Implement this function
   * Hints:
   * - Call deleteTask() API function
   * - Remove the task from the tasks state
   * - Handle errors appropriately
   */
  const handleDeleteTask = async (id: number) => {
    // TODO: Implement
  };

  if (loading) {
    return <div>Loading tasks...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div className="tasks-page">
      <h2>Tasks</h2>

      <TaskForm onSubmit={handleCreateTask} />

      <TaskList
        tasks={tasks}
        onUpdate={handleUpdateTask}
        onDelete={handleDeleteTask}
      />
    </div>
  );
}

export default TasksPage;
