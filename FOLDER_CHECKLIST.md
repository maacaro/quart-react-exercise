# Practice Exercise Folder Checklist

Use this checklist to set up the complete practice exercise structure.

## Documentation Files

- [x] README.md - Main setup guide
- [x] ASSIGNMENT.md - Student assignment instructions
- [x] TESTING.md - Testing patterns and guide
- [x] SOLUTION_HINTS.md - Progressive hints for students
- [x] FOLDER_CHECKLIST.md - This file

## Configuration Files

- [x] .env.example - Example environment variables
- [x] pytest.ini - pytest configuration
- [x] pyproject.toml - Python project configuration
- [ ] .gitignore - Git ignore patterns

## Scripts

- [x] scripts/init_db.py - Database initialization
- [x] scripts/run_tests.sh - Test runner script

## Backend Structure (To Be Created)

```
app/backend/
├── __init__.py
├── app.py                 # Main application factory
├── config.py              # Configuration constants
├── main.py                # Entry point
├── error.py               # Error handling
├── decorators.py          # Route decorators
│
├── core/
│   ├── __init__.py
│   └── database.py        # Database operations
│
├── tasks/
│   ├── __init__.py
│   ├── routes.py          # Task endpoints (STUDENT IMPLEMENTS)
│   └── models.py          # Task models (STUDENT IMPLEMENTS)
│
├── static/                # Compiled React app (generated)
│
└── requirements.txt       # Python dependencies
```

## Frontend Structure (To Be Created)

```
app/frontend/
├── src/
│   ├── main.tsx           # Entry point
│   ├── App.tsx            # Root component
│   │
│   ├── pages/
│   │   └── Tasks.tsx      # Tasks page (STUDENT IMPLEMENTS)
│   │
│   ├── components/
│   │   ├── TaskForm.tsx   # Task form (STUDENT IMPLEMENTS)
│   │   └── TaskList.tsx   # Task list (STUDENT IMPLEMENTS)
│   │
│   ├── api/
│   │   └── tasks.ts       # API client (STUDENT IMPLEMENTS)
│   │
│   └── types/
│       └── task.ts        # TypeScript types
│
├── package.json           # Node dependencies
├── vite.config.ts         # Vite configuration
├── tsconfig.json          # TypeScript config
├── index.html             # HTML template
└── .eslintrc.js           # ESLint config
```

## Test Structure (To Be Created)

```
tests/
├── unit/
│   ├── conftest.py        # Test fixtures
│   └── test_tasks.py      # Task tests (STUDENT IMPLEMENTS)
│
└── e2e/
    ├── conftest.py        # Playwright fixtures
    └── test_tasks.py      # UI tests (STUDENT IMPLEMENTS)
```

## Required Files to Create

### Minimal Backend

- [ ] `app/backend/__init__.py`
- [ ] `app/backend/app.py` - Application factory with blueprint registration
- [ ] `app/backend/config.py` - Configuration constants
- [ ] `app/backend/main.py` - Entry point to run the app
- [ ] `app/backend/error.py` - Error handling utilities
- [ ] `app/backend/core/__init__.py`
- [ ] `app/backend/core/database.py` - Database helpers
- [ ] `app/backend/tasks/__init__.py`
- [ ] `app/backend/tasks/routes.py` - Starter with TODOs
- [ ] `app/backend/tasks/models.py` - Starter with TODOs
- [ ] `app/backend/requirements.txt` - Python dependencies

### Minimal Frontend

- [ ] `app/frontend/package.json` - Node dependencies
- [ ] `app/frontend/vite.config.ts` - Vite config with proxy
- [ ] `app/frontend/tsconfig.json` - TypeScript config
- [ ] `app/frontend/index.html` - HTML template
- [ ] `app/frontend/src/main.tsx` - Entry point
- [ ] `app/frontend/src/App.tsx` - Root component
- [ ] `app/frontend/src/types/task.ts` - Type definitions
- [ ] `app/frontend/src/api/tasks.ts` - Starter with TODOs
- [ ] `app/frontend/src/pages/Tasks.tsx` - Starter with TODOs
- [ ] `app/frontend/src/components/TaskForm.tsx` - Starter with TODOs

### Test Files

- [ ] `tests/__init__.py`
- [ ] `tests/unit/__init__.py`
- [ ] `tests/unit/conftest.py` - Test fixtures
- [ ] `tests/unit/test_tasks.py` - Starter with TODOs
- [ ] `tests/e2e/__init__.py`
- [ ] `tests/e2e/conftest.py` - Playwright fixtures
- [ ] `tests/e2e/test_tasks.py` - Starter with TODOs

### Additional Configuration

- [ ] `.gitignore` - Git ignore patterns
- [ ] `README.md` - Link to documentation files

## Setup Instructions for Instructor

### 1. Create Directory Structure

```bash
cd docs/practice-exercise

# Backend
mkdir -p app/backend/core app/backend/tasks app/backend/static
touch app/backend/__init__.py
touch app/backend/core/__init__.py
touch app/backend/tasks/__init__.py

# Frontend
mkdir -p app/frontend/src/{pages,components,api,types}

# Tests
mkdir -p tests/unit tests/e2e
touch tests/__init__.py
touch tests/unit/__init__.py
touch tests/e2e/__init__.py
```

### 2. Create Starter Files

Use the documentation and hints to create starter files with:
- Basic structure in place
- TODO comments where students should implement
- Examples/patterns they can follow
- Reference to main project patterns

### 3. Create Solution Branch

```bash
# Create solution branch with complete implementation
git checkout -b solution/task-management

# Implement complete solution
# ... (implement all features)

# Commit complete solution
git add .
git commit -m "solution: complete task management implementation"

git push origin solution/task-management
```

### 4. Test the Exercise

1. Start from starter branch
2. Follow ASSIGNMENT.md step by step
3. Ensure all instructions are clear
4. Verify tests work as expected
5. Time how long it takes to complete

### 5. Create Answer Key

Document:
- Expected completion time
- Common mistakes students make
- Grading rubric
- Sample solutions for different approaches

## Student Setup Checklist

Students should be able to:

- [ ] Clone repository
- [ ] Checkout practice exercise branch
- [ ] Follow README.md to set up environment
- [ ] Run existing tests (should pass)
- [ ] Follow ASSIGNMENT.md to implement features
- [ ] Run their tests and see them pass
- [ ] Submit completed work

## Quality Checklist

- [ ] All documentation files are clear and complete
- [ ] Code examples are tested and working
- [ ] Starter files have helpful TODOs and hints
- [ ] Test patterns match main project
- [ ] Git workflow is documented
- [ ] Common issues are documented
- [ ] Solution branch is complete and tested

---

## Next Steps

1. **Create starter files** listed above
2. **Test the exercise** end-to-end
3. **Refine documentation** based on test run
4. **Create solution branch** with complete implementation
5. **Get feedback** from a test student
6. **Iterate** based on feedback

Good luck setting up the practice exercise! 🚀
