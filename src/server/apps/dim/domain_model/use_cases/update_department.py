from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field
from pydantic.json_schema import Examples

from server.apps.dim.domain_model.repositories import DepartmentRepository


class DepartmentUpdateDTO(BaseModel):
    id: Annotated[
        UUID,
        Field(description="Id фирмы"),
        Examples(["a1b2c3d4-e5f6-7890-1234-567890abcdef"]),
    ]
    code: Annotated[
        str,
        Field(description="Код фирмы"),
        Examples(["AV0302"]),
    ]
    name: Annotated[
        str,
        Field(description="Наименование фирмы"),
    ]
    is_deleted: Annotated[
        bool,
        Field(description="Признак удаления"),
        Examples([False]),
    ]


async def handle(
    dto: DepartmentUpdateDTO,
    repository: DepartmentRepository,
) -> None:
    instance = await repository.get_by_id(dto.id)

    for attr, value in dto.model_dump(exclude={"id"}).items():
        setattr(instance, attr, value)

    repository.add(instance)
