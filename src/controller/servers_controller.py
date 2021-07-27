import httpx
from ..payloads import ServerCreatePayload, ServerUpdatePayload
from ..repository import servers_repository as db
from ..models.servers import Server, Status
from ..exceptions import MiddleException
import datetime

CLIENT_TIMEOUT = 60


async def create_server(payload: ServerCreatePayload):
    server = Server(
        name=payload.name.lower(),
        status=Status.ACTIVE,
        description=payload.description,
        url=payload.url,
        updatedDate=str(datetime.datetime.utcnow())
    )

    await validate_url(payload.url)

    serverdb = db.ServerRepository().find({'name': payload.name.lower()})
    if serverdb is not None:
        raise MiddleException(status=400, detail={'error': 'Server already exists'})

    db.ServerRepository().insert(server)
    return server


async def get_servers():
    servers = []
    for server in db.ServerRepository().find_all():
        servers.append(Server(**server))
    return servers


async def get_server(server_id: int):
    server = db.ServerRepository().find({'_id': server_id})
    if server is None:
        raise MiddleException(status=404,
                              detail={'error': 'Server not found'})
    return server


async def update_server(server_id: int, payload: ServerUpdatePayload):
    await validate_url(payload.url)
    server = db.ServerRepository().update_by_id(server_id, {'$set': {'url': payload.url}})
    if server is None:
        raise MiddleException(status=404,
                              detail={'error': 'Server not found'})

    return server


async def validate_url(url: str):
    try:
        async with httpx.AsyncClient(timeout=CLIENT_TIMEOUT) as client:
            h = {'X-Override-Token': 'true'}
            resp: httpx.Response = await client.get(url, headers=h)

            if resp.status_code >= 400:
                print(f"Ping URL {url} failed with status code {resp.status_code}: {resp.text}")
                raise MiddleException(status=400,
                                      detail={
                                          'error': 'Invalid URL. Ping failed: ' + resp.text,
                                          'status': resp.status_code
                                      })
    except httpx.HTTPError as e:
        raise MiddleException(status=400,
                              detail={'error': f'Invalid URL. Ping failed: {e}'})
