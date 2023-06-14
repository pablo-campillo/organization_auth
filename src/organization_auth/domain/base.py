from datetime import datetime
from uuid import uuid4
from pydantic import UUID4, BaseModel, Field

from organization_auth.domain.utils import my_utc_now


class DCEBaseModel(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=my_utc_now)
    updated_at: datetime = Field(default_factory=my_utc_now)

    class Config:
        orm_mode = True

    def __setattr__(self, key, val):
        super().__setattr__(key, val)
        if key != "updated_at":
            self.updated_at = my_utc_now()
