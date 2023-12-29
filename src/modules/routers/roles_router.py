from fastapi import APIRouter, Response
from ..controllers.roles_controller import RolesController

router=APIRouter(
    prefix='/roles'
)

controller=RolesController()

router.add_api_route('/{id}',controller.update, methods=['PUT'])
router.add_api_route('/',controller.create, methods=['POST'])
router.add_api_route('/',controller.read, methods=['GET'])
router.add_api_route('/{id}', controller.delete, methods=['DELETE'])

