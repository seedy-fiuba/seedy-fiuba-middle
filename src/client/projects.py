import httpx
import os


async def getProject(projectId: int):
    url = f"{os.environ['PROJECTS_BASE_URL']}/api/project/{projectId}"

    async with httpx.AsyncClient() as client:
        h = {'X-override-token': 'true'}
        resp: httpx.Response = await client.get(url, headers=h)

        data = resp.json()

    return data
