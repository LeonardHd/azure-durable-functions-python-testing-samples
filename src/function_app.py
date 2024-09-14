import azure.functions as func
from app.orchestrations import hello_orchestrator
from app.activties import example_echo_activity
from app.http import orchestration_starter

app = func.FunctionApp()
app.register_functions(hello_orchestrator.bp)
app.register_functions(example_echo_activity.bp)
app.register_functions(orchestration_starter.bp)