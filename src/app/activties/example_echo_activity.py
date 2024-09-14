from typing import Any

from azure.durable_functions import Blueprint


bp = Blueprint()


@bp.activity_trigger(input_name="inputDict")
def example_echo_activity(inputDict: dict[str, Any]):
    return inputDict
