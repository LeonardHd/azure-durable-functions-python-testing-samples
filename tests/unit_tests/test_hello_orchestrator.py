import datetime
from unittest.mock import Mock, PropertyMock
import pytest_mock
from function_app.orchestrations.hello_orchestrator import _example_orchestration
from azure.durable_functions import DurableOrchestrationContext


def test__example_orchestration(mocker : pytest_mock.MockerFixture):
    # Arrange
    context_mock = Mock(spec=DurableOrchestrationContext)
    context_mock.get_input = Mock(return_value={"input": "Hello, World!"})
    context_mock.call_activity = Mock()
    context_mock.set_custom_status = Mock()
    context_mock

    # type(context_mock).current_utc_datetime = PropertyMock(
    #     side_effect=[
    #         datetime.datetime(2021, 1, 1, 0, 0, 0),
    #         datetime.datetime(2021, 1, 1, 0, 1, 0),
    #         datetime.datetime(2021, 1, 1, 0, 2, 0),
    #     ]
    # )
    type(context_mock).current_utc_datetime = PropertyMock(
        return_value=datetime.datetime(2021, 1, 1, 0, 0, 0) # always return this value will cause infinite loop in the while loop
    )

    orchestration = _example_orchestration(context_mock)

    # Act
    next(orchestration)

    # Assert
    context_mock.set_custom_status.assert_called_once_with(context_mock.get_input())

