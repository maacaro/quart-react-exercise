import { Routes, Route } from 'react-router-dom'
import TasksPage from './pages/TasksPage'

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>Task Manager</h1>
      </header>
      <main className="app-main">
        <Routes>
          <Route path="/" element={<TasksPage />} />
          <Route path="/tasks" element={<TasksPage />} />
        </Routes>
      </main>
    </div>
  )
}

export default App
