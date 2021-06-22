import httpx
import os


async def getProject(projectId: int):
    url = f'{base_url()}/api/project/{projectId}'

    async with httpx.AsyncClient() as client:
        h = {'X-override-token': 'true'}
        resp: httpx.Response = await client.get(url, headers=h)

        data = resp.json()

    return data

async def updateProjectStatus(projectId: int, status: str):
    print("client updating project status")
    url = f'{base_url()}/api/project/{projectId}'
    print(f"url: {url}");
    body = {
        'status': status
    }

    async with httpx.AsyncClient() as client:
        h = {'X-override-token': 'true'}
        resp: httpx.Response = await client.put(url, json=body, headers=h)

        print(f"Status code: {resp.status_code}")

        data = resp.json()

    return data

def base_url():
    return os.environ['PROJECTS_BASE_URL']
