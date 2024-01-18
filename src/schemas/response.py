from pydantic import BaseModel, ConfigDict

class ResponseSchema(BaseModel):
    id: int
    user_id: int
    job_id: int
    message: str | None = None

    model_config = ConfigDict(from_attributes=True, frozen=True)
