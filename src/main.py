import os
import re
import json
import aiohttp

from aiohttp import web
from gidgethub import routing, sansio
from gidgethub import aiohttp as gh_aiohttp

from ghlinter.issue import Issue
from ghlinter import config_manager

#temp
from ghlinter.store import store
from ghlinter import router

# GLOBAL variable setup
routes = web.RouteTableDef()
# router = routing.Router()

#### GLOBAL User Variables
## available user variables when creating commands and responses
##
## author:      author of the given issue or pull request
## number:      number of the given issue or pull request
## assignees:   list of users assigned to given issue or pull request
## unassignee:  user unassigned from given issue or pull request (only available on unassigned events)
## bot_name:    name of the bot (ghlint-bot)
# class Store:
#     def __init__(self):
#         self.author = ''
#         self.number = 0
#         self.assignees = []
#         self.unassignee = ''

#     def format_string(self, string: str) -> str:
#         return string.format(
#         author = self.author, 
#         number=self.number, 
#         assignees=self.assignees, 
#         unassignee=self.unassignee, 
#         bot_name=config_manager.bot_name()
#     )

# store: Store = Store()

# def format_user_globals(src: str) -> str:
#     return src.format(
#         author = global_variable_store.author, 
#         number=global_variable_store.number, 
#         assignees=global_variable_store.assignees, 
#         unassignee=global_variable_store.unassignee, 
#         bot_name=config_manager.bot_name()
#     )

# @router.register("issues", action="opened")
# async def issue_opened_event(event: sansio.Event, github_object: gh_aiohttp.GitHubAPI, *args, **kawrgs):
#     """ endpoint for when an issue is opened """
#     issue: Issue = Issue(event, github_object)

#     # first check that the formatting is correct
#     if not issue.is_formatted_correctly():
#         await issue.comment('title is formatted incorrectly. closing issue. please resubmit your issue in the correct format')
#         await issue.close()
#         return

#     # issue is formatted correctly post on opened comment
#     comment: str = store.format_string(config_manager.issues()['on_opened_comment'])
#     if comment != None:
#         await issue.comment(comment)

# @router.register("issues", action="closed")
# async def issue_closed_event(event: sansio.Event, github_object: gh_aiohttp.GitHubAPI, *args, **kwargs):
#     """ endpoint for when an issue is closed """
#     issue: Issue = Issue(event, github_object)

#     comment: str = store.format_string(config_manager.issues()['on_closed_comment'])
#     if comment != None:
#         await issue.comment(comment)

# @router.register("issues", action="assigned")
# async def issue_assigned_event(event: sansio.Event, github_object: gh_aiohttp.GitHubAPI, *args, **kwargs):
#     """ endpoint for when an issue is assigned """
#     issue: Issue = Issue(event, github_object)

#     comment: str = store.format_string(config_manager.issues()['on_assigned_comment'])
#     if comment != None:
#         await issue.comment(comment)

# @router.register("issues", action="unassigned")
# async def issue_unassigned_event(event: sansio.Event, github_object: gh_aiohttp.GitHubAPI, *args, **kwargs):
#     """ endpoint for when an issue is unassigned """
#     issue: Issue = Issue(event, github_object)

#     comment: str = store.format_string(config_manager.issues()['on_unassigned_comment'])
#     if comment != None:
#         await issue.comment(comment)

# @router.register("issue_comment", action="created")
# async def issue_commented_event(event: sansio.Event, github_object: gh_aiohttp.GitHubAPI, * args, **kwargs):
#     """ endpoint for when someone comments on an issue """
#     issue: Issue = Issue(event, github_object)
#     comment: str = store.format_string(event.data['comment']['body'])

#     # check if bot posted this comment so we can ignore
#     if event.data['comment']['user']['login'] == config_manager.bot_name():
#         return

#     if issue.is_registered_command(comment):
#         await issue.dispatch(comment)
#     else:
#         await issue.comment(f'sorry, [{comment}] is not a registered command')

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
        await router.router.dispatch(event, gh)

    # return a "Success"
    return web.Response(status=200)

if __name__ == "__main__":
    config_manager.load()
    router.load()
    app = web.Application()
    app.add_routes(routes)
    port = os.environ.get("PORT")
    if port is not None:
        port = int(port)
    web.run_app(app, port=port)