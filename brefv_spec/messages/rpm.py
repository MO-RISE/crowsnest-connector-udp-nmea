# generated by datamodel-codegen:
#   filename:  rpm.json
#   timestamp: 2022-10-17T06:10:37+00:00

from __future__ import annotations

from pydantic import BaseModel, Field


class RPM(BaseModel):
    __root__: float = Field(
        ..., description='RPM reading [Revolution Per Minute]', title='RPM'
    )
