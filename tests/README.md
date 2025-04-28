# Expense Tracker Django Tests

This directory contains tests for the Expense Tracker Django application, organized into the following categories:

## Test Structure

- **E2E Tests**: End-to-end tests that verify the behavior of the API endpoints
- **Integration Tests**: Tests that verify integration between components
- **Load Tests**: Performance tests using Locust

## Running Tests

You can use the provided `run_tests.sh` script to run tests:

```bash
# Run E2E tests
./run_tests.sh e2e

# Run integration tests
./run_tests.sh integration

# Run load tests (requires the server to be running at http://localhost:8000)
./run_tests.sh load

# Run all tests except load tests
./run_tests.sh all
```

## E2E Tests

The E2E tests verify that the API endpoints function correctly:

- **User Operations**: Creating and deleting users
- **Expense Operations**: CRUD operations for expenses
- **Authentication**: Verifying JWT authentication

## Integration Tests

These tests verify the interaction between components:

- **Auth Service**: Tests JWT token generation and validation

## Load Tests

The load tests simulate user behavior to measure application performance:

1. The test simulates multiple users
2. Each user creates their own account
3. Users perform CRUD operations on expenses
4. The tests measure response times and throughput

To run load tests:

1. Start the Django server: `python manage.py runserver`
2. Run the load test: `./run_tests.sh load`

For more detailed reports, run Locust with the UI:

```bash
cd tests/load
locust -f locustfile.py --host http://localhost:8000
```

Then open your browser at http://localhost:8089 to view the Locust interface. 