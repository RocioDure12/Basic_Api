from fastapi import APIRouter, Response
from ..controllers.categories_controller import CategoriesController

router=APIRouter(
    prefix='/categories'
)

controller=CategoriesController()

router.add_api_route('/create',controller.create, methods=['POST'])
router.add_api_route('/my_tasks',controller.read_my_categories, methods=['GET'])
router.add_api_route('/{id}',controller.update, methods=['PUT'])
router.add_api_route('/{id}',controller.delete, methods=['DELETE'])




