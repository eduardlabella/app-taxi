import azure.functions as func

from gethotspot import get_hotspot
from gettariff import get_tariff
from sessionstart import sessionstart

app = func.FunctionApp()

# Registra rutas con el decorador del app
app.route(route="sessionstart", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)(sessionstart)
app.route(route="gettariff", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)(get_tariff)
app.route(route="gethotspot", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)(get_hotspot)


#app.route(route="sessionend", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)(sessionend_function)
