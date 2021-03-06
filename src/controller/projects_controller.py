from src.client.responses.smart_contract import ProjectStatus
from ..payloads import FundProjectPayload, AcceptStagePayload, CreateProjectPayload
from ..client import users as users_client, projects as projects_client, smart_contract as sc_client
from ..client.payloads.smart_contract import FundSCProject, AcceptSCProjectStage
from ..client.payloads.projects import FundProjectClientPayload, UpdateProjectPayload
from ..exceptions import MiddleException
from ..utils.map_status import PROJECT_STATUS_FOR_SC_STATUS
from ..models.projects import Status


async def get_projects():
    return await projects_client.get_projects()


async def search_projects(params: dict):
    for key, value in dict(params).items():
        if value is None:
            del params[key]

    return await projects_client.search_projects(params)


async def get_project_by_id(id: int):
    return await projects_client.get_project(id)


async def create_project(payload: CreateProjectPayload):
    return await projects_client.create_project(payload)


async def update_project(project_id: int, payload: UpdateProjectPayload):
    return await projects_client.update_project(project_id, payload)


async def fund_project(project_id: int, payload: FundProjectPayload):
    # Get funder private key
    funder = await users_client.get_user(payload.funderId)

    if funder.walletPrivateKey is None:
        raise MiddleException(status=400, detail={'error': 'Funder does not have a wallet', 'status': 400})

    # Get Project Wallet Id from project
    project = await projects_client.get_project(project_id)

    if project.walletId is None:
        raise MiddleException(status=400, detail={'error': 'Project does not have a wallet', 'status': 400})

    if project.status != Status.FUNDING:
        raise MiddleException(status=400, detail={'error': 'Project is not in  funding status', 'status': 400})

    # Fund in Smart Contract
    fund = await sc_client.fund_project(project.walletId,
                                        FundSCProject(
                                            funderPrivateKey=funder.walletPrivateKey,
                                            amount=payload.amount
                                        ))

    # Fund in Projects Api
    await projects_client.fund_project(project_id,
                                FundProjectClientPayload(
                                    funderId=payload.funderId,
                                    currentFundedAmount=payload.amount,
                                    txHash=fund.txHash
                                 ))

    # Update in Projects Api
    await projects_client.update_project(project_id,
                                         UpdateProjectPayload(
                                             status=PROJECT_STATUS_FOR_SC_STATUS[fund.projectStatus],
                                             missingAmount=fund.missingAmount
                                         ))

    return ''


async def accept_stage(project_id: int, stage_id: int, payload: AcceptStagePayload):
    # Get reviewer private key
    reviewer = await users_client.get_user(payload.reviewerId)

    if reviewer.walletPrivateKey is None:
        raise MiddleException(status=400, detail={'error': 'Reviewer does not have a wallet', 'status': 400})

    # Get Project Wallet Id from project
    project = await projects_client.get_project(project_id)

    if project.walletId is None:
        raise MiddleException(status=400, detail={'error': 'Project does not have a wallet', 'status': 400})

    if project.status != Status.STAGE_PENDING_REVIEWER:
        raise MiddleException(status=400, detail={'error': 'Project is not pending review for stage', 'status': 400})

    # Accept stage in Smart Contract
    sc_response = await sc_client.accept_stage(project.walletId,
                                               AcceptSCProjectStage(
                                                   reviewerPrivateKey=reviewer.walletPrivateKey,
                                                   completedStage=stage_id + 1
                                               ))

    # Update project in Projects Api
    if sc_response.projectStatus == ProjectStatus.IN_PROGRESS:
        update_project_payload = UpdateProjectPayload(
                                             status=PROJECT_STATUS_FOR_SC_STATUS[sc_response.projectStatus],
                                             currentStageId=sc_response.stageCompleted
                                         )
    else:
        update_project_payload = UpdateProjectPayload(
                                             status=PROJECT_STATUS_FOR_SC_STATUS[sc_response.projectStatus]
                                         )

    await projects_client.update_project(project_id, update_project_payload)

    return ''


async def request_stage_review(project_id: int):
    return await projects_client.update_project(project_id, UpdateProjectPayload(
        status=Status.STAGE_PENDING_REVIEWER
    ))

