# Tech Mart - Simple Customers and Orders Service

This project is a simple Django REST framework service for managing customers and orders. It provides REST API endpoints for creating and managing customers and orders, implements authentication and authorization using OpenID Connect, sends SMS alerts using Africa's Talking SMS gateway, and includes automated CI/CD setup with unit tests and code coverage.

## Features

1. **Customers and Orders API:**
   - Create and manage customers/users with simple details such as name and code.
   - Create and manage orders with details such as item, amount, and timestamp.
   
2. **Authentication and Authorization:**
   - OpenID Connect integration for secure login and access control.
   
3. **SMS Alerts:**
   - Sends SMS notifications to customers when an order is created using Africa’s Talking SMS gateway.

4. **CI/CD Pipeline:**
   - Continuous Integration and Continuous Deployment with automated testing and coverage checking.

## Requirements

Before running this project, ensure you have the following installed:

- Python 3.x
- Django 5.x+
- Django Rest Framework
- Africa's Talking API (sandbox setup)
- PostgreSQL or SQLite (for local development)

## Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/tech_mart.git
   cd server
   ````
2. **Create and Activate a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```
4. **Set up .env**

   ```bash
    # Django configuration
    SECRET_KEY = your secret_key
    DEBUG = True #for developemt

    # Database configuration
    DATABASE_URL = your cloud database external url or default db.sqlite3

    # Google OAuth configuration
    GOOGLE_CLIENT_ID = your google client id
    GOOGLE_CLIENT_SECRET = your google client secret
    GOOGLE_REDIRECT_URI = redirect url

    # Africas Talking
    AFRICAS_TALKING_API_KEY = your africas talking api key
    AFRICAS_TALKING_USERNAME = your africas talking username

   ```

5. **Apply Migrations**

   ```bash
   python manage.py migrate
   ```

6. **Create a Superuser**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server**

   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Users/Customers

- **Create/Signin Users with google signin**

  ```
  /api/google/login/
  ```

- **Create Users with email and password**

  ```
  /api/users/register/
  ```

- **List Users**

  ```
  /api/users/
  ```

- **Retrieve Update Destroy users**

  ```
  /api/users/{id}/
  ```

### Orders

- **List Create Orders**

  ```
  /api/orders/
  ```

- **Retrieve, Update, Delete Transaction**

  ```
  /api/orders/{id}/
  ```

## Unit Tests

Tests are located in the `api/tests` directory. To run the tests:

```bash
coverage run --source='.' manage.py test
coverage report
```

## GitHub Actions

A GitHub Action is set up to automatically run unit tests on every push and pull request. You can find the configuration in `.github/workflows/ci-cd.yaml`.

## Contributing

1. **Fork the Repository**
2. **Create a Feature Branch**

   ```bash
   git checkout -b feature/your-feature
   ```

3. **Commit Your Changes**

   ```bash
   git commit -m "Add new feature"
   ```

4. **Push to the Branch**

   ```bash
   git push origin feature/your-feature
   ```

5. **Create a Pull Request**

   Go to the repository on GitHub and create a pull request.

---