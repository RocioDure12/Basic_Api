from ..repositories.categories_repository import CategoriesRepository
from ..models.category import Category
from typing import Annotated
from ..models.user import User
from fastapi import Security
from ..services.token_services import TokenServices

class CategoriesController():
    def __init__(self):
        self.categories_repository=CategoriesRepository()
        
    
    def create(self, item:Category, user:Annotated[User,
                                  Security(TokenServices.check_access_token,
                                           scopes=['categories:create'])]):
        return self.categories_repository.create(item)
    
    def read_my_categories(self, id:int,user:Annotated[User,
                                  Security(TokenServices.check_access_token,
                                           scopes=['categories:read_my_categories'])]):
        return self.categories_repository.read_my_categories(id)
    
    def update(self, update_item:Category, id:int,user:Annotated[User,
                                  Security(TokenServices.check_access_token,
                                           scopes=['categories:update'])]):
        return self.categories_repository.update(update_item, id)
    
    def delete(self,id,user:Annotated[User,
                                  Security(TokenServices.check_access_token,
                                           scopes=['categories:delete'])]):
        return self.categories_repository.delete(id)

        
    