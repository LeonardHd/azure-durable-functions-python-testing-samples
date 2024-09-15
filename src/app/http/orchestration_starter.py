from azure.functions import HttpMethod, HttpRequest, HttpResponse
from azure.durable_functions import Blueprint, DurableOrchestrationClient

from app.orchestrations.hello_orchestrator import EXAMPLE_ORCHESTRATION

bp = Blueprint()


@bp.route(
    route="orchestrators/hello",
    methods=[HttpMethod.POST],
    auth_level="anonymous",
)
@bp.durable_client_input(
    client_name="client",
)
async def example_orchestration_http_start(
    client: DurableOrchestrationClient, req: HttpRequest
) -> HttpResponse:
    return await _example_orchestration_http_start(client, req)

async def _example_orchestration_http_start(
    client: DurableOrchestrationClient, req: HttpRequest
) -> HttpResponse:
    instance_id = await client.start_new(
        orchestration_function_name=EXAMPLE_ORCHESTRATION,
        client_input=req.get_json(),
    )

    return client.create_check_status_response(req, instance_id)
