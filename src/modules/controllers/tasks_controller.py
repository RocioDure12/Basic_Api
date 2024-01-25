from ..repositories.tasks_repository import TasksRepository

class TasksController:
    def __init__(self):
        self._tasks_repository=TasksRepository()
    
    def create(self):
        return self._tasks_repository.create()
    
    def read(self):
        return self._tasks_repository.read_my_tasks()
    
    def update(self):
        return self._tasks_repository.update()
    
    def delete(self):
        return self._tasks_repository.delete()