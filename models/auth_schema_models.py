from typing import Annotated, Literal
from pydantic import BaseModel, ConfigDict, Field, HttpUrl, EmailStr
from pydantic.alias_generators import to_camel


class AuthSchemaModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    access_token:  Annotated[str, Field(min_length=1)]
    refresh_token: Annotated[str, Field(min_length=1)]
    id: Annotated[int, Field(gt=0)]
    username: Annotated[str, Field(min_length=1,  max_length=25)]  # Flag: Assumption
    email: Annotated[EmailStr, Field(min_length=1, max_length=50)]  # Flag: Assumption
    first_name: Annotated[str, Field(min_length=1, max_length=50)]  # Flag: Assumption
    last_name: Annotated[str, Field(min_length=1, max_length=50)]  # Flag: Assumption
    gender: Literal['male', 'female']  # Flag: Assumption
    image: HttpUrl
