from pydantic import BaseModel


class AdminStatusResponse(BaseModel):
    project: str
    service: str
    environment: str
    version: str
    auth_enabled: bool
    auth_mode: str
