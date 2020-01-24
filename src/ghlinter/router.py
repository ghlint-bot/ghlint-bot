from aiohttp import web
from gidgethub import routing
from gidgethub.routing import Router

router: Router

def load():
    global router
    router = routing.Router()