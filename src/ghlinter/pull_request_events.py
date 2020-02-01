from gidgethub.sansio import Event
from gidgethub.aiohttp import GitHubAPI

async def assigned(event: Event, github_object: GitHubAPI) -> None:
    pass

async def unassigned(event: Event, github_object: GitHubAPI) -> None:
    pass

async def review_requested(event: Event, github_object: GitHubAPI) -> None:
    pass

async def review_request_removed(event: Event, github_object: GitHubAPI) -> None:
    pass

async def labeled(event: Event, github_object: GitHubAPI) -> None:
    pass

async def unlabeled(event: Event, github_object: GitHubAPI) -> None:
    pass

async def opened(event: Event, github_object: GitHubAPI) -> None:
    pass

async def edited(event: Event, github_object: GitHubAPI) -> None:
    pass

async def closed(event: Event, github_object: GitHubAPI) -> None:
    pass

async def reopened(event: Event, github_object: GitHubAPI) -> None:
    pass

async def ready_for_review(event: Event, github_object: GitHubAPI) -> None:
    pass

async def locked(event: Event, github_object: GitHubAPI) -> None:
    pass

async def unlocked(event: Event, github_object: GitHubAPI) -> None:
    pass