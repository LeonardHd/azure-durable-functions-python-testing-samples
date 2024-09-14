import datetime
from unittest.mock import Mock, PropertyMock
import pytest
import pytest_mock
from app.orchestrations.hello_orchestrator import _example_orchestration
from app.activties.example_echo_activity import example_echo_activity
from azure.durable_functions import DurableOrchestrationContext


def test__example_orchestrator_sets_initial_custom_status(
    mocker: pytest_mock.MockerFixture,
):
    # Arrange
    context_mock = Mock(spec=DurableOrchestrationContext)
    context_mock.get_input = Mock(return_value={"input": "Hello, World!"})
    context_mock.call_activity = Mock()
    context_mock.set_custom_status = Mock()

    type(context_mock).current_utc_datetime = PropertyMock(
        return_value=datetime.datetime(
            2021, 1, 1, 0, 0, 0
        )  # always return this value will cause infinite loop in the while loop
    )

    orchestration = _example_orchestration(context_mock)

    # Act
    next(orchestration)

    # Assert
    context_mock.set_custom_status.assert_called_once_with(context_mock.get_input())


def test__example_orchestrator_calls_activities_and_sets_status(
    mocker: pytest_mock.MockFixture,
):
    # Arrange
    context_mock = Mock(spec=DurableOrchestrationContext)
    context_mock.get_input = Mock(return_value={"input": "Hello, World!"})
    context_mock.call_activity = Mock(
        side_effect=[
            {"message": "Result from first activity"},
            {"message": "Result from second activity"},
        ]
    )
    context_mock.set_custom_status = Mock()
    type(context_mock).custom_status = PropertyMock(return_value="mocked custom status")

    type(context_mock).current_utc_datetime = PropertyMock(
        side_effect=[
            datetime.datetime(2021, 1, 1, 0, 0, 0),
            datetime.datetime(2021, 1, 1, 0, 1, 0),
            datetime.datetime(2021, 1, 1, 0, 2, 0),
            datetime.datetime(2021, 1, 1, 0, 3, 0),
            datetime.datetime(2021, 1, 1, 0, 4, 0),
            datetime.datetime(
                2021, 2, 1, 0, 0, 0
            ),  # this will cause the while loop to exit
        ]
    )

    orchestration = _example_orchestration(context_mock)

    # Act and Assert

    # -- First activity call (execute all the way to the first call_activity)
    next(orchestration)
    context_mock.call_activity.assert_called_once_with(
        name=example_echo_activity,
        input_={"message": "Hello, World at 2021-01-01 00:02:00!"},
    )

    # -- Second activity call (execute all the way to the second call_activity)
    orchestration.send({"message": "Result from first activity"})
    context_mock.call_activity.assert_called_with(
        name=example_echo_activity,
        input_={"message": "Hello, again at 2021-01-01 00:03:00!"},
    )

    # -- Timer creation (execute all the way to the timer creation)
    orchestration.send({"message": "Result from second activity"})

    context_mock.set_custom_status.assert_called_with(
        {
            "first_result": {"message": "Result from first activity"},
            "second_result": {"message": "Result from second activity"},
        }
    )

    # -- Timer expiration (execute all the way to the return statement)
    with pytest.raises(StopIteration):
        next(orchestration)
