# Solution Hints

Stuck on the assignment? Here are progressive hints to help you without giving away the full solution.

## General Approach

1. **Always write tests first** (TDD)
2. **Run tests and watch them fail** (Red)
3. **Write minimum code to pass** (Green)
4. **Refactor for quality** (Refactor)
5. **Commit often** (after each cycle)

---

## Phase 1: Backend Hints

### Task 1.1: Writing Tests

**Hint 1**: Study existing test patterns
```python
# Look at tests in the main project
# Pattern: tests/unit/test_reviews.py

# Key elements:
# - @pytest.mark.asyncio decorator
# - test_client fixture usage
# - await test_client.post("/api/endpoint", json=data)
# - assert response.status_code == expected_code
# - data = await response.get_json()
```

**Hint 2**: Test structure
```python
@pytest.mark.asyncio
async def test_create_task_success(test_client):
    """Test description."""
    # Arrange - prepare test data
    task_data = {...}

    # Act - call the endpoint
    response = await test_client.post("/api/tasks", json=task_data)

    # Assert - verify results
    assert response.status_code == 201
    data = await response.get_json()
    assert "id" in data
    assert data["title"] == task_data["title"]
```

**Hint 3**: Common assertions for tests
```python
# Success case
assert response.status_code == 201
assert data["id"] is not None
assert data["title"] == "expected title"

# Error case
assert response.status_code == 400
assert "error" in data
assert "title" in data["error"].lower()

# Not found case
assert response.status_code == 404
```

### Task 1.2: Implementing Endpoints

**Hint 1**: Blueprint structure
```python
# In app/backend/tasks/routes.py
from quart import Blueprint, request, jsonify

tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.route("/api/tasks", methods=["POST"])
async def create_task_endpoint():
    # 1. Get request data
    data = await request.get_json()

    # 2. Validate data
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    # 3. Process and save
    # ...

    # 4. Return result
    return jsonify(result), 201
```

**Hint 2**: Validation pattern
```python
# Check required fields
if not data:
    return jsonify({"error": "Request body is required"}), 400

if "title" not in data or not data["title"].strip():
    return jsonify({"error": "Title is required", "field": "title"}), 400

# Validate status
VALID_STATUSES = ["pending", "in_progress", "completed"]
status = data.get("status", "pending")

if status not in VALID_STATUSES:
    return jsonify({
        "error": f"Invalid status. Must be one of: {', '.join(VALID_STATUSES)}",
        "field": "status"
    }), 400
```

**Hint 3**: Database operations
```python
# In app/backend/core/database.py

async def insert_task(title, description, status):
    """Insert task and return created task."""
    async with await get_connection() as db:
        cursor = await db.execute(
            "INSERT INTO tasks (title, description, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
            (title, description, status, now, now)
        )
        await db.commit()

        task_id = cursor.lastrowid

        # Fetch and return created task
        cursor = await db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = await cursor.fetchone()

        return {
            "id": row[0],
            "title": row[1],
            # ... other fields
        }
```

**Hint 4**: Full endpoint example structure
```python
@tasks_bp.route("/api/tasks", methods=["GET"])
async def get_tasks():
    """Get all tasks."""
    try:
        tasks = await fetch_all_tasks()  # Database function
        return jsonify(tasks), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@tasks_bp.route("/api/tasks/<int:task_id>", methods=["GET"])
async def get_task(task_id):
    """Get single task by ID."""
    try:
        task = await fetch_task_by_id(task_id)
        if not task:
            return jsonify({"error": "Task not found"}), 404
        return jsonify(task), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
```

---

## Phase 2: Frontend Hints

### Task 2.1: Writing Playwright Tests

**Hint 1**: Playwright selector patterns
```python
# Use data-testid attributes (recommended)
page.click('[data-testid="new-task-btn"]')

# Wait for element to be ready
page.wait_for_selector('[data-testid="task-form"]')

# Use expect for assertions (auto-waits)
expect(page.locator('[data-testid="success-message"]')).to_be_visible()
```

**Hint 2**: Test flow structure
```python
@pytest.mark.e2e
def test_create_task_flow(page: Page):
    """Test complete task creation."""
    # 1. Navigate
    page.goto("http://localhost:5173/tasks")

    # 2. Interact
    page.click('[data-testid="new-task-btn"]')
    page.fill('[data-testid="title-input"]', "Test Task")
    page.click('[data-testid="submit-btn"]')

    # 3. Verify
    expect(page.locator('[data-testid="success"]')).to_be_visible()
    expect(page.locator('text=Test Task')).to_be_visible()
```

