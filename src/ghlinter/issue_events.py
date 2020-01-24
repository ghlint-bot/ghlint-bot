from gidgethub.sansio import Event
from gidgethub.aiohttp import GitHubAPI
# from ghlinter.router import router
from ghlinter.issue import Issue
from ghlinter.store import store
from ghlinter.router import router
from ghlinter import config_manager

@router.register("issue", action="opened")
async def opened(event: Event, github_object: GitHubAPI, *args, **kwargs) -> None:
    """ endpoint for when an issue is opened """
    issue: Issue = Issue(event, github_object)

    # first check that the formatting is correct
    if not issue.is_formatted_correctly():
        await issue.comment('title is formatted incorrectly. closing issue. please resubmit your issue in the correct format')
        await issue.close()
        return

    # issue is formatted correctly post on opened comment
    comment: str = store.format_string(config_manager.issues()['on_opened_comment'])
    if comment != None:
        await issue.comment(comment)

@router.register("issue", action="closed")
async def closed(event: Event, github_object: GitHubAPI, *args, **kwargs) -> None:
    """ endpoint for when an issue is closed """
    issue: Issue = Issue(event, github_object)

    comment: str = store.format_string(config_manager.issues()['on_closed_comment'])
    if comment != None:
        await issue.comment(comment)

@router.register("issue", action="assigned")
async def assigned(event: Event, github_object: GitHubAPI, *args, **kwargs) -> None:
    """ endpoint for when an issue is assigned """
    issue: Issue = Issue(event, github_object)

    comment: str = store.format_string(config_manager.issues()['on_assigned_comment'])
    if comment != None:
        await issue.comment(comment)

@router.register("issue", action="unassigned")
async def unassigned(event: Event, github_object: GitHubAPI, *args, **kwargs) -> None:
    """ endpoint for when an issue is unassigned """
    issue: Issue = Issue(event, github_object)

    comment: str = store.format_string(config_manager.issues()['on_unassigned_comment'])
    if comment != None:
        await issue.comment(comment)

@router.register("issue_comment", action="created")
async def commented(event: Event, github_object: GitHubAPI, *args, **kwargs) -> None:
    """ endpoint for when someone comments on an issue """
    issue: Issue = Issue(event, github_object)
    comment: str = store.format_string(event.data['comment']['body'])

    # check if bot posted this comment so we can ignore
    if event.data['comment']['user']['login'] == config_manager.bot_name():
        return

    if issue.is_registered_command(comment):
        await issue.dispatch(comment)
    else:
        await issue.comment(f'sorry, [{comment}] is not a registered command')