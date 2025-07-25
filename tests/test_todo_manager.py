import unittest
from unittest.mock import MagicMock

from todo_app import TodoManager, DatabaseConfig, TaskStatus


class TestTodoManagerUpdateTaskStatus(unittest.TestCase):
    def _create_manager(self, rowcount: int) -> TodoManager:
        # Create TodoManager with dummy config and mocked DB connection
        config = DatabaseConfig(
            host="localhost",
            database="db",
            user="user",
            password="pass",
            port=5432,
        )
        manager = TodoManager(config)
        manager.conn = MagicMock()
        manager.cur = MagicMock()
        manager.cur.rowcount = rowcount
        return manager

    def test_update_status_returns_false_when_no_task(self):
        manager = self._create_manager(rowcount=0)
        result = manager.update_task_status(1, TaskStatus.COMPLETED)

        manager.cur.execute.assert_called_once()
        manager.conn.rollback.assert_called_once()
        manager.conn.commit.assert_not_called()
        self.assertFalse(result)

    def test_update_status_returns_true_on_success(self):
        manager = self._create_manager(rowcount=1)
        result = manager.update_task_status(1, TaskStatus.IN_PROGRESS)

        manager.cur.execute.assert_called_once()
        manager.conn.commit.assert_called_once()
        manager.conn.rollback.assert_not_called()
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
