from unittest.mock import AsyncMock, Mock
import pytest
import pytest_mock
from app.http.orchestration_starter import _example_orchestration_http_start
from azure.durable_functions import DurableOrchestrationClient
from azure.functions import HttpRequest


@pytest.mark.asyncio
async def test__example_orchestrator_sets_initial_custom_status(
    mocker: pytest_mock.MockerFixture,
):
    # Arrange
    start_new_mock = AsyncMock(return_value="mocked_instance_id")

    client_mock = Mock(spec=DurableOrchestrationClient)
    client_mock.start_new = start_new_mock

    request_mock = Mock(spec=HttpRequest)
    request_mock.get_json = Mock(return_value={"input": "Hello, World!"})

    # Act
    await _example_orchestration_http_start(client=client_mock, req=request_mock)

    # Assert

    start_new_mock.assert_called_once_with(
        orchestration_function_name="example_orchestration",
        client_input={"input": "Hello, World!"},
    )
