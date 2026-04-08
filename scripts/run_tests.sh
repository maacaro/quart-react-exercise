#!/bin/bash

# Test runner script with coverage
# Usage: ./scripts/run_tests.sh [unit|e2e|all]

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_color() {
    color=$1
    message=$2
    echo -e "${color}${message}${NC}"
}

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    print_color "$YELLOW" "🔧 Activating virtual environment..."
    source venv/bin/activate
fi

# Determine test type
TEST_TYPE=${1:-"all"}

case "$TEST_TYPE" in
    "unit")
        print_color "$GREEN" "🧪 Running unit tests..."
        pytest tests/unit/ -m unit -v --cov=app/backend --cov-report=html --cov-report=term
        print_color "$GREEN" "✅ Unit tests complete!"
        ;;

    "e2e")
        print_color "$GREEN" "🌐 Running E2E tests..."

        # Check if backend is running
        if ! curl -s http://localhost:5000/api/health > /dev/null 2>&1; then
            print_color "$RED" "❌ Backend is not running!"
            print_color "$YELLOW" "Please start backend first:"
            print_color "$YELLOW" "  cd app/backend && hypercorn main:app --bind 0.0.0.0:5000"
            exit 1
        fi

        pytest tests/e2e/ -m e2e -v
        print_color "$GREEN" "✅ E2E tests complete!"
        ;;

    "all")
        print_color "$GREEN" "🧪 Running all tests..."

        # Run unit tests with coverage
        print_color "$YELLOW" "\n📊 Phase 1: Unit Tests"
        pytest tests/unit/ -m unit -v --cov=app/backend --cov-report=html --cov-report=term

        # Run E2E tests if backend is running
        print_color "$YELLOW" "\n🌐 Phase 2: E2E Tests"
        if curl -s http://localhost:5000/api/health > /dev/null 2>&1; then
            pytest tests/e2e/ -m e2e -v
        else
            print_color "$YELLOW" "⚠️  Skipping E2E tests (backend not running)"
        fi

        print_color "$GREEN" "\n✅ All tests complete!"
        print_color "$YELLOW" "\n📊 Coverage report generated: htmlcov/index.html"
        ;;

    *)
        print_color "$RED" "❌ Invalid test type: $TEST_TYPE"
        echo "Usage: $0 [unit|e2e|all]"
        exit 1
        ;;
esac

print_color "$GREEN" "\n🎉 Test run finished successfully!"
