import httpx


async def getProject(projectId: int):
    url = f'https://seedy-fiuba-projects-api.herokuapp.com/api/project/{projectId}'

    async with httpx.AsyncClient() as client:
        h = {'X-override-token': 'true'}
        resp: httpx.Response = await client.get(url, headers=h)

        data = resp.json()

    return data
