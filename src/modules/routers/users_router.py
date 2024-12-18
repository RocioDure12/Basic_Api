from fastapi import APIRouter, Response
from ..controllers.users_controller import UsersController
from typing import List
from ..models.user import User

router=APIRouter(
    prefix='/users'
)

controller=UsersController()


router.add_api_route('/login', controller.login_user, methods=['POST'])
router.add_api_route('/create',controller.create_user, methods=['POST'])
router.add_api_route('/cookies', controller.get_auth_cookies, methods=['GET'])
router.add_api_route('/logout', controller.logout, methods=['POST'])
#router.add_api_route('/',controller.read, methods=['GET'])
router.add_api_route('/{id}',controller.update, methods=['PUT'])
router.add_api_route('/{id}', controller.delete, methods=['DELETE'])

router.add_api_route('/readme',controller.read_me, methods=['GET'])
router.add_api_route('/refresh-token', controller.refresh_access_token, methods=['GET'])
router.add_api_route('/pagination', controller.read_users_paginated, methods=['GET'],response_model=List[User])
router.add_api_route('/{id}', controller.read_by_id, methods=['GET'])
router.add_api_route('/verification/{token}', controller.verify_email_account, methods=['POST'])
router.add_api_route('/admin', controller.create_admin, methods=['POST'])






