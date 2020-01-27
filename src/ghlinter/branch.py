import requests
from gidgethub.aiohttp import GitHubAPI

async def create_branch(repo_owner: str, repo_name: str, new_branch_name: str, github_object: GitHubAPI) -> None:
    new_branch_name = new_branch_name.replace(' ', '-')
    response = requests.get(f'https://api.github.com/repos/{repo_owner}/{repo_name}/git/refs/heads')
    data = response.json()
    sha = data[0]['object']['sha']
    payload = {
        'ref': f'refs/heads/{new_branch_name}',
        'sha': sha
    }
    await github_object.post(f'repos/{repo_owner}/{repo_name}/git/refs', data=payload)