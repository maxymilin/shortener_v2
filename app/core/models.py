from pydantic import BaseModel


class HealthCheck(BaseModel):
    """HealthCheck model for nice representation
    in the SwaggerUI under the schemas section.
    """

    name: str
    version: str
    description: str
