# FastAPI Todo Application

A modern task management application built with [FastAPI](https://fastapi.tiangolo.com/) and [PostgreSQL](https://www.postgresql.org/).

## Project Structure

```
todo-app/
├── web_app.py          # FastAPI application and routes
├── todo_app.py         # Core business logic and database operations
├── requirements.txt    # Python dependencies
├── templates/          # Jinja2 HTML templates
│   └── index.html      # Main application template
├── Dockerfile          # Multi-stage build with Distroless base
├── docker-compose.yml  # Docker Compose configuration
├── README.md           # Project documentation
└── LICENSE             # MIT License
```

## Key Features

- Complete task management (Create, Read, Update, Delete)
- Task status tracking (Pending, In Progress, Completed)
- Secure [PostgreSQL](https://www.postgresql.org/) database integration
- [Jinja2](https://jinja.palletsprojects.com/) templating for dynamic HTML rendering
- [Docker](https://www.docker.com/) support with multi-stage build and [Distroless](https://github.com/GoogleContainerTools/distroless) base image
- Environment variable configuration
- Robust error handling

## Tech Stack

- **Backend Framework**: [FastAPI](https://fastapi.tiangolo.com/) 0.109.2
- **Database**: [PostgreSQL](https://www.postgresql.org/)
- **Template Engine**: [Jinja2](https://jinja.palletsprojects.com/) 3.1.3
- **Python Version**: [Python 3.11](https://www.python.org/downloads/)
- **Additional Dependencies**:
  - [uvicorn](https://www.uvicorn.org/) 0.27.1 (ASGI server)
  - [psycopg2-binary](https://pypi.org/project/psycopg2-binary/) (PostgreSQL adapter)
  - [python-multipart](https://pypi.org/project/python-multipart/) 0.0.6 (Form processing)
  - [typing-extensions](https://pypi.org/project/typing-extensions/) 4.9.0

## Prerequisites

- [Python 3.11+](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/download/) database
- [Docker](https://docs.docker.com/get-docker/) (optional, for containerized deployment)

## Deployment Options

### 1. 🚀 Quick Start with Docker Compose

The fastest way to get the application running locally:

1. **Clone the repository:**

   ```bash
   git clone https://gitlab.com/sela-tracks/1109/students/idosh/application/todo-app.git
   cd todo-app
   ```

2. **Start the application using the Docker image from Docker Hub:**

   ```bash
   docker compose up -d
   ```

3. **Access the application:**

   Open your browser and navigate to [http://localhost:8000](http://localhost:8000)

4. **Stop the application:**

   ```bash
   docker compose down
   ```

5. **Stop the application and remove all data:**

   ```bash
   docker compose down -v
   ```

6. **Remove the Docker image locally (if needed):**

   ```bash
   docker rmi idoshoshani123/my-todo-app:latest
   ```

### 2. Local Development Setup

1. **Clone the repository:**

   ```bash
   git clone https://gitlab.com/sela-tracks/1109/students/idosh/application/todo-app.git
   cd todo-app
   ```

2. **Create and activate virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables:**

   ```bash
   export DATABASE_HOST=localhost
   export DATABASE_NAME=your_db_name
   export DATABASE_USER=your_db_user
   export DATABASE_PASSWORD=your_password
   export DATABASE_PORT=5432
   ```

5. **Run the application:**

   ```bash
   uvicorn web_app:app --host 0.0.0.0 --port 8000
   ```

6. **Access the application:**

   Open your browser and navigate to [http://localhost:8000](http://localhost:8000)

### 3. Docker Deployment

1. **Run the container using the pre-built Docker image from Docker Hub:**

   ```bash
   docker run -d \
     --name todo-app \
     -e DATABASE_HOST=your_db_host \
     -e DATABASE_NAME=your_db_name \
     -e DATABASE_USER=your_db_user \
     -e DATABASE_PASSWORD=your_password \
     -e DATABASE_PORT=5432 \
     -p 8000:8000 \
     idoshoshani123/my-todo-app:latest
   ```

2. **Access the application:**

   Open your browser and navigate to [http://localhost:8000](http://localhost:8000)

3. **Remove the application:**

   - **Stop and remove the container:**

     ```bash
     docker rm -f todo-app
     ```

   - **Remove the Docker image:**

     ```bash
     docker rmi idoshoshani123/my-todo-app:latest
     ```

   - **Clean up unused containers and images:**

     ```bash
     docker container prune
     docker image prune
     ```

## Environment Variables

| Variable          | Description             | Required | Default |
| ----------------- | ----------------------- | -------- | ------- |
| DATABASE_HOST     | PostgreSQL host address | Yes      | -       |
| DATABASE_NAME     | Database name           | Yes      | -       |
| DATABASE_USER     | Database username       | Yes      | -       |
| DATABASE_PASSWORD | Database password       | Yes      | -       |
| DATABASE_PORT     | Database port           | No       | 5432    |

## API Endpoints

| Method | Endpoint                   | Description                       |
| ------ | -------------------------- | --------------------------------- |
| GET    | `/`                        | Display home page with all tasks  |
| POST   | `/add-task`                | Create a new task                 |
| POST   | `/update-status/{task_id}` | Update task status                |
| POST   | `/delete-task/{task_id}`   | Delete a task                     |
| POST   | `/update-task/{task_id}`   | Update task title and description |

## Database Schema

The application uses a single `tasks` table with the following structure:

```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) NOT NULL,
    due_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Security Features

- Database credentials managed through environment variables
- Non-root user in Docker container
- [Distroless](https://github.com/GoogleContainerTools/distroless) base image for minimal attack surface
- Input validation and sanitization
- Error handling for all database operations

## Error Handling

The application includes comprehensive error handling for:

- Database connection issues
- Task creation/update/deletion operations
- Invalid status updates
- Missing environment variables

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT) - see the [LICENSE](LICENSE) file for details.

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/tutorial/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Python venv Documentation](https://docs.python.org/3/library/venv.html)
- [Uvicorn Documentation](https://www.uvicorn.org/)

---

[Back to Top](#fastapi-todo-application)
