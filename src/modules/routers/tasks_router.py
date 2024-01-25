from fastapi import APIRouter, Response
from ..controllers.tasks_controller import TasksController

router=APIRouter(
    prefix='/tasks'
)

controller=TasksController()

router.add_api_route('/{id}',controller.update, methods=['PUT'])

