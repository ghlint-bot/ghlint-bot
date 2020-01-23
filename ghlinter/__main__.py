import os
import re
import json
import aiohttp

from aiohttp import web
from gidgethub import routing, sansio
from gidgethub import aiohttp as gh_aiohttp

# GLOBAL variable setup
routes = web.RouteTableDef()
router = routing.Router()
config_file: json = {}

# global utility functions
def load_json_file(path: str) -> json:
    file = open(path, 'r')
    data: json = json.loads(file.read())
    file.close()
    return data

# issue class. used to get information about a given issue payload
class Issue:
    def __init__(self, event: sansio.Event, github_object: gh_aiohttp.GitHubAPI):
        self.event = event
        self.github_object = github_object

    def get_url(self) -> str:
        repo_owner: str = self.get_repo_owner()
        repo_name: str = self.get_repo_name()
        issue_number: str = self.get_issue_number()
        return f'/repos/{repo_owner}/{repo_name}/issues/{issue_number}'

    def get_repo_owner(self) -> str:
        return self.event.data['repository']['owner']['login']

    def get_repo_name(self) -> str:
        return self.event.data['repository']['name']

    def get_issue_number(self) -> str:
        return self.event.data['issue']['number']

    def get_comment_url(self) -> str:
        return self.event.data['issue']['comments_url']

    def get_author(self) -> str:
        return self.event.data['issue']['user']['login']

    def get_title(self) -> str:
        return self.event.data['issue']['title']

    def is_formatted_correctly(self) -> bool:
        title: str = self.get_title()
        return re.search(config_file['issues']['title_format'], title) != None

    def is_registered_command(self, command: str) -> bool:
        for command in config_file['issues']['cli']:
            if command['command'] == command:
                return True
        return False

    async def comment(self, body: str) -> None:
        url: str = self.get_comment_url()
        await self.github_object.post(url, data={'body': body})

    async def close(self) -> None:
        url: str = self.get_url()
        await self.github_object.patch(url, data={'state': 'closed'})

    async def dispatch(self, command: str) -> None:
        if command == config_file['bot_name'] + ' create branch':
            # TODO implement
            pass

@router.register("issues", action="opened")
async def issue_opened_event(event: sansio.Event, github_object: gh_aiohttp.GitHubAPI, *args, **kawrgs):
    """ endpoint for when an issue is opened """
    issue: Issue = Issue(event, github_object)

    # first check that the formatting is correct
    if not issue.is_formatted_correctly():
        await issue.comment('title is formatted incorrectly. closing issue. please resubmit your issue in the correct format')
        await issue.close()
        return

    # issue is formatted correctly post on opened comment
    comment: str = config_file['issues']['on_opened_comment']
    if comment != None:
        await issue.comment(comment)

@router.register("issues", action="closed")
async def issue_closed_event(event: sansio.Event, github_object: gh_aiohttp.GitHubAPI, *args, **kwargs):
    """ endpoint for when an issue is closed """
    issue: Issue = Issue(event, github_object)

    comment: str = config_file['issues']['on_closed_comment']
    if comment != None:
        await issue.comment(comment)

@router.register("issues", action="assigned")
async def issue_assigned_event(event: sansio.Event, github_object: gh_aiohttp.GitHubAPI, *args, **kwargs):
    """ endpoint for when an issue is assigned """
    issue: Issue = Issue(event, github_object)

    comment: str = config_file['issues']['on_assigned_comment']
    if comment != None:
        await issue.comment(comment)

@router.register("issues", action="unassigned")
async def issue_unassigned_event(event: sansio.Event, github_object: gh_aiohttp.GitHubAPI, *args, **kwargs):
    """ endpoint for when an issue is unassigned """
    issue: Issue = Issue(event, github_object)

    comment: str = config_file['issues']['on_unassigned_comment']
    if comment != None:
        await issue.comment(comment)

@router.register("issue_comment", action="created")
async def issue_commented_event(event: sansio.Event, github_object: gh_aiohttp.GitHubAPI, * args, **kwargs):
    """ endpoint for when someone comments on an issue """
    issue: Issue = Issue(event, github_object)
    comment: str = event.data['comment']['body']

    # check if bot posted this comment so we can ignore
    if event.data['comment']['user']['login'] == config_file['bot_name']: # TODO find way to change this 
        return

    if issue.is_registered_command(comment):
        await issue.dispatch(comment)
    else:
        await issue.comment(f'sorry, [{comment}] is not a registered command')

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
        gh = gh_aiohttp.GitHubAPI(session, config_file['bot_name'], oauth_token=oauth_token)

        # call for the appropriate callback for the event
        await router.dispatch(event, gh)

    # return a "Success"
    return web.Response(status=200)

if __name__ == "__main__":
    config_file = load_json_file('config.json')
    app = web.Application()
    app.add_routes(routes)
    port = os.environ.get("PORT")
    if port is not None:
        port = int(port)
    web.run_app(app, port=port)