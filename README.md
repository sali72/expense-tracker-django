# Expense Tracker Django API

A Django implementation of an expense tracking application with RESTful API endpoints.

## Features

- User management (create, delete)
- Expense tracking (create, read, update, delete)
- JWT authentication
- Tag-based expense categorization

## Setup and Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
4. Run the development server:
   ```
   python manage.py runserver
   ```

## API Endpoints

### Users
- POST `/api/users/` - Create a new user
- DELETE `/api/users/` - Delete a user
- GET `/api/users/test-auth/` - Test authentication

### Expenses
- GET `/api/expenses/` - Get all expenses for authenticated user
- POST `/api/expenses/` - Create a new expense
- GET `/api/expenses/{id}/` - Get a specific expense
- PATCH `/api/expenses/{id}/` - Update a specific expense
- DELETE `/api/expenses/{id}/` - Delete a specific expense 