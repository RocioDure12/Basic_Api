from fastapi import APIRouter, Response
from ..controllers.tasks_controller import TasksController

router=APIRouter(
    prefix='/tasks'
)

controller=TasksController()

router.add_api_route('/',controller.create, methods=['POST'])
router.add_api_route('/my_tasks',controller.read_my_tasks, methods=['GET'])


