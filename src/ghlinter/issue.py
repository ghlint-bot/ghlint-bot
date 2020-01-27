import re
from gidgethub.sansio import Event
from gidgethub.aiohttp import GitHubAPI
from ghlinter import config_manager
from ghlinter import branch
from ghlinter.store import store

class Issue:
    def __init__(self, event: Event, github_object: GitHubAPI):
        self.event = event
        self.github_object = github_object

    def get_url(self) -> str:
        repo_owner: str = self.get_repo_owner()
        repo_name: str = self.get_repo_name()
        issue_number: str = self.get_number()
        return f'/repos/{repo_owner}/{repo_name}/issues/{issue_number}'

    def get_repo_owner(self) -> str:
        return self.event.data['repository']['owner']['login']

    def get_repo_name(self) -> str:
        return self.event.data['repository']['name']

    def get_number(self) -> str:
        return self.event.data['issue']['number']

    def get_comment_url(self) -> str:
        return self.event.data['issue']['comments_url']

    def get_author(self) -> str:
        return self.event.data['issue']['user']['login']

    def get_title(self) -> str:
        return self.event.data['issue']['title']

    def is_formatted_correctly(self) -> bool:
        title: str = self.get_title()
        is_valid: bool = False
        for issue_type in config_manager.issues()['types']:
            if title.startswith('(' + issue_type + ')'):
                is_valid = True
                break
    
        return is_valid and re.search(config_manager.issues()['title_format'], title) != None

    def is_registered_command(self, command: str) -> bool:
        for cli_command in config_manager.issues()['cli']:
            if store.format_string(cli_command['command']) == command:
                return True
        return False

    async def comment(self, body: str) -> None:
        url: str = self.get_comment_url()
        await self.github_object.post(url, data={'body': body})

    async def close(self) -> None:
        url: str = self.get_url()
        await self.github_object.patch(url, data={'state': 'closed'})

    async def dispatch(self, command: str) -> None:
        if command == '@' + config_manager.bot_name() + ' create branch':
            await branch.create_branch(self.get_repo_owner(), self.get_repo_name(), self.get_title(), self.github_object)