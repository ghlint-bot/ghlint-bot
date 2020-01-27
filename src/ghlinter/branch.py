import requests
from gidgethub.aiohttp import GitHubAPI

async def create_branch(repo_owner: str, repo_name: str, new_branch_name: str, github_object: GitHubAPI) -> None:
    print(repo_owner + ' ' + repo_name + ' ' + new_branch_name)
    response = requests.get(f'https://api.github.com/repos/{repo_owner}/{repo_name}/git/refs/heads')
    print(response.status_code)
    data = response.json()
    sha = data[0]['object']['sha']
    payload = {
        'ref': f'refs/heads/{new_branch_name}',
        'sha': sha
    }
    await github_object.post(f'repos/{repo_owner}/{repo_name}/git/refs', data=payload)