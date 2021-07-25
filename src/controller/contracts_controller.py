from ..client import projects as projects_client
from ..responses import ContractProjectSearchResponse, ContractResponseModel


async def get_contracts(funder_id: str, size: str, page: str):
    params = {}

    if funder_id is not None:
        params['funderId'] = funder_id

    if size is not None:
        params['size'] = size

    if page is not None:
        params['page'] = page

    contracts = await projects_client.search_contracts(params)
    search_results = []

    if contracts.totalItems > 0:
        projects_ids = list(map(lambda c: str(c.projectId), contracts.contracts))
        projects_results = await projects_client.search_project({'id': ','.join(projects_ids)})

        for contract in contracts.contracts:
            project = list(filter(lambda p: p.id == contract.projectId, projects_results.results))

            if len(project) > 0:
                project = project[0]
            else:
                project = None

            result = ContractResponseModel(contract=contract, project=project)
            search_results.append(result)

    return ContractProjectSearchResponse(totalItems=contracts.totalItems,
                                         results=search_results,
                                         totalPages=contracts.totalPages,
                                         currentPage=contracts.currentPage)