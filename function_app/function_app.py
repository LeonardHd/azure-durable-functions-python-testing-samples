import azure.functions as func
from orchestrations.hello_orchestrator import example_blueprint


app = func.FunctionApp()
app.register_functions(example_blueprint)