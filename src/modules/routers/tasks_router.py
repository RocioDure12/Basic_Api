from fastapi import APIRouter, Response
from ..controllers.tasks_controller import TasksController

router=APIRouter(
    prefix='/tasks'
)

controller=TasksController()

router.add_api_route('/create',controller.create, methods=['POST'])
router.add_api_route('/my_tasks',controller.read_my_tasks, methods=['GET'])
router.add_api_route('/task/{id}',controller.get_task_by_id, methods=['GET'])
router.add_api_route('/{id}',controller.update, methods=['PUT'])
router.add_api_route('/{id}',controller.delete, methods=['DELETE'])




