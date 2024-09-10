import azure.functions as func
from orchestrations.hello_orchestrator import hello_orchestrator_blueprint


app = func.FunctionApp()
app.register_functions(hello_orchestrator_blueprint)