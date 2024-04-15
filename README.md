# Student Assignment System

This project is a student assignment system built on SQL database containing user table and assignment table, featuring super user (teacher) privileges, and a Flask backend with JWT authentication. Additionally, a Postman JSON response file is attached for testing purposes.

Students can view the assignments allotted to them by registering and login. Teacher can create, delete and modify the assignment for each student. This can be further 
expanded by adding a feature to display individual grades with minor modifications.

## Features

- **User Management**: Allows creation, deletion, and modification of users, distinguishing between regular users and super users (teachers).
- **Assignment Management**: Facilitates the creation, deletion, and updating of assignments by super users.
- **JWT Authentication**: Secures the system with JWT authentication to ensure authorized access.
- **Postman JSON Response**: Provides a file for testing the API endpoints using Postman for seamless integration and validation.

## Components

- **SQL Database**: Stores user information and assignment details.
- **Flask Backend**: Powers the backend logic of the system, handling requests, authentication, and database operations.
- **JWT Authentication**: Ensures secure access to the system by generating and verifying JWT tokens.
- **Postman JSON Response**: Facilitates testing of the API endpoints with sample requests and responses.

## API Endpoints
[Postman Documentation](https://documenter.getpostman.com/view/33092409/2sA2r9WiY2#8a7edc2b-3c17-4840-9e96-ddbca7322bdf)
### User Management

- **POST /register**
  - Description: Register a new user.
  - Request Body: JSON object containing user information (e.g., username, password).
  - Example: `http://127.0.0.1:5000/register`

- **POST /login**
  - Description: Authenticate user login.
  - Request Body: JSON object containing user credentials (e.g., username, password).
  - Example: `http://127.0.0.1:5000/login`

### Teacher Operations

- **POST /teacher/login**
  - Description: Authenticate teacher login.
  - Request Body: JSON object containing teacher credentials (e.g., username, password).
  - Example: `http://127.0.0.1:5000/teacher/login`

- **POST /assignment/create**
  - Description: Create a new assignment (accessible to teachers).
  - Request Body: JSON object containing assignment details (e.g., title, description).
  - Example: `http://127.0.0.1:5000/assignment/create`

- **DELETE /assignment/delete**
  - Description: Delete an assignment (accessible to teachers).
  - Request Body: JSON object containing assignment ID.
  - Example: `http://127.0.0.1:5000/assignment/delete`

### User Operations

- **POST /user/login**
  - Description: Authenticate user login.
  - Request Body: JSON object containing user credentials (e.g., username, password).
  - Example: `http://127.0.0.1:5000/user/login`

- **GET /user/assignments**
  - Description: View assignments for a user.
  - Example: `http://127.0.0.1:5000/user/assignments`

### Error Handling

- **GET /wrong/login**
  - Description: Simulated wrong login attempt (for testing error handling).
  - Example: `http://127.0.0.1:5000/wrong/login`

- **GET /wrong/access**
  - Description: Simulated wrong access attempt (for testing error handling).
  - Example: `http://127.0.0.1:5000/wrong/access`

## Usage

1. **Setup SQL Database**: Set up the SQL database with the provided schema for user and assignment tables.
2. **Install Dependencies**: Install the required dependencies for the Flask backend.
3. **Run Flask Application**: Start the Flask application to initialize the backend server.
4. **Authenticate**: Authenticate using JWT tokens to access privileged endpoints.
5. **Manage Users**: Perform user management operations such as creating, deleting, and updating users.
6. **Manage Assignments**: Utilize the assignment management endpoints to handle assignment-related tasks.
7. **Test Endpoints**: Use the provided Postman JSON file to test the API endpoints and validate responses.

## Postman JSON Response

The attached Postman JSON file contains sample requests and responses for testing the API endpoints. Import this file into Postman to streamline the testing process and ensure seamless integration with the system.

## License

This project is licensed under the [License Name] License - see the [LICENSE.md](LICENSE.md) file for details.
