import os
import re
import json
import aiohttp

from aiohttp import web
from gidgethub import routing, sansio
from gidgethub import aiohttp as gh_aiohttp

from ghlinter.issue import Issue
from ghlinter import config_manager
from ghlinter import issue_events

#### router setup
routes = web.RouteTableDef()
router = routing.Router()

#### issue routes
@router.register("issues", action="opened")
async def issue_opened_event(event: sansio.Event, github_object: gh_aiohttp.GitHubAPI, *args, **kawrgs):
    """ endpoint for when an issue is opened """
    await issue_events.opened(event, github_object)

@router.register("issues", action="closed")
async def issue_closed_event(event: sansio.Event, github_object: gh_aiohttp.GitHubAPI, *args, **kwargs):
    """ endpoint for when an issue is closed """
    await issue_events.closed(event, github_object)

@router.register("issues", action="assigned")
async def issue_assigned_event(event: sansio.Event, github_object: gh_aiohttp.GitHubAPI, *args, **kwargs):
    """ endpoint for when an issue is assigned """
    await issue_events.assigned(event, github_object)

@router.register("issues", action="unassigned")
async def issue_unassigned_event(event: sansio.Event, github_object: gh_aiohttp.GitHubAPI, *args, **kwargs):
    """ endpoint for when an issue is unassigned """
    await issue_events.unassigned(event, github_object)

@router.register("issue_comment", action="created")
async def issue_commented_event(event: sansio.Event, github_object: gh_aiohttp.GitHubAPI, * args, **kwargs):
    """ endpoint for when someone comments on an issue """
    await issue_events.commented(event, github_object)

#### pull request routes

#### webhook route
@routes.post("/")
async def main(request):
    # read the GitHub webhook payload
    body = await request.read()

    #our authentication token and secret
    secret = os.environ.get("GH_SECRET")
    oauth_token = os.environ.get("GH_AUTH")

    # a representation of Github webhook event
    event = sansio.Event.from_http(request.headers, body, secret=secret)

    async with aiohttp.ClientSession() as session:
        gh = gh_aiohttp.GitHubAPI(session, config_manager.bot_name(), oauth_token=oauth_token)

        # call for the appropriate callback for the event
        await router.dispatch(event, gh)

    # return a "Success"
    return web.Response(status=200)

if __name__ == "__main__":
    config_manager.load()
    app = web.Application()
    app.add_routes(routes)
    port = os.environ.get("PORT")
    if port is not None:
        port = int(port)
    web.run_app(app, port=port)