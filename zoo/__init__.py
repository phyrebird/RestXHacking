from flask_restx import Api

from .cat import api as cat_api
from .dog import api as dog_api

version = "v1.0"

api = Api(title="Zoo API", version=version, description="A simple demo API", doc=f"/api/{version}",)

api.add_namespace(cat_api)
api.add_namespace(dog_api)
