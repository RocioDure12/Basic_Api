from fastapi import APIRouter, Response
from ..controllers.users_controller import UsersController


router=APIRouter(
    prefix='/users'
)

controller=UsersController()

router.add_api_route('/',controller.create, methods=['POST'])
router.add_api_route('/',controller.read, methods=['GET'])
router.add_api_route('/{id}',controller.update, methods=['PUT'])
router.add_api_route('/{id}', controller.delete, methods=['DELETE'])
router.add_api_route('/login', controller.login_user, methods=['POST'])
router.add_api_route('/readme',controller.read_me, methods=['GET'])
router.add_api_route('/{id}', controller.read_by_id, methods=['GET'])




