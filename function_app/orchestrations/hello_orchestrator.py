from datetime import timedelta
from typing import Any, Generator

from azure.durable_functions import Blueprint, DurableOrchestrationContext

hello_orchestrator_blueprint = Blueprint()

@hello_orchestrator_blueprint.activity_trigger(input_name="inputDict")
def example_echo_activity(inputDict: dict[str, Any]):
    return inputDict


@hello_orchestrator_blueprint.orchestration_trigger(
    context_name="context",
)
def example_orchestration(context: DurableOrchestrationContext) -> Generator[dict[str, Any], Any, Any]:
    _example_orchestration(context)

def _example_orchestration(context: DurableOrchestrationContext) -> Generator[dict[str, Any], Any, Any]:

    context.set_custom_status(context.get_input())
    expiry_time = context.current_utc_datetime + timedelta(minutes=5)

    while context.current_utc_datetime < expiry_time:

        first_result = yield context.call_activity(
            name=example_echo_activity,
            input_={"message": f"Hello, World at {context.current_utc_datetime}!"},
        )

        second_result = yield context.call_activity(
            name=example_echo_activity,
            input_={"message": f"Hello, again at {context.current_utc_datetime}!"},
        )

        context.set_custom_status({
            "first_result": first_result,
            "second_result": second_result,
        })

        yield context.create_timer(context.current_utc_datetime + timedelta(minutes=1))

    return {
        "message": "Goodbye, World!",
        "input": context.get_input(),
        "status": context.custom_status,
    }
