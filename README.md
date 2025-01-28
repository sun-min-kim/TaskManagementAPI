# Task Management API

This is a Task Management API built with Flask, allowing users to create, read, update, and delete tasks while using authentication. 

## Table of Contents
- [Prerequisites](#prerequisites)
- [Setup and Run](#setup-and-run)
- [Testing the API Locally](#testing-the-api-locally)
- [Accessing the MySQL Database Manually (Local Only)](#accessing-the-mysql-database-manually-local-only)
- [Testing the API on External IP](#testing-the-api-on-external-ip)

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- [Docker](https://www.docker.com/get-started) 
- [Docker Compose](https://docs.docker.com/compose/install)

## Setup and Run

Follow these steps to set up and run the API locally using Docker Compose:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/sun-min-kim/TaskManagementAPI.git
   cd task-management-api
   ```

2. **Create a `.env` file** in the root of the project and define the necessary environment variables:

    ```dotenv
    SECRET_KEY=your_secret_key

    MYSQL_ROOT_PASSWORD=your_root_password
    MYSQL_DATABASE=your_db_name
    MYSQL_USER=your_user
    MYSQL_PASSWORD=your_password

    SQLALCHEMY_DATABASE_URI=mysql+pymysql://your_user:your_password@mysql:3306/your_db_name
    FLASK_ENV=development
    ```

    Replace `your_secret_key`, `your_root_password`, `your_db_name`, `your_user` and `your_password`along with their values in `SQLALCHEMY_DATABASE_URI`.

    For example, a sample `SQLALCHEMY_DATABASE_URI` may look like `mysql+pymysql://user:password@mysql:3306/tasks_db`

3. **Build and run the application**:

    ```bash
    docker-compose up --build
    ```
    This command will build the Docker images and start the containers.

4. The API will be accessible at `http://localhost:5000`.

## Testing the API Locally

You can test the API endpoints using cURL at `http://localhost:5000`.

1. **Register a new user**:

    ```bash
    curl -X POST http://localhost:5000/register \
    -H "Content-Type: application/json" \
    -d '{"username": "testuser", "password": "testpassword"}'
    ```

2. **Login the user** (save cookies):

    ```bash
    curl -X POST http://localhost:5000/login \
    -H "Content-Type: application/json" \
    -d '{"username": "testuser", "password": "testpassword"}' \
    -c cookie.txt
    ```

3. **Create a new task**:

    ```bash
    curl -X POST http://localhost:5000/tasks \
    -H "Content-Type: application/json" \
    -b cookie.txt \
    -d '{"title": "New Task", "description": "Description of the task", "dueDate": "2025-01-26T12:00:00", "status": "pending"}'
    ```

4. **Get all tasks**:

    ```bash
    curl -X GET http://localhost:5000/tasks \
    -b cookie.txt
    ```

5. **Get a task by ID**:

    ```bash
    curl -X GET http://localhost:5000/tasks/{id} \
    -b cookie.txt
    ```

6. **Update a task**:

    ```bash
    curl -X PUT http://localhost:5000/tasks/{id} \
    -H "Content-Type: application/json" \
    -b cookie.txt \
    -d '{"title": "Updated Task", "description": "Updated description", "dueDate": "2025-01-30T12:00:00", "status": "in-progress"}'
    ```

7. **Delete a task**:

    ```bash
    curl -X DELETE http://localhost:5000/tasks/{id} \
    -b cookie.txt
    ```

8. **Logout**:

    ```bash
    curl -X POST http://localhost:5000/logout \
    -b cookie.txt
    ```

## Accessing the MySQL Database Manually

When you run the API locally using Docker Compose, the MySQL database running in your Docker container can be accessed with these following steps:

1. **Ensure Docker is Running**: Make sure your Docker service is running.

2. **Navigate to Your Project Directory**: Open a terminal and navigate to the directory where your `docker-compose.yml` file is located.

3. **Run Docker Compose**: Start your containers by running:
   
   ```bash
   docker-compose up -d
   ```

4. **Access MySQL Container**: Find the name or ID of the MySQL container using the following command:

    ```bash
    docker ps
    ```

    Look for a container with a name like `taskmanagementapi_mysql_1` or similar.

5. **Connect to the MySQL Container**: Use the following command to open a bash shell inside the MySQL container (replace `container_name` with the actual name of your MySQL container):

    ```bash
    docker exec -it container_name bash
    ```

6. **Login to MySQL**: Once inside the container, you can log in to the MySQL server using the following command (replace `root` and `your_password` with your MySQL username and password defined in `.env` file):

    ```bash
    mysql -u root -p
    ```

    You will be prompted to enter `your_password`.

7. **Interact with the Database**: After successfully logging in, run the following SQL commands show the databases tables (replace `your_db_name` with your database name set in the `.env` file):

    ```sql
    SHOW DATABASES;
    USE your_db_name
    SHOW TABLES;
    ```

    Use the following SQL commands to view either the tasks or users tables:

    ```sql
    SELECT * FROM tasks;
    SELECT * FROM users;
    ```

8. **Exit MySQL and the Container**: To exit MySQL, type:

    ```sql
    EXIT;
    ```

## Testing the API on External IP

The Task Management API is also deployed on Google Kubernetes Engine and can be accessed using cURL at the external IP address `http://35.233.152.104:5000`.

1. **Register a new user**:

    ```bash
    curl -X POST http://35.233.152.104:5000/register \
    -H "Content-Type: application/json" \
    -d '{"username": "testuser", "password": "testpassword"}'
    ```

2. **Login the user** (save cookies):

    ```bash
    curl -X POST http://35.233.152.104:5000/login \
    -H "Content-Type: application/json" \
    -d '{"username": "testuser", "password": "testpassword"}' \
    -c cookie.txt
    ```

3. **Create a new task**:

    ```bash
    curl -X POST http://35.233.152.104:5000/tasks \
    -H "Content-Type: application/json" \
    -b cookie.txt \
    -d '{"title": "New Task", "description": "Description of the task", "dueDate": "2025-01-26T12:00:00", "status": "pending"}'
    ```

4. **Get all tasks**:

    ```bash
    curl -X GET http://35.233.152.104:5000/tasks \
    -b cookie.txt
    ```

5. **Get a task by ID**:

    ```bash
    curl -X GET http://35.233.152.104:5000/tasks/{id} \
    -b cookie.txt
    ```

6. **Update a task**:

    ```bash
    curl -X PUT http://35.233.152.104:5000/tasks/{id} \
    -H "Content-Type: application/json" \
    -b cookie.txt \
    -d '{"title": "Updated Task", "description": "Updated description", "dueDate": "2025-01-30T12:00:00", "status": "in-progress"}'
    ```

7. **Delete a task**:

    ```bash
    curl -X DELETE http://35.233.152.104:5000/tasks/{id} \
    -b cookie.txt
    ```

8. **Logout**:

    ```bash
    curl -X POST http://35.233.152.104:5000/logout \
    -b cookie.txt
    ```
