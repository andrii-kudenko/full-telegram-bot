from . import *
from .friendships_empty_handler import friendships_empty_router
from .friendships_bio_handler import friendships_bio_router
from .friendships_search_handler import friendships_search_router
from .friendships_commands_handler import frienships_commands_router

friendships_router = Router(name=__name__)
friendships_router.include_routers(frienships_commands_router, 
                                   friendships_bio_router, friendships_search_router, friendships_empty_router)