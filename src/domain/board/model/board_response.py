from pydantic import BaseModel, ConfigDict, ValidationInfo, field_validator

from src.common.exception import WhiteSpaceError


class Category(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str

    @field_validator("name")
    def check_empty(cls, v: str, info: ValidationInfo):
        if not v or not v.strip():
            raise WhiteSpaceError(field=info.field_name)
        return v
