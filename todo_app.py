from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
import psycopg2
import os
from enum import Enum

class TaskStatus(Enum):
    """Enum for representing task status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

@dataclass
class DatabaseConfig:
    """
    Database connection configuration
    
    Attributes:
        host (str): Database host address
        database (str): Database name
        user (str): Database user
        password (str): Database password
        port (int): Database port
    """
    host: str = os.getenv('DATABASE_HOST')
    database: str = os.getenv('DATABASE_NAME')
    user: str = os.getenv('DATABASE_USER')
    password: str = os.getenv('DATABASE_PASSWORD')
    port: int = int(os.getenv('DATABASE_PORT', 5432))
    
    # Checks for a missing environment variables.
    def __post_init__(self):
        missing_vars = []
        if not self.host:
            missing_vars.append('DATABASE_HOST')
        if not self.database:
            missing_vars.append('DATABASE_NAME')
        if not self.user:
            missing_vars.append('DATABASE_USER')
        if not self.password:
            missing_vars.append('DATABASE_PASSWORD')
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

@dataclass
class Task:
    """
    Represents a todo task
    
    Attributes:
        id (Optional[int]): Task ID (None for new tasks)
        title (str): Task title
        description (Optional[str]): Task description
        status (TaskStatus): Current task status
        due_date (Optional[datetime]): Task due date
        created_at (datetime): Task creation timestamp
    """
    id: Optional[int]
    title: str
    description: Optional[str]
    status: TaskStatus
    due_date: Optional[datetime]
    created_at: datetime

class TodoManager:
    """Manages todo tasks in the PostgreSQL database"""
    
    def __init__(self, config: DatabaseConfig):
        """
        Initialize TodoManager with database configuration
        
        Args:
            config: Database connection parameters
        """
        self.config = config
        self.conn = None
        self.cur = None
    
    def connect(self) -> None:
        """
        Establish database connection
        
        Raises:
            Exception: If connection fails
        """
        try:
            self.conn = psycopg2.connect(
                host=self.config.host,
                database=self.config.database,
                user=self.config.user,
                password=self.config.password,
                port=self.config.port
            )
            self.cur = self.conn.cursor()
            print("Successfully connected to the database")
        except Exception as e:
            print(f"Connection error: {e}")
            raise
    
    def close(self) -> None:
        """Close database connection"""
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
            print("Database connection closed")
    
    def create_tables(self) -> None:
        """Create the tasks table if it doesn't exist"""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(200) NOT NULL,
            description TEXT,
            status VARCHAR(20) NOT NULL,
            due_date TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        try:
            self.cur.execute(create_table_query)
            self.conn.commit()
            print("Tasks table created successfully")
        except Exception as e:
            print(f"Error creating table: {e}")
            self.conn.rollback()
    
    def add_task(self, task: Task) -> Optional[int]:
        """
        Add a new task to the database
        
        Args:
            task: Task object containing task details
            
        Returns:
            int: ID of the created task, or None if creation failed
        """
        insert_query = """
        INSERT INTO tasks (title, description, status, due_date, created_at)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
        """
        try:
            self.cur.execute(insert_query, (
                task.title,
                task.description,
                task.status.value,
                task.due_date,
                task.created_at or datetime.now()
            ))
            task_id = self.cur.fetchone()[0]
            self.conn.commit()
            print(f"Task created successfully with ID: {task_id}")
            return task_id
        except Exception as e:
            print(f"Error adding task: {e}")
            self.conn.rollback()
            return None
    
    def update_task_status(self, task_id: int, status: TaskStatus) -> bool:
        """
        Update the status of a task
        
        Args:
            task_id: ID of the task to update
            status: New status to set
            
        Returns:
            bool: True if update successful, False otherwise
        """
        update_query = """
        UPDATE tasks
        SET status = %s
        WHERE id = %s;
        """
        try:
            self.cur.execute(update_query, (status.value, task_id))
            self.conn.commit()
            print(f"Task {task_id} status updated to {status.value}")
            return True
        except Exception as e:
            print(f"Error updating task status: {e}")
            self.conn.rollback()
            return False
    
    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks from the database
        
        Returns:
            List[Task]: List of all tasks
        """
        select_query = "SELECT * FROM tasks ORDER BY created_at DESC;"
        try:
            self.cur.execute(select_query)
            rows = self.cur.fetchall()
            return [
                Task(
                    id=row[0],
                    title=row[1],
                    description=row[2],
                    status=TaskStatus(row[3]),
                    due_date=row[4],
                    created_at=row[5]
                )
                for row in rows
            ]
        except Exception as e:
            print(f"Error retrieving tasks: {e}")
            return []

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task from the database
        
        Args:
            task_id: ID of the task to delete
            
        Returns:
            bool: True if deletion successful, False otherwise
        """
        delete_query = "DELETE FROM tasks WHERE id = %s;"
        try:
            self.cur.execute(delete_query, (task_id,))
            self.conn.commit()
            print(f"Task {task_id} deleted successfully")
            return True
        except Exception as e:
            print(f"Error deleting task: {e}")
            self.conn.rollback()
            return False

    def update_task(self, task_id: int, title: str, description: str) -> bool:
        """
        Update task title and description
        
        Args:
            task_id: ID of the task to update
            title: New title
            description: New description
            
        Returns:
            bool: True if update successful, False otherwise
        """
        update_query = """
        UPDATE tasks
        SET title = %s, description = %s
        WHERE id = %s;
        """
        try:
            self.cur.execute(update_query, (title, description, task_id))
            self.conn.commit()
            print(f"Task {task_id} updated successfully")
            return True
        except Exception as e:
            print(f"Error updating task: {e}")
            self.conn.rollback()
            return False
