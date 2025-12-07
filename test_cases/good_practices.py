# Test Case: Good Practices - Clean Code
# Expected Quality: A
# Expected Bugs: 0


from typing import List, Optional
from dataclasses import dataclass
from enum import Enum

class Status(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"

@dataclass
class Task:
    id: int
    title: str
    description: str
    status: Status
    
    def mark_completed(self) -> None:
        """Mark task as completed."""
        self.status = Status.COMPLETED
    
    def is_active(self) -> bool:
        """Check if task is active."""
        return self.status == Status.ACTIVE

class TaskManager:
    def __init__(self):
        self.tasks: List[Task] = []
    
    def add_task(self, task: Task) -> None:
        """Add a new task."""
        if not isinstance(task, Task):
            raise TypeError("Expected Task object")
        self.tasks.append(task)
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """Get task by ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def get_completed_tasks(self) -> List[Task]:
        """Get all completed tasks."""
        return [t for t in self.tasks if t.status == Status.COMPLETED]
