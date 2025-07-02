from fastapi import APIRouter, Response
from ..controllers.tasks_controller import TasksController

router=APIRouter(
    prefix='/tasks'
)

controller=TasksController()
router.add_api_route('/dates_for_calendar',controller.get_task_dates_for_calendar, methods=['GET'])

router.add_api_route('/percentage',controller.calculate_percentage_tasks_completed, methods=['GET'])
router.add_api_route('/pagination', controller.read_tasks_paginated, methods=['GET'])
router.add_api_route('/count_tasks', controller.count_tasks, methods=['GET'])
router.add_api_route('/upcoming_tasks', controller.get_upcoming_tasks, methods=['GET'])


router.add_api_route('/{id}',controller.get_task_by_id, methods=['GET'])
router.add_api_route('/create',controller.create, methods=['POST'])
router.add_api_route('/',controller.read_my_tasks, methods=['GET'])

router.add_api_route('/{id}',controller.update, methods=['PUT'])
router.add_api_route('/{id}',controller.delete, methods=['DELETE'])





