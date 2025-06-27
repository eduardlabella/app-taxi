import azure.functions as func
from sessionstart import sessionstart

app = func.FunctionApp()

# Registra rutas con el decorador del app
app.route(route="sessionstart", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)(sessionstart)
#app.route(route="sessionend", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)(sessionend_function)
