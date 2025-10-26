from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field
from pydantic.json_schema import Examples

from server.apps.dim.domain_model.entities import Department
from server.apps.dim.domain_model.repositories import DepartmentRepository
from server.core.exceptions import AlreadyExists, NotFound


class DepartmentCreateDTO(BaseModel):
    id: Annotated[
        UUID,
        Field(description="Id фирмы"),
        Examples(["a1b2c3d4-e5f6-7890-1234-567890abcdef"]),
    ]
    code: Annotated[
        str,
        Field(description="Код фирмы"),
        Examples(["AV0302"])
    ]
    name: Annotated[
        str,
        Field(description="Наименование фирмы"),
        Examples(["Прим - СЦ БизнесСтройИнструмент"]),
    ]
    is_deleted: Annotated[
        bool,
        Field(description="Признак удаления"),
        Examples([False]),
    ]


async def handle(
    dto: DepartmentCreateDTO,
    repository: DepartmentRepository,
) -> None:
    try:
        await repository.get_by_id(dto.id)
    except NotFound:
        instance = Department(**dto.model_dump())
    else:
        msg = f"{Department.__name__} with {dto.id!r} already exists"
        raise AlreadyExists(msg)

    repository.add(instance)