**Hint 3**: Common Playwright patterns
```python
# Fill input
page.fill('input[name="title"]', "value")

# Select option
page.select_option('select[name="status"]', "pending")

# Click button
page.click('button[type="submit"]')

# Wait for navigation
page.wait_for_url("**/tasks")

# Check visibility
expect(page.locator('[data-testid="element"]')).to_be_visible()
expect(page.locator('[data-testid="element"]')).not_to_be_visible()

# Check text content
expect(page.locator('h1')).to_contain_text("Tasks")

# Check count
expect(page.locator('[data-testid="task-card"]')).to_have_count(3)
```

### Task 2.2: Implementing React Components

**Hint 1**: API client pattern
```typescript
// app/frontend/src/api/tasks.ts

export const getTasks = async (): Promise<Task[]> => {
  const response = await fetch('/api/tasks');

  if (!response.ok) {
    throw new Error('Failed to fetch tasks');
  }

  return response.json();
};

export const createTask = async (data: CreateTaskRequest): Promise<Task> => {
  const response = await fetch('/api/tasks', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Failed to create task');
  }

  return response.json();
};
```

**Hint 2**: React component with state
```tsx
export const TasksPage: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    try {
      setLoading(true);
      const data = await getTasks();
      setTasks(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load tasks');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      {loading && <div>Loading...</div>}
      {error && <div>Error: {error}</div>}
      {/* Render tasks */}
    </div>
  );
};
```

**Hint 3**: Form handling pattern
```tsx
export const TaskForm: React.FC<TaskFormProps> = ({ onSubmit, onCancel }) => {
  const [title, setTitle] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    // Validation
    if (!title.trim()) {
      setError('Title is required');
      return;
    }

    try {
      setLoading(true);
      await onSubmit({ title });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to save');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {error && <div data-testid="error-message">{error}</div>}

      <input
        data-testid="title-input"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        disabled={loading}
      />

      <button data-testid="submit-btn" type="submit" disabled={loading}>
        {loading ? 'Saving...' : 'Save'}
      </button>
    </form>
  );
};
```

**Hint 4**: Don't forget data-testid attributes!
```tsx
// Every element that E2E tests interact with needs data-testid

<button data-testid="new-task-btn">New Task</button>
<input data-testid="task-title-input" />
<div data-testid="task-list">...</div>
<div data-testid="task-card">...</div>
<div data-testid="success-message">...</div>
<div data-testid="error-message">...</div>
```

---

## Common Pitfalls

### Pitfall 1: Forgetting async/await

```python
# ❌ Wrong
def test_something(test_client):
    response = test_client.post("/api/tasks", json=data)

# ✅ Correct
@pytest.mark.asyncio
async def test_something(test_client):
    response = await test_client.post("/api/tasks", json=data)
```

### Pitfall 2: Not cleaning database between tests

```python
# Add to conftest.py
@pytest.fixture(autouse=True)
async def cleanup():
    """Clean database before each test."""
    await clear_db()
    await init_db()
    yield
```

### Pitfall 3: Race conditions in E2E tests

```python
# ❌ Wrong - Element might not be ready
page.click('[data-testid="button"]')

# ✅ Correct - Wait for element
expect(page.locator('[data-testid="button"]')).to_be_visible()
page.click('[data-testid="button"]')
```

### Pitfall 4: Not handling errors in React

```typescript
// ❌ Wrong - Errors crash the app
const data = await createTask(taskData);

// ✅ Correct - Handle errors gracefully
try {
  const data = await createTask(taskData);
  setSuccess(true);
} catch (error) {
  setError(error.message);
}
```

---

## Still Stuck?

### Debugging Checklist

- [ ] Did you activate the virtual environment?
- [ ] Did you install all dependencies?
- [ ] Is the database initialized?
- [ ] Are you using the correct async/await syntax?
- [ ] Did you register the blueprint in app.py?
- [ ] Are data-testid attributes present in components?
- [ ] Is the backend running for E2E tests?
- [ ] Did you check the error message carefully?

### Get More Help

1. **Review main project code** - Look at how similar features are implemented
2. **Read the error message** - It usually tells you what's wrong
3. **Check the tests** - Tests show how code should work
4. **Use debugger** - Add `breakpoint()` in Python or `console.log()` in TypeScript
5. **Ask for help** - Provide specific error messages and what you've tried

---

## Next Level Challenges

After completing the basic assignment, try these:

1. **Add filtering** - Filter tasks by status
2. **Add sorting** - Sort tasks by date or title
3. **Add pagination** - Show 10 tasks per page
4. **Add search** - Search tasks by title
5. **Add user authentication** - Follow patterns from main project
6. **Add task categories** - Group tasks into categories
7. **Add due dates** - Add and sort by due date
8. **Add task priority** - High, medium, low priority

Good luck! 🚀
