from fastapi import APIRouter, Response
from ..controllers.subtasks_controller import SubtaskController
router=APIRouter(
    prefix='/subtasks'
)

controller=SubtaskController()

router.add_api_route('/create',controller.create, methods=['POST'])
router.add_api_route('/subtasks',controller.read_my_subtasks, methods=['GET'])
router.add_api_route('/{id}',controller.update, methods=['PUT'])
router.add_api_route('/{id}',controller.delete, methods=['DELETE'])