#!/bin/bash

# Function to display help message
show_help() {
    echo "Usage: ./run_tests.sh [OPTION]"
    echo "Run different test suites for the Django expense tracker app."
    echo ""
    echo "Options:"
    echo "  e2e            Run end-to-end tests"
    echo "  integration    Run integration tests"
    echo "  load           Run load tests"
    echo "  all            Run all tests (except load tests)"
    echo "  help           Display this help and exit"
    echo ""
}

# Handle arguments
case "$1" in
    e2e)
        echo "Running E2E tests..."
        python -m pytest tests/E2E -v
        ;;
    integration)
        echo "Running integration tests..."
        python -m pytest tests/integration -v
        ;;
    load)
        echo "Running load tests..."
        cd tests/load
        locust -f locustfile.py --headless -u 10 -r 1 --run-time 30s --host http://localhost:8000
        ;;
    all)
        echo "Running all tests (except load tests)..."
        python -m pytest tests/E2E tests/integration -v
        ;;
    help|*)
        show_help
        ;;
esac
