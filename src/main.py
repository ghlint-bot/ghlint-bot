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
from ghlinter import pull_request_events

#### router setup
routes = web.RouteTableDef()
router = routing.Router()

#####################################################################################################################################################
#### issue routes
####
#####################################################################################################################################################
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

#####################################################################################################################################################
#### pull request routes
####
#####################################################################################################################################################
@router.register("pull_request", action="assigned")
async def pull_request_assigned_event(event: sansio.Event, github_object: gh_aiohttp.GitHubAPI, * args, **kwargs):
    """ endpoint for when someone assigns a pull request """
    await pull_request_events.assigned(event, github_object)

@router.register("pull_request", action="unassigned")
async def pull_request_unassigned_event(event: sansio.Event, github_object: gh_aiohttp.GitHubAPI, * args, **kwargs):
    """ endpoint for when someone unassigns a pull request """
    await pull_request_events.unassigned(event, github_object)

@router.register("pull_requst", action="review_requested")
async def pull_request_review_requested_event(event: sansio.Event, github_object: gh_aiohttp.GitHubAPI, * args, **kwargs):
    """ endpoint for when someone requests a review for a pull request """
    await pull_request_events.review_requested(event, github_object)

@router.register("pull_requst", action="review_request_removed")
async def pull_request_review_request_removed_event(event: sansio.Event, github_object: gh_aiohttp.GitHubAPI, * args, **kwargs):
    """ endpoint for when someone removes a review request for a pull request """
    await pull_request_events.review_request_removed(event, github_object)

@router.register("pull_requst", action="labeled")
async def pull_request_labeled_event(event: sansio.Event, github_object: gh_aiohttp.GitHubAPI, * args, **kwargs):
    """ endpoint for when someone labels a pull request """
    await pull_request_events.labeled(event, github_object)

@router.register("pull_requst", action="unlabeled")
async def pull_request_unlabeled_event(event: sansio.Event, github_object: gh_aiohttp.GitHubAPI, * args, **kwargs):
    """ endpoint for when someone unlabels a pull request """
    await pull_request_events.unlabeled(event, github_object)

@router.register("pull_requst", action="opened")
async def pull_request_opened_event(event: sansio.Event, github_object: gh_aiohttp.GitHubAPI, * args, **kwargs):
    """ endpoint for when someone opens a pull request """
    await pull_request_events.opened(event, github_object)

@router.register("pull_requst", action="edited")
async def pull_request_edited_event(event: sansio.Event, github_object: gh_aiohttp.GitHubAPI, * args, **kwargs):
    """ endpoint for when someone edits a pull request """
    await pull_request_events.edited(event, github_object)

@router.register("pull_requst", action="closed")
async def pull_request_closed_event(event: sansio.Event, github_object: gh_aiohttp.GitHubAPI, * args, **kwargs):
    """ endpoint for when someone closes a pull request """
    await pull_request_events.closed(event, github_object)

@router.register("pull_requst", action="reopened")
async def pull_request_reopened_event(event: sansio.Event, github_object: gh_aiohttp.GitHubAPI, * args, **kwargs):
    """ endpoint for when someone reopens a pull request """
    await pull_request_events.reopened(event, github_object)

@router.register("pull_requst", action="ready_for_review")
async def pull_request_ready_for_review_event(event: sansio.Event, github_object: gh_aiohttp.GitHubAPI, * args, **kwargs):
    """ endpoint for when a pull request  is ready or review """
    await pull_request_events.ready_for_review(event, github_object)

@router.register("pull_requst", action="locked")
async def pull_request_locked_event(event: sansio.Event, github_object: gh_aiohttp.GitHubAPI, * args, **kwargs):
    """ endpoint for when someone locks a pull request """
    await pull_request_events.locked(event, github_object)

@router.register("pull_requst", action="unlocked")
async def pull_request_unlocked_event(event: sansio.Event, github_object: gh_aiohttp.GitHubAPI, * args, **kwargs):
    """ endpoint for when someone unlocks a pull request """
    await pull_request_events.unlocked(event, github_object)

#####################################################################################################################################################
#### webhook route
####
#####################################################################################################################################################
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