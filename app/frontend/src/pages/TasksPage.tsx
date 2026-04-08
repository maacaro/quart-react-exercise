/**
 * Tasks page component.
 *
 * Página principal de gestión de tareas.
 * Diseñada para que coincida con los tests E2E (data-testid, flujos, etc.).
 */

import React, { useEffect, useState } from "react";

import { Task, TaskStatus, CreateTaskRequest } from "../types/task";

import { getTasks, createTask, updateTask, deleteTask } from "../api/tasks";
import { TaskForm } from "../components/TaskForm";
import TaskList from "../components/TaskList"; // ✅ usamos el componente

const TasksPage: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [showForm, setShowForm] = useState(false);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  // Para manejar el diálogo de confirmación de borrado
  const [pendingDeleteId, setPendingDeleteId] = useState<number | null>(null);

  // Cargar tareas al montar
  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getTasks();
      setTasks(data);
    } catch (err) {
      console.error("Failed to load tasks:", err);
      setError(err instanceof Error ? err.message : "Failed to load tasks");
    } finally {
      setLoading(false);
    }
  };

  const showSuccess = (msg: string) => {
    setSuccessMessage(msg);
    setTimeout(() => setSuccessMessage(null), 3000);
  };

  const handleCreateTask = async (data: CreateTaskRequest): Promise<void> => {
    const newTask = await createTask(data);
    // Lo ponemos al principio de la lista
    setTasks((prev) => [newTask, ...prev]);
    setShowForm(false);
    showSuccess("Task created successfully!");
  };

  // Cambiar el estado en memoria cuando el usuario cambia el select
  // (Esto lo dejamos porque puede ayudar a que la UI responda inmediato)
  const handleStatusChange = (id: number, status: TaskStatus) => {
    setTasks((prev) =>
      prev.map((task) => (task.id === id ? { ...task, status } : task)),
    );
  };

  // Guardar cambios de una tarea (incluido el estado) en el backend
  // ✅ Se mantiene porque tus E2E ya usan task-save-btn
  const handleSaveTask = async (task: Task) => {
    const updated = await updateTask(task.id, {
      title: task.title,
      description: task.description,
      status: task.status,
    });

    setTasks((prev) => prev.map((t) => (t.id === task.id ? updated : t)));
    showSuccess("Task updated successfully!");
  };

  const handleDeleteTask = async (id: number) => {
    await deleteTask(id);
    setTasks((prev) => prev.filter((task) => task.id !== id));
    showSuccess("Task deleted successfully!");
  };

  // ✅ Esto es lo que TaskList va a usar para actualizar status en backend
  const handleUpdateFromList = async (id: number, data: Partial<Task>) => {
    // Si solo viene status, hacemos update del status.
    // Mantenemos también la actualización “optimista” en memoria.
    if (data.status) {
      handleStatusChange(id, data.status as TaskStatus);
    }

    // Nota: tu backend probablemente espera PUT /api/tasks/:id con status
    const current = tasks.find((t) => t.id === id);
    if (!current) return;

    const updated = await updateTask(id, {
      title: current.title,
      description: current.description,
      status: (data.status ?? current.status) as TaskStatus,
    });

    setTasks((prev) => prev.map((t) => (t.id === id ? updated : t)));
    showSuccess("Task updated successfully!");
  };

  return (
    <div className="tasks-page">
      {/* 👇 Tus tests hacen get_by_role("heading", name="Tasks") */}
      <h1>Tasks</h1>

      {successMessage && (
        <div data-testid="success-message" className="success">
          {successMessage}
        </div>
      )}

      {error && <div className="error">Error: {error}</div>}

      {/* Botón para abrir el formulario de nueva tarea */}
      <button
        type="button"
        data-testid="new-task-btn"
        onClick={() => setShowForm(true)}
      >
        New Task
      </button>

      {showForm && (
        <TaskForm onSubmit={handleCreateTask} onCancel={() => setShowForm(false)} />
      )}

      {loading ? (
        <div>Loading tasks...</div>
      ) : (
        <div data-testid="task-list">
          {/* ✅ Ahora TaskList renderiza la lista, pero NO rompemos el flujo de confirm */}
          <TaskList
            tasks={tasks}
            onUpdate={handleUpdateFromList}
            onDelete={async (id) => {
              // IMPORTANTE: aquí NO borramos directo
              // para que siga existiendo el confirm-delete-btn que esperan los tests.
              setPendingDeleteId(id);
            }}
            // ✅ extra prop para mantener Save
            onSave={handleSaveTask}
          />
        </div>
      )}

      {/* Diálogo de confirmación que usan tus tests con confirm-delete-btn */}
      {pendingDeleteId !== null && (
        <div className="delete-confirm">
          <p>Are you sure you want to delete this task?</p>
          <button
            type="button"
            data-testid="confirm-delete-btn"
            onClick={async () => {
              await handleDeleteTask(pendingDeleteId);
              setPendingDeleteId(null);
            }}
          >
            Confirm
          </button>
          <button type="button" onClick={() => setPendingDeleteId(null)}>
            Cancel
          </button>
        </div>
      )}
    </div>
  );
};

// Lo exportamos de las dos formas para ser compatibles
export default TasksPage;
export { TasksPage };
